import re, glob, os

# 1. Webpack runtime: .p="/r21/" -> .p="/"
patched = 0
for path in glob.glob('webpack-runtime-*.js'):
    with open(path) as f:
        content = f.read()
    new = content.replace('.p="/r21/"', '.p="/"')
    if new != content:
        with open(path, 'w') as f:
            f.write(new)
        patched += 1
print("webpack-runtime: %d files" % patched)

# 2. App JS files
app_files = glob.glob('app-*.js')
for path in app_files:
    with open(path) as f:
        content = f.read()
    orig = content

    # a) v/m pathPrefix getters
    content = content.replace(
        'var v=function(){return"/r21"},m=function(){return"/r21"}',
        'var v=function(){return""},m=function(){return""}'
    )

    # b) encodeURI with /r21 prefix
    content = content.replace(
        'encodeURI("/r21"+(r.page.matchPath||r.page.path))',
        'encodeURI(r.page.matchPath||r.page.path)'
    )

    # c) h() function: restore original without r21 strip logic
    content = content.replace(
        'h=function(t){var e,r=t.startsWith("/r21")?t.slice(4)||"/":t;return"/r21/page-data/"+(r==="/"||r===""?"index":e=(e="/"===(e=r)[0]?e.slice(1):e).endsWith("/")?e.slice(0,-1):e)+"/page-data.json',
        'h=function(t){var e;return"/page-data/"+(t==="/"||t===""?"index":e=(e="/"===(e=t)[0]?e.slice(1):e).endsWith("/")?e.slice(0,-1):e)+"/page-data.json'
    )

    # d) remaining /r21/page-data/ refs
    content = content.replace('"/r21/page-data/sq/d/"', '"/page-data/sq/d/"')
    content = content.replace('"/r21/page-data/app-data.json"', '"/page-data/app-data.json"')

    if content != orig:
        with open(path, 'w') as f:
            f.write(content)
        print("  app JS patched: " + path)

print("app JS: %d files processed" % len(app_files))

# 3. HTML files
html_patched = 0
for path in glob.glob('**/*.html', recursive=True):
    if os.path.isdir(path):
        continue
    with open(path) as f:
        content = f.read()
    orig = content

    content = re.sub(r'href="/r21/', 'href="/', content)
    content = re.sub(r'src="/r21/', 'src="/', content)
    content = re.sub(r'as="/r21/', 'as="/', content)
    content = content.replace('url(/r21/static/', 'url(/static/')
    content = re.sub(r'window\.pagePath="/r21([^"]*)"',
                     lambda m: 'window.pagePath="%s"' % (m.group(1) or '/'),
                     content)

    if content != orig:
        with open(path, 'w') as f:
            f.write(content)
        html_patched += 1

print("HTML files: %d patched" % html_patched)

# 4. CSS files
css_patched = 0
for path in glob.glob('**/*.css', recursive=True):
    if os.path.isdir(path):
        continue
    with open(path) as f:
        content = f.read()
    new = content.replace('url(/r21/static/', 'url(/static/')
    if new != content:
        with open(path, 'w') as f:
            f.write(new)
        css_patched += 1
        print("  CSS patched: " + path)

print("CSS files: %d patched" % css_patched)
print("All done.")
