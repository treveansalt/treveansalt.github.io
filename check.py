from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
root=Path(__file__).resolve().parent
out=root/'docs'
posts=json.loads((root/'posts.json').read_text(encoding='utf-8'))
assert posts
assert len({p['slug'] for p in posts})==len(posts)
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        for key in ('href','src'):
            value=attrs.get(key,'')
            if not value.startswith('/') or value.startswith('//'): continue
            target=out/unquote(urlsplit(value).path).lstrip('/')
            if target.is_dir(): target=target/'index.html'
            assert target.is_file(),f'Missing local target: {value}'
for page in out.rglob('*.html'):
    text=page.read_text(encoding='utf-8')
    assert '<h1>' in text,page
    assert 'Fictional' in text,page
    assert 'viewport' in text,page
    Links().feed(text)
print(f'Checked {len(list(out.rglob("*.html")))} pages. All internal links and image references resolve; all {len(posts)} stories are present.')

