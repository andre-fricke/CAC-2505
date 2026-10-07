#!/usr/bin/python3
"""Temporary two-byte RAM test. No source VRR forcing, flash, or reconnect commands."""
import subprocess,sys,time,signal,plistlib,hashlib
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
BIN=HERE/'CAC-Mac-Typ-RAM'
CLI='/opt/homebrew/bin/betterdisplaycli'
def invoke(mode):
 r=subprocess.run([str(BIN),mode],capture_output=True,text=True,timeout=5)
 print(r.stdout, end='',flush=True)
 if r.stderr:print(r.stderr,end='',flush=True)
 if r.returncode:raise RuntimeError('RAM operation failed: '+str(r.returncode))
def reinitialize():
 r=subprocess.run([CLI,'perform','--nameLike=LG','--reinitialize'],capture_output=True,text=True,timeout=6)
 print('Reinitialize exit',r.returncode,flush=True)
 print(r.stdout+r.stderr,flush=True)
 if r.returncode:raise RuntimeError('Display reinitialization command failed')
 time.sleep(3)
def restore():
 for attempt in range(3):
  try:invoke('--restore');return
  except Exception:
   if attempt==2:raise
   time.sleep(.5)
def cached_attributes():
 try:
  r=subprocess.run(['/usr/sbin/ioreg','-r','-c','IOMobileFramebuffer','-a'],capture_output=True,timeout=5)
  if r.returncode:raise RuntimeError('ioreg failed')
  def visit(obj):
   if isinstance(obj,dict):
    attrs=obj.get('DisplayAttributes',{})
    if attrs.get('ProductAttributes',{}).get('ProductName')=='LG TV SSCR2':
     print('macOS cached LG SupportsVariableRefreshRate:',attrs.get('SupportsVariableRefreshRate'),flush=True)
    for value in obj.values():visit(value)
   elif isinstance(obj,list):
    for value in obj:visit(value)
  visit(plistlib.loads(r.stdout))
 except Exception as e:print('Cached attribute query:',repr(e),flush=True)
edid_index=0
def transport_edid():
 global edid_index
 edid_index+=1
 try:
  r=subprocess.run(['/usr/sbin/ioreg','-r','-c','IOPortTransportStateDisplayPort','-a'],capture_output=True,timeout=5)
  if r.returncode:raise RuntimeError('Transport query failed')
  def visit(obj):
   if isinstance(obj,dict):
    if obj.get('BranchDeviceID')=='SYNAq' and obj.get('Active') is True:
     e=obj.get('EDID')
     if isinstance(e,bytes) and len(e)>=128:
      name='CAC-Mac-EDID-snapshot-'+str(edid_index)+'.bin'
      (HERE/name).write_bytes(e)
      print('MAC EDID:',name,'length',len(e),'SHA256',hashlib.sha256(e).hexdigest(),'version/input',e[18:21].hex(' '),'checksums',[sum(e[i:i+128])%256 for i in range(0,len(e),128)],flush=True)
      for i in range(54,126,18):
       d=e[i:i+18]
       if d[:3]==b'\0\0\0':print('EDID descriptor:',hex(i),d.hex(' '),flush=True)
    for value in obj.values():visit(value)
   elif isinstance(obj,list):
    for value in obj:visit(value)
  visit(plistlib.loads(r.stdout))
 except Exception as e:print('EDID query:',repr(e),flush=True)
def reports():
 transport_edid()
 cached_attributes()
 for flag in ('dpcdReport','refreshRateList'):
  try:
   r=subprocess.run([CLI,'get','--nameLike=LG','--'+flag],capture_output=True,text=True,timeout=4)
   print(flag,'exit',r.returncode,flush=True);print(r.stdout+r.stderr,flush=True)
  except subprocess.TimeoutExpired:print(flag,'timed out',flush=True)
def interrupted(*args):raise KeyboardInterrupt
if sys.argv[1:]==['--watchdog']:
 time.sleep(120);restore();print('Independent RAM restoration verified.',flush=True);reinitialize();sys.exit(0)
for sig in (signal.SIGINT,signal.SIGTERM,signal.SIGHUP):signal.signal(sig,interrupted)
print('Mac temporary RAM217 08->48, RAM25B 0A->02. Automatic RAM restoration. No DCP forcing.',flush=True)
invoke('--inspect')
reports()
if input('Type JA to test with automatic display reinitialization and 20-second observation; picture may disappear: ').strip()!='JA':sys.exit('Cancelled; no RAM write.')
with (HERE/'CAC-Mac-EDID-Watchdog.txt').open('w') as log:
 guard=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),'--watchdog'],stdout=log,stderr=subprocess.STDOUT,start_new_session=True)
 restored=False
 try:
  invoke('--enable')
  reports()
  print('Reinitializing only the LG connection; brief black picture possible.',flush=True)
  reinitialize()
  invoke('--inspect')
  reports()
  print('20-second observation: check System Settings > Displays > Refresh rate. Leave cables connected.',flush=True)
  time.sleep(20)
 finally:
  print('Restoring original RAM bytes.',flush=True)
  try:
   restore()
   reinitialize()
   restored=True
   print('RESTORED: RAM217=08, RAM25B=0A verified.',flush=True)
  except Exception as e:
   print('Restoration not confirmed:',repr(e),flush=True)
   print('Independent retry remains scheduled. If picture does not recover, unplug USB-C for 10 seconds.',flush=True)
  if restored and guard.poll() is None:guard.terminate();guard.wait(timeout=3)
reports()
