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
CLI='/opt/homebrew/bin/betterdisplaycli'
SELECT='--UUID=0A65EDC5-C030-4BD5-8B0C-3FFE1ECCDE42'
import base64
BIN=HERE/'CAC-Mac-Typ-RAM'
def ram(mode):
 r=subprocess.run([str(BIN),mode],capture_output=True,text=True,timeout=8)
 print(r.stdout+r.stderr,flush=True)
 if r.returncode:raise RuntimeError('RAM operation failed: '+str(r.returncode))

ORIGINAL=(HERE/'LG-Mac-EDID-original.bin').read_bytes()
TEST=(HERE/'LG-Mac-EDID-range48.bin').read_bytes()
def call(op,flag,checked=True):
 r=subprocess.run([CLI,op,SELECT,flag],capture_output=True,text=True,timeout=8)
 print(op,flag.split('=')[0],'exit',r.returncode,flush=True)
 print(r.stdout+r.stderr,flush=True)
 if checked and r.returncode:raise RuntimeError('BetterDisplay operation failed')
 return r

def edid():
 return base64.b64decode(call('get','--osEDID').stdout.strip(),validate=True)
def recover():
 errors=[]
 for attempt in range(3):
  try:
   ram('--restore');break
  except Exception as e:
   if attempt==2:errors.append('RAM restoration: '+str(e))
   else:time.sleep(.5)
 for op,flag in [('set','--autoApplyCustomEDID=off'),('perform','--applyFactoryEDID'),('set','--customEDID')]:
  try:call(op,flag)
  except Exception as e:errors.append(str(e))
 time.sleep(3)
 if edid()!=ORIGINAL:raise RuntimeError('Original OS EDID not confirmed')
 if errors:raise RuntimeError('; '.join(errors))
 print('RESTORED: RAM helper succeeded; original OS EDID verified; custom EDID cleared; auto-apply off.',flush=True)

def capture_cache(phase):
 import plistlib
 r=subprocess.run(['/usr/sbin/ioreg','-r','-c','IOMobileFramebuffer','-a'],capture_output=True,timeout=10)
 (HERE/('CAC-Mac-Timing-'+phase+'.plist')).write_bytes(r.stdout)
 if r.returncode:raise RuntimeError('Registry capture failed')
 tree=plistlib.loads(r.stdout)
 summaries=[]
 def walk(o):
  if isinstance(o,dict):
   attrs=o.get('DisplayAttributes',{})
   if attrs.get('ProductAttributes',{}).get('ProductName')=='LG TV SSCR2':
    entries=[]
    def timings(v):
     if isinstance(v,dict):
      if 'MaximumVariableRefreshRate' in v:entries.append({k:x for k,x in v.items() if isinstance(x,(str,int,bool,float))})
      for x in v.values():timings(x)
     elif isinstance(v,list):
      for x in v:timings(x)
    for key in ('TimingElements','PreferredTimingElements'):timings(o.get(key,[]))
    summaries.append({'attributes':attrs,'timings':entries})
   for v in o.values():
    if isinstance(v,(dict,list)):walk(v)
  elif isinstance(o,list):
   for v in o:walk(v)
 walk(tree)
 (HERE/('CAC-Mac-Timing-'+phase+'.json')).write_text(json.dumps(summaries,indent=2,default=str))
 print('Saved macOS timing snapshot:',phase,'LG matches',len(summaries),flush=True)

def reports():
 for flag in ('--osEDID','--dpcdReport','--refreshRateList','--displayInformation'):
  call('get',flag,False)
if sys.argv[1:]==['--watchdog']:
 time.sleep(150)
 recover()
 sys.exit(0)
if edid()!=ORIGINAL:raise SystemExit('Unexpected original EDID; no changes.')
if call('get','--autoApplyCustomEDID').stdout.strip()!='off':raise SystemExit('Auto-apply enabled; no changes.')
custom=call('get','--customEDID',False)
if custom.returncode==0 and custom.stdout.strip():raise SystemExit('Stored custom EDID exists; no changes.')
assert len(TEST)==len(ORIGINAL)==256
assert TEST[128:]==ORIGINAL[128:]
assert [(i,ORIGINAL[i],TEST[i]) for i in range(256) if ORIGINAL[i]!=TEST[i]]==[(0x18,0x0a,0x0b),(0x5f,0x18,0x30),(0x7f,0xe5,0xcc)]
print('Combined temporary test: RAM217 08->48, RAM25B 0A->02 plus continuous-frequency EDID bit and 48-120 Hz range. No flash write.',flush=True)
ram('--inspect')
capture_cache('before')
if input('Type YES for a 30-second test with automatic EDID restoration: ').strip()!='YES':sys.exit('Cancelled')
def interrupted(*args):raise KeyboardInterrupt
for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(sig,interrupted)
with (HERE/'CAC-Mac-Timing-Watchdog.log').open('w') as log:
 guard=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'--watchdog'],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 restored=False
 try:
  ram('--enable')
  call('set','--customEDID='+base64.b64encode(TEST).decode())
  call('perform','--applyCustomEDID')
  time.sleep(5)
  if edid()!=TEST:raise RuntimeError('Test EDID not adopted by OS')
  print('Test EDID verified. Observe refresh-rate choices and LG picture for 30 seconds.',flush=True)
  capture_cache('during')
  reports()
  time.sleep(30)
 finally:
  try:
   recover();restored=True
   capture_cache("after")
  finally:
   if restored:guard.terminate();guard.wait(timeout=5)
   else:print('Recovery not confirmed; independent watchdog remains scheduled. Use built-in display to restore factory EDID in BetterDisplay.',flush=True)
