#!/usr/bin/python3
import os,hashlib,shutil,subprocess
from pathlib import Path
src=Path(__file__).resolve().parent;dst=Path('/var/lib/cac2505-vrr')
if os.geteuid()!=0:raise SystemExit('Run with sudo')
if not (dst/'daemon.py').is_file():raise SystemExit('No existing installation')
for line in (src/'SHA256SUMS.txt').read_text().splitlines():
 h,n=line.split('  ',1)
 if Path(n).name!=n or hashlib.sha256((src/n).read_bytes()).hexdigest()!=h:raise SystemExit('Integrity check failed')
subprocess.run(['systemctl','stop','cac2505-vrr.service'],check=True)
for name in ('daemon.py','adapter.py'):
 shutil.copy2(dst/name,dst/(name+'.previous'))
 shutil.copyfile(src/name,dst/name);(dst/name).chmod(0o600);os.chown(dst/name,0,0)
subprocess.run(['systemctl','start','cac2505-vrr.service'],check=True)
print('Updated connection handling. Old daemon backed up; service restarted.')
