import json, re, html, os, sys, markdown
ws = os.path.dirname(os.path.abspath(__file__)); out = sys.argv[1]
src = open(os.path.join(ws, 'ANALYSE_ECRANS.md'), encoding='utf-8').read()
src = src.split('\n', 1)[1]  # drop H1 (rendered in the header)
md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'], extension_configs={'toc': {'toc_depth': '2-3'}})
body = md.convert(src)
# mermaid fence -> native block
body = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', lambda m: '<pre class="mermaid">' + html.unescape(m.group(1)) + '</pre>', body, flags=re.S)
# wireframes after each screen heading
def wire(m):
    name = m.group(2)
    path = os.path.join(ws, 'wireframes', name + '.svg')
    if not os.path.exists(path): return m.group(0)
    svg = open(path, encoding='utf-8').read()
    mm = re.match(r'<svg xmlns="http://www.w3.org/2000/svg" width="(\d+)" height="(\d+)"', svg)
    W, H = mm.group(1), mm.group(2)
    svg = svg.replace(mm.group(0), f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Maquette filaire de {name}"', 1)
    return m.group(0) + f'<figure class="wire" style="max-width:{W}px"><div class="wire-scroll">{svg}</div><figcaption>Maquette filaire de <code>{name}</code>, générée depuis les coordonnées réelles des contrôles (pixels WinDev). Les libellés sont les noms de champs, pas les légendes d\'origine.</figcaption></figure>'
body = re.sub(r'(<h3 id="[^"]+">4\.\d+ (FEN_[^\s<]+)[^<]*</h3>)', wire, body)
body = re.sub(r'<table>', '<div class="tbl"><table>', body).replace('</table>', '</table></div>')
# sidebar
def toc_html(tokens):
    items = []
    for t in tokens:
        label = re.sub(r'^\d+(\.\d+)?\s+', '', t['name'])
        label = re.sub(r'\s+—.*$', '', label) if t['level'] == 3 else label
        sub = toc_html(t['children']) if t.get('children') else ''
        items.append(f'<li><a href="#{t["id"]}">{html.escape(label)}</a>{sub}</li>')
    return '<ul>' + ''.join(items) + '</ul>'
toc = toc_html(md.toc_tokens)
wdw = json.load(open(os.path.join(ws, 'wdw.json'))); seed = json.load(open(os.path.join(ws, 'seed_data.json')))
nctrl = sum(len(w['controls']) for w in wdw.values())
facts = [('11', 'fenêtres'), (str(nctrl), 'contrôles positionnés'), ('6', 'fichiers HFSQL'), ('5', 'relations'), ('6', 'états imprimés'), (f"{len(seed['MACHINE'])}", 'machines décodées'), (f"{len(seed['COMPOSANT']):,}".replace(',', ' '), 'composants décodés')]
facts_html = ''.join(f'<div class="fact"><span class="n">{n}</span><span class="l">{l}</span></div>' for n, l in facts)
page = f'''<title>Écrans WD Gestion de Parc</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
:root {{ --bg:#F2F4F7; --panel:#FFFFFF; --ink:#1B2430; --muted:#5B6675; --line:#D3DAE3; --accent:#0B6E99; --accent-ink:#0B6E99; --accent-soft:#E2EFF6; --amber:#A86400; --code-bg:#E9EDF2; --wire-bg:#FFFFFF; --shadow: 0 1px 2px rgba(20,30,45,.06); }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#11161D; --panel:#181F29; --ink:#E4E9F0; --muted:#98A4B4; --line:#2A3441; --accent:#5FB3D9; --accent-ink:#8CCBE8; --accent-soft:#15303C; --amber:#F0B454; --code-bg:#212A35; --wire-bg:#FFFFFF; --shadow: 0 1px 2px rgba(0,0,0,.4); }} }}
:root[data-theme="dark"] {{ --bg:#11161D; --panel:#181F29; --ink:#E4E9F0; --muted:#98A4B4; --line:#2A3441; --accent:#5FB3D9; --accent-ink:#8CCBE8; --accent-soft:#15303C; --amber:#F0B454; --code-bg:#212A35; --wire-bg:#FFFFFF; --shadow: 0 1px 2px rgba(0,0,0,.4); }}
* {{ box-sizing: border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font-family:"Source Sans 3", "Segoe UI", Roboto, system-ui, sans-serif; font-size:17px; line-height:1.55; -webkit-font-smoothing:antialiased; }}
a {{ color:var(--accent-ink); text-decoration:none; }} a:hover {{ text-decoration:underline; }}
a:focus-visible, button:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
code, pre {{ font-family:"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace; font-size:.86em; }}
code {{ background:var(--code-bg); padding:.08em .35em; border-radius:3px; }}
pre {{ background:var(--code-bg); padding:14px 16px; border-radius:6px; overflow-x:auto; line-height:1.45; }}
pre code {{ background:none; padding:0; }}
header.top {{ border-bottom:1px solid var(--line); background:var(--panel); }}
.top-inner {{ max-width:1280px; margin:0 auto; padding:34px 28px 26px; }}
.eyebrow {{ font-family:"Archivo", sans-serif; text-transform:uppercase; letter-spacing:.12em; font-size:.74rem; font-weight:600; color:var(--accent-ink); margin:0 0 10px; }}
h1 {{ font-family:"Archivo", sans-serif; font-weight:700; font-size:2.05rem; line-height:1.15; margin:0 0 12px; text-wrap:balance; letter-spacing:-.01em; }}
.lede {{ max-width:70ch; margin:0 0 22px; color:var(--muted); font-size:1.08rem; }}
.facts {{ display:flex; flex-wrap:wrap; gap:10px 28px; padding-top:18px; border-top:1px dashed var(--line); }}
.fact {{ display:flex; flex-direction:column; }} .fact .n {{ font-family:"Archivo", sans-serif; font-weight:700; font-size:1.45rem; font-variant-numeric:tabular-nums; line-height:1.1; }} .fact .l {{ font-size:.8rem; color:var(--muted); text-transform:uppercase; letter-spacing:.06em; }}
.page {{ max-width:1280px; margin:0 auto; padding:28px 28px 80px; display:grid; grid-template-columns:250px minmax(0,1fr); gap:44px; align-items:start; }}
nav.side {{ position:sticky; top:16px; max-height:calc(100vh - 32px); overflow:auto; font-size:.9rem; padding-right:6px; }}
nav.side .t {{ font-family:"Archivo", sans-serif; text-transform:uppercase; letter-spacing:.1em; font-size:.7rem; color:var(--muted); margin:0 0 8px; font-weight:600; }}
nav.side ul {{ list-style:none; margin:0; padding:0; }} nav.side > ul > li {{ margin:0 0 6px; }} nav.side > ul > li > a {{ font-weight:600; color:var(--ink); }}
nav.side ul ul {{ margin:4px 0 8px 10px; border-left:1px solid var(--line); padding-left:10px; }} nav.side ul ul a {{ color:var(--muted); }} nav.side a:hover {{ color:var(--accent-ink); text-decoration:none; }}
main {{ min-width:0; }}
main h2 {{ font-family:"Archivo", sans-serif; font-weight:700; font-size:1.55rem; margin:54px 0 14px; padding-top:18px; border-top:1px solid var(--line); text-wrap:balance; }}
main h2:first-child {{ margin-top:0; border-top:0; padding-top:0; }}
main h3 {{ font-family:"Archivo", sans-serif; font-weight:600; font-size:1.18rem; margin:38px 0 10px; text-wrap:balance; }}
main h3 code {{ font-size:.9em; }}
main p, main li {{ max-width:76ch; }} main p {{ margin:0 0 14px; }}
main ul, main ol {{ padding-left:22px; margin:0 0 16px; }} main li {{ margin:4px 0; }}
.tbl {{ overflow-x:auto; margin:12px 0 22px; border:1px solid var(--line); border-radius:6px; background:var(--panel); box-shadow:var(--shadow); }}
table {{ border-collapse:collapse; width:100%; font-size:.92rem; }} th, td {{ text-align:left; vertical-align:top; padding:8px 12px; border-bottom:1px solid var(--line); }}
th {{ font-family:"Archivo", sans-serif; font-weight:600; font-size:.78rem; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); background:var(--code-bg); white-space:nowrap; }}
tr:last-child td {{ border-bottom:0; }} td code {{ white-space:nowrap; }} td {{ font-variant-numeric:tabular-nums; }}
figure.wire {{ margin:16px 0 26px; background:var(--wire-bg); border:1px solid var(--line); border-radius:6px; padding:8px; box-shadow:var(--shadow); }}
.wire-scroll {{ overflow-x:auto; }} figure.wire svg {{ width:100%; height:auto; display:block; min-width:520px; }}
figure.wire figcaption {{ font-size:.82rem; color:#5B6675; padding:8px 6px 2px; }}
pre.mermaid {{ background:var(--panel); border:1px solid var(--line); text-align:center; }}
blockquote {{ margin:0 0 16px; padding:2px 16px; border-left:3px solid var(--accent); color:var(--muted); }}
@media (max-width: 920px) {{ .page {{ grid-template-columns:1fr; gap:24px; }} nav.side {{ position:static; max-height:none; }} nav.side ul ul {{ display:none; }} }}
@media (prefers-reduced-motion: no-preference) {{ html {{ scroll-behavior:smooth; }} }}
</style>
<header class="top"><div class="top-inner">
<p class="eyebrow">Rétro-ingénierie · WinDev 28 → Convertigo NGX</p>
<h1>Écrans de « WD Gestion de parc informatique »</h1>
<p class="lede">Exemple officiel PC SOFT récupéré sur GitHub, décortiqué fenêtre par fenêtre (contrôles, liaisons, règles métier, données de démo) pour être resoumis au MCP Convertigo. Aucun objet Convertigo n'a encore été créé : ce dossier est l'entrée de l'étape suivante.</p>
<div class="facts">{facts_html}</div>
</div></header>
<div class="page">
<nav class="side" aria-label="Sommaire"><p class="t">Sommaire</p>{toc}</nav>
<main>{body}</main>
</div>
'''
open(out, 'w', encoding='utf-8').write(page)
print(out, len(page)//1024, 'KB')
