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
import plistlib,datetime
stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
folder=HERE/('CAC-Mac-Cache-'+stamp);folder.mkdir()
CLI='/opt/homebrew/bin/betterdisplaycli'
selector='--UUID=0A65EDC5-C030-4BD5-8B0C-3FFE1ECCDE42'
results={}
for feature in ('customEDID','autoApplyCustomEDID','osEDID','i2cEDID','displayInformation','connectionModeListAll','dpcdReport'):
 print('Read-only:',feature,flush=True)
 try:
  r=subprocess.run([CLI,'get',selector,'--'+feature],capture_output=True,text=True,timeout=12)
  results[feature]={'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
  (folder/(feature+'.txt')).write_text(r.stdout+r.stderr)
  print('Exit:',r.returncode,flush=True)
 except subprocess.TimeoutExpired:results[feature]={'timeout':True}
for cls in ('IOMobileFramebuffer','IOPortTransportStateDisplayPort','DCPAVServiceProxy'):
 print('Read-only registry:',cls,flush=True)
 try:
  r=subprocess.run(['/usr/sbin/ioreg','-r','-c',cls,'-a'],capture_output=True,timeout=12)
  (folder/(cls+'.plist')).write_bytes(r.stdout)
  results[cls]={'exit':r.returncode,'bytes':len(r.stdout),'stderr':r.stderr.decode(errors='replace')}
  print('Exit:',r.returncode,'bytes:',len(r.stdout),flush=True)
  try:
   tree=plistlib.loads(r.stdout)
   summaries=[]
   def walk(o,path=''):
    if isinstance(o,dict):
     name=o.get('IORegistryEntryName','')
     path=path+'/'+str(name) if name else path
     for k,v in o.items():
      if any(t in k.lower() for t in ('dpcd','adaptivesync','variablerefresh','continuousfrequency','branchdevice','edid','linkrate','lanecount')):
       if isinstance(v,bytes):value={'length':len(v),'hex':v[:256].hex(),'sha256':hashlib.sha256(v).hexdigest()}
       elif isinstance(v,(str,int,float,bool)) or v is None:value=v
       else:value=str(v)[:1000]
       summaries.append({'path':path,'key':k,'value':value})
      if isinstance(v,(dict,list)):walk(v,path+'/'+k)
    elif isinstance(o,list):
     for v in o:walk(v,path)
   walk(tree)
   (folder/(cls+'-summary.json')).write_text(json.dumps(summaries,indent=2))
   print('Relevant properties:',len(summaries),flush=True)
  except Exception as e:print('Registry parse:',str(e),flush=True)
 except subprocess.TimeoutExpired:results[cls]={'timeout':True}
r=subprocess.run([str(HERE/'CAC-Mac-Typ-RAM'),'--inspect'],capture_output=True,text=True,timeout=8)
(folder/'RAM-inspect.txt').write_text(r.stdout+r.stderr)
results['RAM-inspect']={'exit':r.returncode}
(folder/'results.json').write_text(json.dumps(results,indent=2))
(HERE/'CAC-Mac-Cache-latest-path.txt').write_text(str(folder))
print('Read-only capture saved:',folder,flush=True)
print('No RAM, EDID or display settings changed.',flush=True)
