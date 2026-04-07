import os, re, glob

PREFIX = '/r21'

def patch_html(content):
    # Fix href/src/as attributes that reference root-local paths, not protocol-relative (//) or external
    return re.sub(r'((?:href|src|as)=")(/)(?!/)', r'\1' + PREFIX + r'\2', content)

def patch_webpack_runtime(content):
    return content.replace('.p="/"', '.p="' + PREFIX + '/"')

def patch_app_js(content):
    content = content.replace('"/page-data/', '"' + PREFIX + '/page-data/')
    return content

changed = []

for f in glob.glob('**/*.html', recursive=True):
    if os.path.isdir(f):
        continue
    orig = open(f, encoding='utf-8').read()
    patched = patch_html(orig)
    if patched != orig:
        open(f, 'w', encoding='utf-8').write(patched)
        changed.append(f)

for f in glob.glob('webpack-runtime-*.js'):
    orig = open(f, encoding='utf-8').read()
    patched = patch_webpack_runtime(orig)
    if patched != orig:
        open(f, 'w', encoding='utf-8').write(patched)
        changed.append(f)

for f in glob.glob('app-*.js'):
    orig = open(f, encoding='utf-8').read()
    patched = patch_app_js(orig)
    if patched != orig:
        open(f, 'w', encoding='utf-8').write(patched)
        changed.append(f)

print(f"Patched {len(changed)} files:")
for f in sorted(changed):
    print(' ', f)
