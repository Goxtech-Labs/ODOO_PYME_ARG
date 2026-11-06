"""Package owned addons with syntax controls and a redacted secret scan (no business QA)."""
import argparse, ast, csv, gzip, hashlib, io, json, os, shutil, subprocess, tarfile
from pathlib import Path
from lxml import etree

parser=argparse.ArgumentParser()
parser.add_argument('output',type=Path)
parser.add_argument('--gitleaks',default=os.environ.get('ARG_GITLEAKS') or shutil.which('gitleaks'))
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
source=root/'addons'
if not source.is_dir():raise SystemExit('Run the versioned helper from ops/package_release.py')
if not args.gitleaks:raise SystemExit('Provide an installed Gitleaks via --gitleaks or ARG_GITLEAKS')
for manifest_path in source.glob('*/__manifest__.py'):
 module=manifest_path.parent
 definition=ast.literal_eval(manifest_path.read_text())
 for relative in definition.get('data',[])+definition.get('demo',[]):
  if not (module/relative).is_file():raise SystemExit('Missing manifest input: '+module.name+'/'+relative)
 for bundle in definition.get('assets',{}).values():
  for item in bundle:
   if isinstance(item,str) and item.startswith(module.name+'/') and not list(source.glob(item)):
    raise SystemExit('Missing asset input: '+item)
 for dependency in definition.get('depends',[]):
  if dependency.startswith('arg_pyme_') and not (source/dependency/'__manifest__.py').is_file():
   raise SystemExit('Missing ARG dependency: '+dependency)
files=sorted(p for p in source.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
for path in files:
 if path.is_symlink():raise SystemExit('Symlinks are not valid release inputs')
 if path.suffix=='.py':ast.parse(path.read_text())
 if path.suffix=='.xml':etree.fromstring(path.read_bytes())
 if path.suffix=='.js':subprocess.run(['node','--input-type=module','--check'],input=path.read_text(),text=True,check=True)
 if path.name=='ir.access.csv':
  # Odoo20 CRUD_SELECTION uses canonical c/r/u/d order (e.g. cr, never rc).
  with path.open(newline='') as access_file:
   reader=csv.DictReader(access_file)
   if not reader.fieldnames or 'operation' not in reader.fieldnames:
    raise SystemExit('Missing Odoo20 operation column: '+str(path.relative_to(root)))
   for line,row in enumerate(reader,start=2):
    operation=row.get('operation','')
    if None in row or not operation or operation!=''.join(letter for letter in 'crud' if letter in operation):
     raise SystemExit('Invalid Odoo20 access operation: '+str(path.relative_to(root))+':'+str(line))
args.output.parent.mkdir(parents=True,exist_ok=True)
scan=args.output.with_suffix('.gitleaks.json')
subprocess.run([args.gitleaks,'dir',str(source),'--redact','--no-banner','--exit-code','2','--report-format','json','--report-path',str(scan)],check=True)
manifest={}
with args.output.open('wb') as stream:
 with gzip.GzipFile(filename='',fileobj=stream,mode='wb',mtime=0) as compressed:
  with tarfile.open(fileobj=compressed,mode='w') as archive:
   for path in files:
    raw=path.read_bytes();name=str(path.relative_to(root));manifest[name]=hashlib.sha256(raw).hexdigest()
    info=tarfile.TarInfo(name);info.size=len(raw);info.mode=0o644;info.mtime=0
    archive.addfile(info,io.BytesIO(raw))
receipt={'archive_sha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),'file_sha256':manifest,'gitleaks_findings':0,'syntax_checked':True,'business_qa':False}
args.output.with_suffix('.receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'archive':str(args.output),'sha256':receipt['archive_sha256'],'files':len(files)}))
