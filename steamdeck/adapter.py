#!/usr/bin/env python3
# Bounded RAM/capability recognition test. No flash, driver or boot changes.
import os, sys, subprocess, time, signal, json, errno
from pathlib import Path
SELF=str(Path(__file__).resolve())
TRIGGER='/sys/kernel/debug/dri/0/DP-1/trigger_hotplug'
LOG='/tmp/CAC-Deck-Betrieb-Ruecksetzung.log'
CORE="items=hid.enumerate(0x06cb,0x7100)\nif len(items)!=1: raise RuntimeError('Ambiguous device')\nfd=os.open(items[0]['path'],os.O_RDWR)\ndef command(cmd,address=0,length=0,payload=b''):\n if cmd not in (1,2,0x21,0x31): raise ValueError('Forbidden command')\n if cmd==0x21 and (length!=1 or (address,payload) not in ((0x90000217,b'\\x08'),(0x90000217,b'\\x48'),(0x9000025b,b'\\x0a'),(0x9000025b,b'\\x02'))): raise ValueError('Forbidden write')\n b=bytearray(62);b[0]=1;b[2]=13+len(payload);b[5]=cmd|0x80\n struct.pack_into('<II',b,7,address,length);b[15:15+len(payload)]=payload\n fcntl.ioctl(fd,0xC03E480B,b,True);time.sleep(.02)\n for _ in range(100):\n  buf=bytearray(62);buf[0]=1\n  fcntl.ioctl(fd,0xC03E480A,buf,True)\n  r=bytes(buf)\n\n  if len(r)<15: raise RuntimeError('Short reply')\n  if r[5]&0x80: time.sleep(.01);continue\n  if r[0]!=1 or r[5]!=cmd: raise RuntimeError('Wrong command echo')\n  if cmd==1:\n   if r[4]!=1: raise RuntimeError('RC not enabled')\n   print('RC enabled, status',r[6]);return b''\n  if r[6]: raise RuntimeError('Command error '+hex(r[6]))\n  if cmd==2:return b''\n  end,n=struct.unpack_from('<II',r,7)\n  if end!=address+length or n!=length: raise RuntimeError('Address/length mismatch')\n  return r[15:15+length]\n raise RuntimeError('Timeout')\n"
def ram(value=None,address=0x90000217):
 import hid, struct, fcntl
 allowed={0x90000217:(b'\x08',b'\x48'),0x9000025b:(b'\x0a',b'\x02')}
 original,test=allowed[address]
 if value is not None and value not in (original,test):raise ValueError('Forbidden value')
 namespace=dict(hid=hid,struct=struct,time=time,os=os,fcntl=fcntl)
 exec(CORE,namespace)
 command=namespace['command']; fd=namespace['fd']
 try:
  command(1,0,5,b'PRIUS')
  old=command(0x31,address,1)
  if old not in (original,test):raise RuntimeError('Unexpected config '+old.hex())
  if value is not None:
   if value==test and old!=original:raise RuntimeError('Enable requires original config')
   if old!=value:command(0x21,address,1,value)
   if command(0x31,address,1)!=value:raise RuntimeError('RAM verification failed')
  return (value or old).hex()
 finally:
  try:command(2)
  finally:os.close(fd)
def worker(action):
 r=subprocess.run([sys.executable,SELF,'--worker',action],capture_output=True,text=True,timeout=4)
 if r.returncode:raise RuntimeError(r.stderr+r.stdout)
 print(r.stdout.strip(),flush=True)
 return r.stdout.strip().splitlines()[-1]
def detect():
 code="import sys; f=open(sys.argv[1],'w'); f.write(sys.argv[2]); f.close()"
 subprocess.run([sys.executable,'-c',code,TRIGGER,'1\n'],check=True,timeout=8)
def kde(*args):
 env=os.environ.copy()
 sessions=[]
 for p in Path('/proc').glob('[0-9]*/comm'):
  try:
   if p.stat().st_uid==1000 and p.read_text().strip()=='plasmashell':
    entries=(p.parent/'environ').read_bytes().split(b'\0')
    sessions.append(dict(e.decode().split('=',1) for e in entries if b'=' in e))
  except OSError:pass
 if len(sessions)!=1:raise RuntimeError('Ambiguous KDE session')
 for k in ('XDG_RUNTIME_DIR','WAYLAND_DISPLAY','DBUS_SESSION_BUS_ADDRESS'):
  env[k]=sessions[0][k]
 env['QT_QPA_PLATFORM']='wayland'
 r=subprocess.run(['kscreen-doctor',*args],env=env,user=1000,group=1000,extra_groups=[],capture_output=True,text=True,timeout=5)
 if r.returncode:raise RuntimeError('KDE operation failed: '+r.stderr+r.stdout)
 return r.stdout
def screen():
 config=json.loads(kde('-j'))
 outputs=[o for o in config['outputs'] if o['name']=='DP-1' and o['enabled']]
 if len(outputs)!=1:raise RuntimeError('Expected one enabled DP-1')
 o=outputs[0]
 mode=next(m for m in o['modes'] if m['id']==o['currentModeId'])
 print('KDE:',json.dumps(dict(mode=mode['name'],hdr=o.get('hdr'),vrrPolicy=o.get('vrrPolicy'))),flush=True)
 return o,mode
def restore():
 errors=[]
 try:kde("output.DP-1.vrrpolicy.never")
 except Exception as e:errors.append("KDE restore: "+repr(e))
 for action,expected in [('restore','08'),('restore-type','0a')]:
  for attempt in range(3):
   try:
    if worker(action)!=expected:raise RuntimeError('Restore not confirmed')
    break
   except Exception as e:
    if attempt==2:errors.append(repr(e))
    else:time.sleep(.5)
 if errors:raise RuntimeError('; '.join(errors))
def caps_once():
 fd=os.open('/dev/drm_dp_aux1',os.O_RDONLY)
 try:
  identity=os.pread(fd,16,0x500)
  if identity[:9]!=bytes.fromhex('90cc2453594e417100') or identity[10:13]!=bytes.fromhex('070274'):raise RuntimeError('Wrong adapter/firmware')
  result={}
  for off,n in [(7,1),(0x80,16),(0x107,1),(0x160,1),(0x2200,16),(0x2214,1),(0x3030,16)]:
   data=os.pread(fd,n,off)
   if len(data)!=n:raise RuntimeError('Short AUX read')
   result[f'{off:05X}']=data.hex(' ')
  print(json.dumps(result),flush=True)
  return result
 finally:os.close(fd)
def caps():
 deadline=time.monotonic()+6
 attempts=0
 while True:
  try:return caps_once()
  except OSError as e:
   if e.errno not in (errno.EBUSY,errno.EAGAIN,errno.EIO) or time.monotonic()>=deadline:raise
   attempts+=1
   if attempts==1:print('AUX busy during detection; waiting for readable capabilities.',flush=True)
   time.sleep(.25)
def drm():
 r=subprocess.run(['modetest','-M','amdgpu','-c'],capture_output=True,text=True,timeout=4)
 if r.returncode:raise RuntimeError('DRM query failed')
 lines=r.stdout.splitlines();dp=False
 for i,line in enumerate(lines):
  if '\tDP-1' in line:dp=True;print(line,flush=True)
  if dp and ('vrr_capable:' in line):print(' | '.join(lines[i:i+5]),flush=True)
def interrupted(*args):raise KeyboardInterrupt()
def main():
 if os.geteuid()!=0:raise SystemExit('Run with sudo')
 if len(sys.argv)>1 and sys.argv[1]=='--worker':
  action=sys.argv[2]
  mapping={'read':(None,0x90000217),'enable':(b'\x48',0x90000217),'restore':(b'\x08',0x90000217),'read-type':(None,0x9000025b),'enable-type':(b'\x02',0x9000025b),'restore-type':(b'\x0a',0x9000025b)}
  print(ram(*mapping[action]),flush=True)
  return
 if len(sys.argv)>1 and sys.argv[1]=='--watchdog':
  time.sleep(90)
  restore()
  print('Watchdog: RAM217=08 and RAM25B=0A verified; refreshing original capabilities.',flush=True)
  detect();caps()
  return
 for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(sig,interrupted)
 if worker('read')!='08' or worker('read-type')!='0a':raise RuntimeError('Original config required')
 o,mode=screen()
 if mode['size']!={'width':3840,'height':2160} or abs(mode['refreshRate']-120)>.2 or not o.get('hdr'):raise RuntimeError('Expected baseline 4K120 HDR')
 stored=json.loads(Path('/home/deck/.config/kwinoutputconfig.json').read_text())
 entries=[o for section in stored if section['name']=='outputs' for o in section['data'] if o.get('connectorName')=='DP-1']
 if not entries or any(o.get('vrrPolicy')!='Never' for o in entries):raise RuntimeError('Expected original VRR Never; refusing to overwrite another policy')
 before=caps()
 if before['00007']!='81' or before['02214']!='00':raise RuntimeError('Unexpected baseline capabilities')
 if not Path(TRIGGER).is_file():raise RuntimeError('Missing trigger')
 print('Temporary test: RAM217 08->48 and RAM25B 0A->02; no flash write. Picture may disappear.',flush=True)
 if input('Type JA for a 20-second VRR Always test at current 4K120 HDR: ').strip()!='JA':
  print('Cancelled; no RAM writes.');return
 # Independent process and new session: survives parent termination/SSH disconnect.
 log=open(LOG,'w')
 guard=subprocess.Popen([sys.executable,SELF,'--watchdog'],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 success=False
 try:
  worker('enable-type')
  worker('enable')
  active=caps()
  if active['00007']!='c1' or active['02214']!='03':raise RuntimeError('Capabilities not verified')
  print('RAM48 verified. Software detection; no cable changes.',flush=True)
  detect();caps();drm()
  time.sleep(3)
  print('Settled observation:',flush=True);caps();drm()
  kde('output.DP-1.vrrpolicy.always')
  print('VRR Always requested: observe TV for 20 seconds.',flush=True)
  screen()
  for _ in range(4):
   time.sleep(5);caps()
  print('VRR observation finished.',flush=True)
 finally:
  print('Restoring original RAM and source detection.',flush=True)
  try:
   restore();detect()
   after=caps()
   if after['00007']!='81' or after['02214']!='00':raise RuntimeError('Original capabilities not verified')
   success=True
   print('RESTORED: RAM217=08, RAM25B=0A and original81/00 capabilities verified.',flush=True)
  except Exception as e:
   print('Restore incomplete:',repr(e),flush=True)
   print('Independent recovery remains scheduled. If no recovery: unplug USB-C for10seconds.',flush=True)
  if success and guard.poll() is None:
   guard.terminate();guard.wait(timeout=3)
  log.close()
if __name__=='__main__':main()
