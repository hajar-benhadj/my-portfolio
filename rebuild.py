"""Rebuild the projects section as vertical name→web→description→web→actions flows."""
import re

src = open('index.html', encoding='utf-8').read()

# ── capture the projects section inner block ──
sec_start = src.index('<div class="projects-grid">')
sec_end = src.index('<!-- Footer -->')
old_block = src[sec_start:sec_end]

# split into per-card chunks
chunks = re.split(r'(?=<div class="project-card")', old_block)
chunks = [c for c in chunks if c.startswith('<div class="project-card"')]
assert len(chunks) == 7, f'expected 7 cards, got {len(chunks)}'

themes = [
    ('#fcd34d', '#e6a23c'),
    ('#34d399', '#059669'),
    ('#38bdf8', '#0072ff'),
    ('#38bdf8', '#0284c7'),
    ('#fde047', '#eab308'),
    ('#22d3ee', '#0e7490'),
    ('#f87171', '#dc2626'),
]

def extract(chunk):
    h3 = re.search(r'<h3>(.*?)</h3>', chunk, re.S).group(1).strip()
    tags = re.findall(r'<span>(.*?)</span>', re.search(r'<div class="project-tags">([\s\S]*?)</div>', chunk).group(1))
    desc = re.search(r'<div class="card-reveal">\s*<p>([\s\S]*?)</p>', chunk).group(1).strip()
    links = [(m.group(1), 'ghost' if 'ghost' in m.group(0) else '', m.group(2))
             for m in re.finditer(r'<a href="([^"]+)"[^>]*class="p-btn[^"]*"[^>]*>([\s\S]*?)</a>', chunk)]
    return h3, tags, desc, links

def web_svg():
    return '''<div class="flow-web" aria-hidden="true">
                    <svg viewBox="0 0 110 150" preserveAspectRatio="xMidYMid meet">
                        <path class="strand" d="M0 75 C 40 75, 70 75, 110 75"/>
                        <path class="strand slow" d="M0 75 C 38 42, 72 38, 110 58"/>
                        <path class="strand slow" d="M0 75 C 38 108, 72 112, 110 92"/>
                        <circle class="node-dot" cx="55" cy="74" r="3.2"/>
                        <circle class="dew d1" cx="30" cy="56" r="2.2"/>
                        <circle class="dew d2" cx="82" cy="94" r="2.2"/>
                    </svg>
                </div>'''

flows = []
for i, chunk in enumerate(chunks):
    pa1, pa2 = themes[i % len(themes)]
    h3, tags, desc, links = extract(chunk)

    if '—' in h3:
        name, sub = [p.strip() for p in h3.split('—', 1)]
    else:
        name, sub = h3.strip(), ''

    tag_html = ''.join(f'<li>{t}</li>' for t in tags)
    links_html = ''.join(
        f'<a href="{href}" target="_blank" class="p-btn{" ghost" if "ghost" in cls else ""}" '
        f'style="--pa1: {pa1}; --pa2: {pa2};">{label.strip()} <span class="arr">→</span></a>'
        for href, cls, label in links
    )

    sub_html = f'<p class="flow-sub">{sub}</p>' if sub else ''
    flows.append(f'''        <div class="project-flow" style="--pa1: {pa1}; --pa2: {pa2};">
            <div class="flow-node node-name reveal">
                <span class="flow-index">{i + 1:02d}</span>
                <h3>{name}</h3>
                {sub_html}
                <ul class="flow-tags">{tag_html}</ul>
            </div>
            {web_svg()}
            <div class="flow-node node-desc reveal">
                <p>{desc}</p>
            </div>
            {web_svg()}
            <div class="flow-node node-actions reveal">
                {links_html}
            </div>
        </div>''')

new_section_inner = '\n'.join(flows) + '\n'

src = src[:sec_start] + new_section_inner + src[sec_end:]
open('index.html', 'w', encoding='utf-8').write(src)
print(f'rebuilt {len(flows)} project flows')
