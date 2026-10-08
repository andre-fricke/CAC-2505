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
watchdogs=[str(HERE/name) for name in ('CAC-Mac-VRR-Auswahl-Test.py','CAC-Mac-VRR-Modi-Lesen-Test.py','CAC-Mac-VRR-720p-Test.py','CAC-Mac-Nativ720-Lesen-Test.py','CAC-Mac-Nativ720-VRR-Test.py','CAC-Mac-Nativ720-VRR8-Test.py','CAC-Mac-Signal-Diagnose-Test.py')]
r=subprocess.run(['/bin/ps','-axo','pid=,command='],capture_output=True,text=True,check=True,timeout=5)
for line in r.stdout.splitlines():
 parts=line.strip().split(None,1)
 if len(parts)!=2:continue
 pid,command=parts
 if any(path in command for path in watchdogs) and command.rstrip().endswith(' --watchdog'):
  try:
   _log_os.kill(int(pid),signal.SIGTERM)
   print('Stopped pending recovery process:',pid,flush=True)
  except ProcessLookupError:pass
time.sleep(1)
print('Unplug the adapter USB-C from the Mac. Wait ten seconds, then reconnect with HDMI attached.',flush=True)
input('Press Return once reconnected and the picture is back: ')
time.sleep(5)
r=subprocess.run([sys.executable,str(HERE/'CAC-Mac-Cache-Lesen.py')],timeout=180)
sys.exit(r.returncode)
