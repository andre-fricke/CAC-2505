#!/usr/bin/python3
import subprocess,sys,time,signal,json,hashlib
from pathlib import Path
# Parent logger: captures Python, helper and CLI output, while preserving terminal input.
import os as _log_os, datetime as _log_datetime
if '--watchdog' not in sys.argv and _log_os.environ.get('CAC_TEST_LOG_CHILD') != '1':
 _log_here=Path(__file__).resolve().parent
 _log_stamp=_log_datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
 _log_path=_log_here/(Path(__file__).stem+'-'+_log_stamp+'.log')
 _log_latest=_log_here/(Path(__file__).stem+'-latest.log')
 _log_env=_log_os.environ.copy();_log_env['CAC_TEST_LOG_CHILD']='1'
 print('Automatic test log:',str(_log_path),flush=True)
 with _log_path.open('w',buffering=1) as _log_file, _log_latest.open('w',buffering=1) as _log_copy:
  _log_proc=subprocess.Popen([sys.executable,'-u',str(Path(__file__).resolve()),*sys.argv[1:]],env=_log_env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,bufsize=1)
  def _log_write(_line):
   sys.stdout.write(_line);sys.stdout.flush();_log_file.write(_line);_log_copy.write(_line)
  try:
   # Reading characters also exposes input prompts without a trailing newline.
   while True:
    _log_char=_log_proc.stdout.read(1)
    if not _log_char:break
    _log_write(_log_char)
   _log_status=_log_proc.wait()
  except KeyboardInterrupt:
   if _log_proc.poll() is None:_log_proc.send_signal(signal.SIGINT)
   try:
    for _log_line in _log_proc.stdout:_log_write(_log_line)
    _log_status=_log_proc.wait(timeout=30)
   except subprocess.TimeoutExpired:
    _log_status=130
    _log_write('Logger interrupted; independent recovery remains scheduled.\n')
  _log_write('\nTest process exit: '+str(_log_status)+'\n')
 print('Saved:',str(_log_path),flush=True)
 sys.exit(_log_status)


HERE=Path(__file__).resolve().parent
import base64,re,select,plistlib
CLI='/opt/homebrew/bin/betterdisplaycli'
SELECT='--UUID=0A65EDC5-C030-4BD5-8B0C-3FFE1ECCDE42'
BIN=HERE/'CAC-Mac-Typ-RAM-Robust'
ORIGINAL=(HERE/'LG-Mac-EDID-original.bin').read_bytes()
TEST=(HERE/'LG-Mac-EDID-range48.bin').read_bytes()
def call(op,flag,checked=True):
 r=subprocess.run([CLI,op,SELECT,flag],capture_output=True,text=True,timeout=8)
 print(op,flag.split('=')[0],'exit',r.returncode,flush=True)
 print(r.stdout+r.stderr,flush=True)
 if checked and r.returncode:raise RuntimeError('BetterDisplay failed: '+flag.split('=')[0])
 return r.stdout.strip()
def ram(mode):
 attempts=3 if mode in ('--inspect','--restore') else 1
 for attempt in range(attempts):
  r=subprocess.run([str(BIN),mode],capture_output=True,text=True,timeout=20)
  print(r.stdout+r.stderr,flush=True)
  if r.returncode==0:return r.stdout
  if attempt+1<attempts:
   print('HID retry after settling:',mode,attempt+1,flush=True);time.sleep(2)
 raise RuntimeError('RAM operation failed: '+mode)

def fixed60():
 if call('get','--hdr')!='off':call('set','--hdr=off')
 modes=call('get','--displayModeList')
 candidates=[m.group(1) for line in modes.splitlines() if (m:=re.match(r'^(\d+) - 3840x2160 60Hz ',line)) and 'HiDPI' not in line and 'Unsafe' not in line]
 if len(candidates)!=1:raise RuntimeError('No unique safe listed 4K60 mode')
 call('set','--displayModeNumber='+candidates[0]);time.sleep(2)
 modes=call('get','--connectionModeList')
 candidates=[m.group(1) for line in modes.splitlines() if (m:=re.match(r'^(\d+) - 3840x2160 60\.00Hz Fixed 8bit SDR RGB Full ',line))]
 if len(candidates)!=1:raise RuntimeError('No unique compatible fixed 4K60 RGB8 mode')
 call('set','--connectionMode='+candidates[0]);time.sleep(3)
 info=call('get','--displayInformation')
 connection=info.split('Current Display Mode (Connection Level)',1)[1].split('Preferred Display Mode (Connection Level)',1)[0]
 if '3840 x 2160' not in connection or 'Bit Depth: 8 bits per sample' not in connection or not re.search(r'Refresh Rate: 59\.\d+',connection) or 'Variable Refresh Rate: No' not in connection:raise RuntimeError('Fixed 4K60 SDR8 not verified')
 print('VERIFIED fixed 4K60 SDR8. DSC state:', 'No' if 'Display Stream Compression (DSC): No' in info else 'Yes or unknown; see capture',flush=True)

def capture(phase):
 print('CAPTURE',phase,time.strftime('%Y-%m-%d %H:%M:%S'),flush=True)
 for flag in ('--displayInformation','--dpcdReport','--refreshRateList'):
  try:call('get',flag)
  except Exception as e:print('Capture failed:',str(e),flush=True)
 try:
  r=subprocess.run(['/usr/sbin/ioreg','-r','-c','IOMobileFramebuffer','-a'],capture_output=True,timeout=10)
  tree=plistlib.loads(r.stdout);matches=[]
  def walk(o):
   if isinstance(o,dict):
    a=o.get('DisplayAttributes',{})
    if a.get('ProductAttributes',{}).get('ProductName')=='LG TV SSCR2':
     entries=[]
     def timings(v):
      if isinstance(v,dict):
       if 'MaximumVariableRefreshRate' in v:entries.append({k:x for k,x in v.items() if isinstance(x,(int,float,str,bool))})
       for x in v.values():timings(x)
      elif isinstance(v,list):
       for x in v:timings(x)
     for key in ('TimingElements','PreferredTimingElements'):timings(o.get(key,[]))
     matches.append({'attributes':a,'timings':entries})
    for v in o.values():walk(v)
   elif isinstance(o,list):
    for v in o:walk(v)
  walk(tree)
  (HERE/('CAC-Mac-VRR-Auswahl-'+phase+'.json')).write_text(json.dumps(matches,indent=2,default=str))
  print('Native SupportsVRR:',[m['attributes'].get('SupportsVariableRefreshRate') for m in matches],flush=True)
 except Exception as e:print('Registry capture failed:',str(e),flush=True)

def recover():
 errors=[]
 # Stop source VRR before removing the sink capability. Try again after factory reprobe.
 try:fixed60()
 except Exception as e:print('Initial fixed-mode recovery warning; retrying after factory cleanup:',str(e),flush=True)
 try:ram('--restore')
 except Exception as e:errors.append('RAM restore: '+str(e))
 for op,flag in [('set','--autoApplyCustomEDID=off'),('perform','--applyFactoryEDID'),('set','--customEDID')]:
  try:call(op,flag)
  except Exception as e:errors.append('Factory cleanup: '+str(e))
 time.sleep(3)
 try:fixed60()
 except Exception as e:errors.append('Final fixed-mode recovery: '+str(e))
 state=ram('--inspect')
 if 'RAM 90000217 = 08' not in state or 'RAM 9000025B = 0A' not in state:raise RuntimeError('Original RAM not confirmed')
 osedid=base64.b64decode(call('get','--osEDID'),validate=True)
 wire=base64.b64decode(call('get','--i2cEDID'),validate=True)
 known={hashlib.sha256(ORIGINAL).hexdigest(),'fcb048faa03baf2d3c106f2b0b1cd191df1557322022c94ab8c48b39488a57b0'}
 if osedid!=wire or hashlib.sha256(osedid).hexdigest() not in known or any(sum(osedid[i:i+128])%256 for i in (0,128)):raise RuntimeError('Known factory EDID / I2C equality not confirmed')
 if errors:raise RuntimeError('; '.join(errors))
 print('RESTORED: fixed 4K60 SDR8, RAM08/0A, known valid factory EDID matching I2C.',flush=True)

def wait_return(prompt,seconds,required=True):
 print(prompt,flush=True)
 ready,_,_=select.select([sys.stdin],[],[],seconds)
 if not ready:
  if required:raise RuntimeError('Input deadline expired')
  print('Selection window elapsed; capturing current state before recovery.',flush=True)
  return None
 return sys.stdin.readline().strip()

if sys.argv[1:]==['--watchdog']:
 time.sleep(300);recover();sys.exit(0)
if sys.argv[1:]:raise SystemExit('Unexpected arguments')
baseline=base64.b64decode(call('get','--osEDID'),validate=True)
known_baselines={hashlib.sha256(ORIGINAL).hexdigest(),'fcb048faa03baf2d3c106f2b0b1cd191df1557322022c94ab8c48b39488a57b0'}
if hashlib.sha256(baseline).hexdigest() not in known_baselines or baseline!=base64.b64decode(call('get','--i2cEDID'),validate=True):raise SystemExit('Unexpected baseline EDID; no changes')
if call('get','--autoApplyCustomEDID')!='off':raise SystemExit('Custom EDID auto-apply active; no changes')
if call('get','--customEDID',False):raise SystemExit('Custom EDID response not empty; no changes')
state=ram('--inspect')
if 'RAM 90000217 = 08' not in state or 'RAM 9000025B = 0A' not in state:raise SystemExit('Unexpected RAM baseline; no changes')
print('Temporary RAM48/02 + range EDID test at fixed 4K60 SDR8. HDMI-only reconnect. Select variable refresh ONLY when prompted. Independent recovery after 300 seconds; no flash writes. Final mode remains 4K60 SDR8.',flush=True)
if input('Type YES to run: ').strip()!='YES':raise SystemExit('Cancelled')
def interrupted(*args):raise KeyboardInterrupt
for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(sig,interrupted)
with (HERE/'CAC-Mac-VRR-Auswahl-Watchdog.log').open('w') as log:
 guard=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'--watchdog'],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 restored=False
 try:
  fixed60();capture('before')
  ram('--enable')
  wait_return('Leave USB-C connected. Unplug ONLY HDMI, wait ten seconds, reconnect HDMI, then press Return within 60 seconds.',60)
  time.sleep(8)
  state=ram('--inspect')
  if 'RAM 90000217 = 48' not in state or 'RAM 9000025B = 02' not in state:raise RuntimeError('Temporary RAM settings lost')
  call('set','--customEDID='+base64.b64encode(TEST).decode());call('perform','--applyCustomEDID');time.sleep(4)
  if base64.b64decode(call('get','--osEDID'),validate=True)!=TEST:raise RuntimeError('Test EDID not adopted')
  fixed60();capture('ready')
  wait_return('On the built-in display: System Settings > Displays > LG TV SSCR2 > Refresh rate. If Variable is offered, select it now, then press Return here, even if TV says No Signal. If unavailable, press Return without changing anything. You have 60 seconds. At the deadline the current state is captured automatically.',60,required=False)
  capture('selected')
  time.sleep(5);capture('settled')
 finally:
  try:recover();restored=True;capture('after')
  finally:
   if restored:guard.terminate();guard.wait(timeout=5)
   else:print('Recovery not fully verified. Independent watchdog remains scheduled. If TV stays dark, unplug USB-C for ten seconds and select a fixed Refresh rate using the built-in display.',flush=True)
