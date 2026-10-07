#!/usr/bin/python3
import os,sys,hashlib,shutil,subprocess
from pathlib import Path
src=Path(__file__).resolve().parent
dst=Path('/var/lib/cac2505-vrr');unit=Path('/etc/systemd/system/cac2505-vrr.service')
def run(*args):subprocess.run(args,check=True)
if os.geteuid()!=0:raise SystemExit('Run sudo python3 install.py [--remove]')
if sys.argv[1:]==['--remove']:
 run('systemctl','disable','--now','cac2505-vrr.service')
 unit.unlink(missing_ok=True);run('systemctl','daemon-reload')
 print('Service removed. Helper files retained under /var/lib/cac2505-vrr for inspection.');sys.exit(0)
if sys.argv[1:]:raise SystemExit('Unknown arguments')
if unit.exists() or dst.exists():raise SystemExit('Existing installation found; refusing to overwrite')
for line in (src/'SHA256SUMS.txt').read_text().splitlines():
 digest,name=line.split('  ',1)
 if Path(name).name!=name:raise SystemExit('Invalid manifest path')
 if hashlib.sha256((src/name).read_bytes()).hexdigest()!=digest:raise SystemExit('Package integrity failed: '+name)
# Fail before installation if the runtime prerequisites are missing.
try:
 import hid
except ImportError:
 raise SystemExit('Missing Python hid module (distribution: hidapi); see README.md')
for executable in ('kscreen-doctor','gamescopectl'):
 if shutil.which(executable) is None:raise SystemExit('Missing prerequisite: '+executable)
if not Path('/sys/kernel/debug/dri/0/DP-1/trigger_hotplug').exists():
 raise SystemExit('Missing DP-1 trigger_hotplug interface; see README.md')
print('Install automatic volatile VRR helper for CAC-2505 firmware7.02.116 and LG TV. No flash or driver changes.')
if input('Type YES to install and enable at boot: ').strip()!='YES':sys.exit('Cancelled')
dst.mkdir(mode=0o700)
for name in ('daemon.py','adapter.py'):
 target=dst/name;shutil.copyfile(src/name,target);target.chmod(0o600);os.chown(target,0,0)
shutil.copyfile(src/'cac2505-vrr.service',unit);unit.chmod(0o644);os.chown(unit,0,0)
run('systemd-analyze','verify',str(unit))
run('systemctl','daemon-reload');run('systemctl','enable','--now','cac2505-vrr.service')
print('Installed. Logs: journalctl -u cac2505-vrr.service. Remove with this installer --remove.')
