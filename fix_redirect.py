import glob, re, os

PREFIX = '/r21'
changed = []

# Fix 1: Update window.pagePath in all HTML files to include /r21 prefix
for f in glob.glob('**/*.html', recursive=True):
    if os.path.isdir(f):
        continue
    orig = open(f, encoding='utf-8').read()
    patched = re.sub(
        r'window\.pagePath="(?!/r21)([^"]*)"',
        lambda m: 'window.pagePath="' + PREFIX + m.group(1) + '"',
        orig
    )
    if patched != orig:
        open(f, 'w', encoding='utf-8').write(patched)
        changed.append(f)

# Fix 2: Update pathPrefix getter v() and basePath getter m() in app JS
for f in glob.glob('app-*.js'):
    orig = open(f, encoding='utf-8').read()
    patched = orig.replace(
        'var v=function(){return""},m=function(){return""}',
        'var v=function(){return"/r21"},m=function(){return"/r21"}'
    )
    if patched != orig:
        open(f, 'w', encoding='utf-8').write(patched)
        changed.append(f)

print("Patched %d files:" % len(changed))
for f in sorted(changed):
    print(' ', f)
