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
results={}
for feature in ('displayModeList','displayModeNumber','hiDPI','hdr','protectResolution','protectRefreshRate','protectHDR','connectionModeList','displayInformation'):
 print('=== Read-only',feature,'===',flush=True)
 try:
  r=subprocess.run([CLI,'get','--nameLike=LG','--'+feature],capture_output=True,text=True,timeout=8)
  results[feature]=dict(exit=r.returncode,stdout=r.stdout,stderr=r.stderr)
  print('Exit:',r.returncode,flush=True);print(r.stdout+r.stderr,flush=True)
 except subprocess.TimeoutExpired:
  results[feature]=dict(timeout=True);print('Timed out; no changes.',flush=True)
(HERE/'CAC-Mac-Modi.json').write_text(json.dumps(results,indent=2))
print('Read-only configuration capture complete; no RAM, EDID or display settings changed.',flush=True)
