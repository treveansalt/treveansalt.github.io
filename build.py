import json, html, re, shutil
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'docs'
ASSETS = OUT / 'images'
SOURCE = ROOT.parent / 'output' / 'pannier-papers'
ASSETS.mkdir(parents=True, exist_ok=True)
posts = json.loads((ROOT / 'posts.json').read_text(encoding='utf-8'))
E = lambda text: html.escape(str(text), quote=True)
favicon = 'data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Crect width=%2264%22 height=%2264%22 rx=%2212%22 fill=%22%23f4511e%22/%3E%3Ctext x=%2232%22 y=%2246%22 text-anchor=%22middle%22 font-family=%22Arial%22 font-weight=%22900%22 font-size=%2245%22 fill=%22white%22%3ER%3C/text%3E%3C/svg%3E'

def image_name(name):
    return Path(name).stem + '.webp'

for p in posts:
    for name in p['images']:
        dest = ASSETS / image_name(name)
        if not dest.exists():
            with Image.open(SOURCE / name) as im:
                im.convert('RGB').save(dest, 'WEBP', quality=85, method=6)
                im.thumbnail((720, 540))
                im.convert('RGB').save(ASSETS / ('small-' + image_name(name)), 'WEBP', quality=80, method=6)

def photo(p, index=0, eager=False, small=False):
    name = image_name(p['images'][index])
    alt = p.get('alts', [p['title']]*len(p['images']))[index]
    return f'<img src="/images/{"small-" if small else ""}{name}" alt="{E(alt)}" width="1448" height="1086" loading="{"eager" if eager else "lazy"}" decoding="async">'

def url(p): return '/stories/' + p['slug'] + '/'
def minutes(p): return max(1, round(len(p['body'].split()) / 220))
def meta(p): return f'<span>{E(p["category"])}</span><span>{minutes(p)} min read</span>'

def shell(title, description, body, current=''):
    return f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} | Real Adventure Riders</title><meta name="description" content="{E(description)}"><meta name="theme-color" content="#f4511e"><link rel="icon" type="image/svg+xml" href="{favicon}"><link rel="stylesheet" href="/style.css"><script async src="https://www.googletagmanager.com/gtag/js?id=G-QD3K2L24N7"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("js",new Date());gtag("config","G-QD3K2L24N7");</script></head><body>
<a class="skip" href="#main">Skip to content</a><div class="notice">ADVENTURE MOTORCYCLING SATIRE <span>Fictional stories. AI-generated photos.</span></div>
<header class="header"><a href="/" class="brand" aria-label="Real Adventure Riders home"><span class="brand-icon">R<span>!</span></span><span>REAL ADVENTURE<br>RIDERS<span class="brand-dot">.</span></span></a><nav aria-label="Main navigation"><a href="/" {'aria-current="page"' if current=='home' else ''}>Latest stories</a><a href="/#archive">The archive</a><a href="/about/" {'aria-current="page"' if current=='about' else ''}>About the nonsense</a></nav></header>
{body}<footer><a class="footer-brand" href="/">REAL ADVENTURE RIDERS.</a><p>All the gear. Questionable ideas.</p><div class="footer-bottom"><span>Fictional riders, fictional disasters. Very real enthusiasm.</span><a href="/about/">Satire &amp; AI disclosure</a><a href="/#archive">All stories</a></div><p class="fine">An independent satire blog. Not affiliated with the Trans Euro Trail, motorcycle manufacturers or any real rider. The stories are entertainment, not riding or repair advice.</p></footer></body></html>'''

def card(p, compact=False):
    return f'<article class="card {"compact" if compact else ""}"><a class="card-image" href="{url(p)}" tabindex="-1" aria-hidden="true">{photo(p,small=True)}</a><div class="card-copy"><div class="meta">{meta(p)}</div><h3><a href="{url(p)}">{E(p["title"])}</a></h3><p>{E(p["excerpt"])}</p><a class="read" href="{url(p)}">Read the story<span class="sr">: {E(p["title"])}</span></a></div></article>'

if posts:
    lead = posts[-1]
    supporting = list(reversed(posts[:-1]))[:2]
    hero = f'''<main id="main"><section class="intro"><div><p class="eyebrow">THE PANNIER PAPERS</p><h1>All the gear.<br><span>Questionable ideas.</span></h1></div><p>Dispatches from riders who packed everything except common sense.</p></section>
    <section class="lead-grid" aria-label="Featured stories"><article class="lead"><a href="{url(lead)}" class="lead-image" tabindex="-1" aria-hidden="true">{photo(lead,eager=True)}<span class="image-stamp">THE LATEST MISADVENTURE</span></a><div class="lead-copy"><div class="meta">{meta(lead)}</div><h2><a href="{url(lead)}">{E(lead['title'])}</a></h2><p>{E(lead['excerpt'])}</p><a class="button" href="{url(lead)}">Read the story</a></div></article><div class="side-stories">{''.join(card(p,True) for p in supporting)}</div></section>
    <section class="archive" id="archive"><div class="section-heading"><h2>The complete lack of preparation.</h2><span>{len(posts):02d} STORIES &amp; COUNTING</span></div><div class="cards">{''.join(card(p) for p in reversed(posts))}</div></section></main>'''
    (OUT/'index.html').write_text(shell('All the gear. Questionable ideas.', 'A satirical adventure motorcycle blog about big bikes, bad planning and very confident people. Read The Pannier Papers.', hero, 'home'), encoding='utf-8')

for i,p in enumerate(posts):
    paragraphs = []
    for para in p['body'].strip().split('\n\n'):
        text = E(para).replace('\n','<br>')
        if para.startswith('EDIT'):
            text = re.sub(r'^(EDIT(?: \d+)?:)',r'<strong>\1</strong>',text)
        paragraphs.append(f'<p>{text}</p>')
    gallery = ''.join(f'<figure class="extra-photo">{photo(p,n)}<figcaption>From the same entirely fictional expedition. AI-generated image.</figcaption></figure>' for n in range(1,len(p['images'])))
    related = [x for x in reversed(posts) if x!=p][:3]
    body = f'''<main id="main"><article class="story"><a class="back" href="/#archive">All stories</a><header class="story-heading"><div class="meta">{meta(p)}<span>THE PANNIER PAPERS · NO. {i+1:02d}</span></div><h1>{E(p['title'])}</h1><p class="dek">{E(p['excerpt'])}</p></header><figure class="story-photo">{photo(p,eager=True)}<figcaption>Fictional scene. AI-generated image.</figcaption></figure><div class="story-body">{''.join(paragraphs)}<div class="story-disclosure">The Pannier Papers. Fictional story and AI-generated photography.</div></div>{gallery}</article><section class="related"><div class="section-heading"><h2>More questionable decisions.</h2><a href="/#archive">Browse the archive</a></div><div class="cards">{''.join(card(x) for x in related)}</div></section></main>'''
    folder = OUT/'stories'/p['slug']; folder.mkdir(parents=True,exist_ok=True)
    (folder/'index.html').write_text(shell(p['title'],p['excerpt'],body),encoding='utf-8')

about = '''<main id="main" class="about"><p class="eyebrow">ABOUT THE NONSENSE</p><h1>Very serious bikes.<br>Entirely unserious stories.</h1><div class="about-copy"><p>Real Adventure Riders is the home of The Pannier Papers: a collection of fictional posts inspired by the familiar chaos of adventure motorcycling groups.</p><p>These posts are satire. The riders, disasters and requests for help are made up.</p><p>AI is used extensively to write the nonsense and create the photos. No actual rider has been caught charging a Zero with a solar-powered drinks coaster.</p><p>It’s a piss-take of poor planning, expensive kit and misplaced confidence. If you recognise yourself, that’s probably coincidence. Probably.</p><h2>A note about the photos</h2><p>The images are AI-generated illustrations, not photographs of real incidents. The people are fictional. Recognisable motorcycles and equipment are props in invented stories, not evidence of product faults or endorsements.</p><h2>And the advice?</h2><p>Please don’t take it. These characters aren’t qualified to give it. This is entertainment, not a guide to riding, repairs, navigation or personal safety.</p><p>We’re independent and not affiliated with the Trans Euro Trail, any motorcycle manufacturer or any real rider or influencer.</p><a class="button" href="/#archive">Read the stories</a></div></main>'''
(OUT/'about').mkdir(exist_ok=True)
(OUT/'about'/'index.html').write_text(shell('About the nonsense','What is Real Adventure Riders? A note on our fictional stories, satire and AI-generated images.',about,'about'),encoding='utf-8')
(OUT/'404.html').write_text(shell('Wrong turn','This trail does not exist.', '<main id="main" class="about"><p class="eyebrow">404 · ANOTHER NAVIGATION INCIDENT</p><h1>You’ve taken a wrong turn.</h1><p>This page isn’t on the route.</p><a class="button" href="/">Back to the stories</a></main>'),encoding='utf-8')
shutil.copyfile(ROOT/'style.css',OUT/'style.css')
(OUT/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n/images/*\n  Cache-Control: public, max-age=86400\n',encoding='utf-8')
print(f'Built {len(posts)} stories, home, about and 404. Images: {len(list(ASSETS.glob("*.webp")))}')

