#!/usr/bin/python3
import os,sys,time,signal,subprocess,json,importlib.util,hid
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('adapter',HERE/'adapter.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
OWNED=Path("/run/cac2505-vrr/owned.json")
stopping=False
state=None
blocked=None
missing_hid=0

def log(s):print(s,flush=True)
def run(cmd,**kw):
 r=subprocess.run(cmd,capture_output=True,text=True,timeout=8,**kw)
 output=r.stdout+r.stderr
 if r.returncode or 'Command not found.' in output:raise RuntimeError('Command failed: '+output)
 return output

def probe():
 matches=[]
 for connector in Path('/sys/class/drm').glob('card*-DP-*'):
  try:
   edid=(connector/'edid').read_bytes()
   if len(edid)<128 or edid[8:12]!=bytes.fromhex('1e6d0100'):continue
   auxes=list(connector.glob('drm_dp_aux*'))
   for aux in auxes:
    f=os.open('/dev/'+aux.name,os.O_RDONLY)
    try:identity=os.pread(f,16,0x500)
    finally:os.close(f)
    if identity[:9]==bytes.fromhex('90cc2453594e417100') and identity[10:13]==bytes.fromhex('070274'):
     trigger=Path('/sys/kernel/debug/dri/0')/connector.name.split('-',1)[1]/'trigger_hotplug'
     matches.append((str(connector),'/dev/'+aux.name,str(trigger)))
  except OSError:continue
 if len(matches)>1:raise RuntimeError('Ambiguous adapter/TV; no activation')
 return matches[0] if matches else None

def snapshot(aux):
 f=os.open(aux,os.O_RDONLY)
 try:
  return {hex(off):os.pread(f,n,off).hex() for off,n in [(7,1),(0x80,4),(0x2214,1),(0x3030,16)]}
 finally:os.close(f)

def detect(trigger):
 run([sys.executable,'-c',"import sys;open(sys.argv[1],'w').write('1\\n')",trigger])
 time.sleep(3)

def session():
 plasma=[];games=[]
 for p in Path('/proc').glob('[0-9]*/comm'):
  try:
   status=(p.parent/'status').read_text()
   uid_line=next(line for line in status.splitlines() if line.startswith('Uid:'))
   if int(uid_line.split()[1])!=1000:continue
   name=p.read_text().strip()
   if name=='plasmashell':plasma.append(p.parent.name)
   if name in ('gamescope','gamescope-wl'):games.append(p.parent.name)
  except OSError:pass
 if len(plasma)==1:return ('desktop',plasma[0])
 if len(games)==1:return ('gaming',games[0])
 return None

def gaming_env():
 p=Path('/run/user/1000/gamescope-environment')
 values=dict(line.split('=',1) for line in p.read_text().splitlines() if '=' in line)
 allowed=['XDG_RUNTIME_DIR','GAMESCOPE_WAYLAND_DISPLAY','WAYLAND_DISPLAY','DISPLAY','DBUS_SESSION_BUS_ADDRESS']
 env={'PATH':'/usr/bin:/bin','HOME':'/home/deck','USER':'deck','LOGNAME':'deck'}
 for k in allowed:
  if k in values:env[k]=values[k]
 if not env.get('GAMESCOPE_WAYLAND_DISPLAY'):raise RuntimeError('Gaming session environment not ready')
 return env

def display_on(mode):
 if mode=='desktop':
  a.kde('output.DP-1.mode.3840x2160@120','output.DP-1.hdr.enable','output.DP-1.vrrpolicy.always')
  output,timing=a.screen()
  if timing['size']!={'width':3840,'height':2160} or abs(timing['refreshRate']-120)>.2 or not output.get('hdr'):raise RuntimeError('Desktop 4K120 HDR not confirmed')
 else:
  env=gaming_env()
  helptext=run(['/usr/bin/gamescopectl','help'],env=env,user=1000,group=1000,extra_groups=[])
  if 'adaptive_sync' not in helptext:raise RuntimeError('Installed Gamescope has no verified adaptive_sync control')
  result=run(['/usr/bin/gamescopectl','adaptive_sync','1'],env=env,user=1000,group=1000,extra_groups=[])
  log('Gaming VRR requested: '+result.strip())
  log('Gaming 4K120/HDR must be selected once in Steam display settings; not forced by this helper.')

def display_off():
 s=session()
 if not s:return
 if s[0]=='desktop':a.kde('output.DP-1.vrrpolicy.never')
 else:run(['/usr/bin/gamescopectl','adaptive_sync','0'],env=gaming_env(),user=1000,group=1000,extra_groups=[])

def restore(info):
 errors=[]
 try:display_off()
 except Exception as e:log('VRR disable warning: '+str(e))
 for action,want in [('restore','08'),('restore-type','0a')]:
  try:
   if a.worker(action)!=want:raise RuntimeError('Readback mismatch')
  except Exception as e:errors.append(str(e))
 if errors:raise RuntimeError('RAM restoration unconfirmed: '+'; '.join(errors))
 detect(info[2]);OWNED.unlink(missing_ok=True);log('Original RAM08/0A restored; display detection requested')

def activation(info,s):
 log('Waiting ten seconds for a settled adapter connection')
 for _ in range(50):
  if stopping:raise RuntimeError('Service stopping before activation')
  time.sleep(.2)
 if probe()!=info or session()!=s:raise RuntimeError('Connection/session changed while settling; no RAM write')
 if a.worker('read')!='08' or a.worker('read-type')!='0a':raise RuntimeError('Expected original RAM08/0A; refusing to adopt another test')
 OWNED.write_text(json.dumps(info))
 try:
  a.worker('enable-type');a.worker('enable')
  values=snapshot(info[1])
  if values['0x7']!='c1' or values['0x80']!='0bf01afe' or values['0x2214']!='03':raise RuntimeError('Capabilities not confirmed')
  detect(info[2]);display_on(s[0]);log('Activated '+s[0]+' session; '+json.dumps(snapshot(info[1])))
 except BaseException:
  restore(info);raise

def stop(*args):
 global stopping
 stopping=True

def main():
 global state,blocked,missing_hid
 if os.geteuid()!=0:raise SystemExit('Root service required')
 for sig in (signal.SIGINT,signal.SIGTERM):signal.signal(sig,stop)
 log('CAC automatic helper started: exact firmware7.02.116 / LG identity only')
 try:
  while not stopping:
   try:
    info=probe();s=session()
    key=(info,s)
    if not info:
     devices=hid.enumerate(0x06cb,0x7100)
     if devices:
      # AUX/EDID may be temporarily unavailable; keep ownership of active RAM.
      missing_hid=0
     else:
      missing_hid+=1
      if missing_hid>=3:
       if state:
        try:display_off()
        except Exception as e:log('Disconnect VRR disable warning: '+str(e))
        log('USB adapter absent in three checks; volatile state discarded')
       state=None;blocked=None;OWNED.unlink(missing_ok=True)
    elif not s:missing_hid=0
    elif state and info==state[0] and s!=state[1]:
     missing_hid=0
     display_on(s[0]);state=(info,s);log('Session switch: '+s[0])
    elif state is None and key!=blocked:
     missing_hid=0
     activation(info,s);state=(info,s);blocked=None
    elif state and info!=state[0]:
     raise RuntimeError('Connector changed; disconnect/reconnect before retry')
   except Exception as e:
    log('Activation stopped: '+repr(e))
    if state:
     try:restore(state[0])
     except Exception as recovery:log('RECOVERY FAILED: '+repr(recovery)+'; unplug USB-C10seconds')
    state=None
    blocked=locals().get('key')
   for _ in range(10):
    if stopping:break
    time.sleep(.2)
 finally:
  if state:
   try:restore(state[0])
   except Exception as e:log('Stop recovery failed: '+repr(e)+'; unplug USB-C10seconds')
def recover():
 if not OWNED.exists():return
 info=probe()
 if not info:
  log('Recovery: matching adapter/TV absent; if still connected, unplug USB-C10seconds')
  return
 restore(info)
if __name__=='__main__':
 if sys.argv[1:]==['--recover']:recover()
 else:main()
