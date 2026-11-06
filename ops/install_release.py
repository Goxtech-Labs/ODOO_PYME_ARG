from pathlib import Path
import argparse,hashlib,tarfile,subprocess,os,json
parser=argparse.ArgumentParser(description='Install the exact owned-addon package and selected modules.')
parser.add_argument('archive',type=Path);parser.add_argument('sha');parser.add_argument('modules',nargs='+')
parser.add_argument('--keep-stopped',action='store_true',help='Keep Odoo stopped for technical readback before controlled startup.')
options=parser.parse_args();archive=options.archive;sha=options.sha;modules=options.modules
assert hashlib.sha256(archive.read_bytes()).hexdigest()==sha
assert modules and all(x.startswith('arg_pyme_') and x.replace('_','').isalnum() for x in modules)
root=Path('/opt/arg/releases')/sha[:16];root.mkdir(parents=True,exist_ok=True)
with tarfile.open(archive) as t:
 for item in t.getmembers():
  p=Path(item.name)
  if p.is_absolute() or '..' in p.parts or item.issym() or item.islnk():raise ValueError('Unsafe release member')
 t.extractall(root,filter='data')
for p in root.rglob('*'):
 if p.is_dir():p.chmod(0o755)
 else:
  p.chmod(0o644)
  # Odoo bundle versions include source mtime. Tar is reproducible (mtime=0), runtime cache must see this release.
  os.utime(p,None)
current=Path('/opt/arg/current');previous=os.readlink(current) if current.is_symlink() else None
cfg=Path('/etc/odoo/odoo.conf');text=cfg.read_text()
lines=[s for s in text.splitlines() if not s.startswith('addons_path')]
lines.append('addons_path = /opt/arg/current/addons,/usr/lib/python3/dist-packages/odoo/addons')
subprocess.run(['systemctl','stop','odoo'],check=True)
successful=False
try:
 new=Path('/opt/arg/current.next')
 if new.is_symlink():new.unlink()
 new.symlink_to(root);new.replace(current)
 cfg.write_text('\n'.join(lines)+'\n')
 raw=subprocess.check_output(['runuser','-u','postgres','--','psql','-d','arg_demo','-At','-c',"select name from ir_module_module where state='installed'"],text=True)
 installed=set(raw.splitlines());initial=[m for m in modules if m not in installed];upgrade=[m for m in modules if m in installed]
 cmd=['runuser','-u','odoo','--','odoo','server','-c',str(cfg),'-d','arg_demo','--stop-after-init','--without-demo=True','--workers=0','--max-cron-threads=0','--no-http']
 if initial:cmd+=['--init='+','.join(initial)]
 if upgrade:cmd+=['--update='+','.join(upgrade)]
 result=subprocess.run(cmd,cwd='/var/lib/odoo',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
 log=Path('/var/log/arg-install-'+sha[:16]+'.log');log.write_text(result.stdout);log.chmod(0o600)
 if result.returncode:
  print('INSTALL FAILED:',log,'Exit',result.returncode)
  print(result.stdout[-2000:])
  tail=subprocess.check_output(['tail','-65','/var/log/odoo/odoo-server.log'],text=True);print(tail)
  raise SystemExit(result.returncode)
 successful=True
finally:
 # Failed upgrades remain stopped. Starting a partial registry would expose inconsistent code/schema.
 if successful and not options.keep_stopped:subprocess.run(['systemctl','start','odoo'],check=True)
print(json.dumps({'release_sha256':sha,'modules':modules,'installed':True,
                 'previous_release':previous,'odoo_started':not options.keep_stopped}))
