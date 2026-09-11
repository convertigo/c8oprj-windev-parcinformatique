import json, os, html, sys
d = json.load(open(sys.argv[1])); outdir = sys.argv[2]; os.makedirs(outdir, exist_ok=True)
KIND = {2:'EDIT',3:'STATIC',4:'BUTTON',7:'LIST',8:'IMAGE',9:'TABLE',14:'COMBO',16:'TAB',27:'LISTVIEW'}
FILL = {'EDIT':'#ffffff','STATIC':'#f3f3f3','BUTTON':'#ffd9a0','LIST':'#e6f4e6','LISTVIEW':'#e6f4e6','IMAGE':'#ece3fb','TABLE':'#dff3ee','COMBO':'#fff3c4','TAB':'#fbfbfb'}
STROKE = {'EDIT':'#2f6fd6','STATIC':'#999999','BUTTON':'#c77d00','LIST':'#2e8b3d','LISTVIEW':'#2e8b3d','IMAGE':'#7a48c9','TABLE':'#0f8a6f','COMBO':'#b58a00','TAB':'#666666'}
TABNAMES = {'FEN_Machine': {1: 'Machine', 2: 'Composants'}}
PREFIX = ('SAI_','LIB_','BTN_','TABLE_','COMBO_','ONG_','IMG_','LISTE_','LSI_','COL_','OPT_')
def label(name):
    for p in PREFIX:
        if name.startswith(p): return name[len(p):].replace('_',' ')
    return name
def esc(s): return html.escape(str(s))
def text(x, y, s, size=10, anchor='start', weight='normal', fill='#222', style='normal'):
    return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" font-style="{style}" fill="{fill}">{esc(s)}</text>'
def clip(s, w, size=10):
    n = max(1, int(w / (size*0.55)));  return s if len(s) <= n else s[:max(1,n-1)] + '…'
for win, w in d.items():
    W, H = w['properties']['width'], w['properties']['height']
    ctrls = [c for c in w['controls'] if c['type'] in KIND and (c['y'] or 0) >= 0]
    tabs = [c for c in ctrls if c['type'] == 16]
    pages = [None]
    if tabs:
        t = tabs[0]; n = max([int(c['parent'].split('[')[1][:-1]) for c in ctrls if c['parent'] and c['parent'].startswith(t['name']+'[')] + [1])
        pages = list(range(1, n+1))
    menu_h = 22 if w['menu'] else 0
    fw, fh = W + 2, H + 26 + menu_h
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{len(pages)*(fw+24)+24}" height="{fh+70}" font-family="Helvetica, Arial, sans-serif">',
           '<rect width="100%" height="100%" fill="#ffffff"/>']
    for pi, page in enumerate(pages):
        ox, oy = 24 + pi*(fw+24), 40
        title = w['name'] + (f'  — onglet {page}' if page else '')
        out.append(f'<rect x="{ox}" y="{oy}" width="{fw}" height="{fh}" fill="#f7f7f7" stroke="#333" stroke-width="1.5"/>')
        out.append(f'<rect x="{ox}" y="{oy}" width="{fw}" height="24" fill="#3b4a5a"/>' + text(ox+8, oy+16, title, 12, weight='bold', fill='#fff') + text(ox+fw-8, oy+16, f'{W}×{H}', 10, anchor='end', fill='#dde'))
        if menu_h:
            out.append(f'<rect x="{ox}" y="{oy+24}" width="{fw}" height="{menu_h}" fill="#e9e9e9" stroke="#bbb"/>')
            mx = ox + 10
            for m in w['menu']:
                if m['depth'] == 1:
                    s = label(m['name']); out.append(text(mx, oy+24+15, s, 10)); mx += len(s)*6 + 18
                elif m['depth'] == 0:
                    s = label(m['name']) + ' ▾'; out.append(text(mx, oy+24+15, s, 10, weight='bold')); mx += len(s)*6 + 18
        bx, by = ox + 1, oy + 25 + menu_h   # client origin
        def abs_xy(c):
            p = c['parent']
            if p and '[' in p:
                tname, idx = p.split('['); idx = int(idx[:-1])
                if idx != page: return None
                return bx + tabs[0]['x'] + 2 + c['x'], by + tabs[0]['y'] + 26 + c['y']
            return bx + c['x'], by + c['y']
        for c in sorted(ctrls, key=lambda c: (c['type'] != 16, c['type'] != 3, c['y'])):
            k = KIND[c['type']]; pos = abs_xy(c)
            if pos is None: continue
            x, y = pos; cw, ch = c['w'], c['h']; nm = label(c['name'])
            if k == 'TAB':
                out.append(f'<rect x="{x}" y="{y+24}" width="{cw}" height="{ch-24}" fill="#fbfbfb" stroke="#666"/>')
                tx = x
                for i in range(1, len(pages)+1):
                    act = (i == page)
                    out.append(f'<rect x="{tx}" y="{y}" width="110" height="25" fill="{"#fbfbfb" if act else "#d9d9d9"}" stroke="#666"/>' + text(tx+55, y+17, TABNAMES.get(w['name'], {}).get(i, f'Onglet {i}'), 10, anchor='middle', weight='bold' if act else 'normal'))
                    tx += 110
                continue
            out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{FILL[k]}" stroke="{STROKE[k]}" stroke-width="1" {"stroke-dasharray=\"4 3\"" if k=="STATIC" and ch>40 else ""} {"rx=\"4\"" if k=="BUTTON" else ""}/>')
            if k == 'BUTTON':
                out.append(text(x+cw/2, y+ch/2+4, clip(nm, cw-6), 10, anchor='middle', weight='bold'))
            elif k == 'STATIC':
                out.append(text(x+4, y+14 if ch>40 else y+ch/2+4, clip(nm, cw-8, 11), 11 if ch <= 40 else 10, weight='bold' if ch<=40 else 'normal', fill='#333' if ch<=40 else '#777', style='normal' if ch<=40 else 'italic'))
            elif k in ('EDIT', 'COMBO'):
                multi = ch > 30
                if cw > 150 and not multi:
                    lw = min(int(cw*0.42), 120)
                    out.append(text(x+3, y+ch/2+4, clip(nm, lw-6, 9), 9, fill='#444'))
                    out.append(f'<rect x="{x+lw}" y="{y+2}" width="{cw-lw-2}" height="{ch-4}" fill="#fff" stroke="#8aa8e0"/>')
                    if k == 'COMBO': out.append(text(x+cw-12, y+ch/2+4, '▾', 11))
                else:
                    out.append(text(x+4, y+13, clip(nm, cw-8, 9), 9, fill='#444', style='italic'))
                    if k == 'COMBO': out.append(text(x+cw-12, y+ch/2+4, '▾', 11))
            elif k == 'IMAGE':
                out.append(f'<line x1="{x}" y1="{y}" x2="{x+cw}" y2="{y+ch}" stroke="#b9a6df"/><line x1="{x+cw}" y1="{y}" x2="{x}" y2="{y+ch}" stroke="#b9a6df"/>')
                out.append(text(x+cw/2, y+ch/2+4, clip('IMG ' + nm, cw-6), 10, anchor='middle', fill='#5b3aa5', weight='bold'))
            elif k in ('LIST', 'LISTVIEW'):
                out.append(text(x+4, y+13, clip(('Liste ' if k=='LIST' else 'Liste image ') + nm, cw-8, 9), 9, weight='bold', fill='#256b30'))
                for i in range(1, 5): out.append(f'<line x1="{x+2}" y1="{y+18+i*18}" x2="{x+cw-2}" y2="{y+18+i*18}" stroke="#bcd9bc"/>')
            elif k == 'TABLE':
                cols = [col for col in (c.get('columns') or [])]
                out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="20" fill="#bfe6da" stroke="{STROKE[k]}"/>')
                if cols:
                    colw = cw / len(cols); cx = x
                    for col in cols:
                        hidden = str(col['name']).upper().startswith('COL_ID')
                        out.append(text(cx+3, y+14, clip(label(col['name']), colw-6, 9), 9, weight='bold', fill='#888' if hidden else '#0b4d3e', style='italic' if hidden else 'normal'))
                        cx += colw
                        out.append(f'<line x1="{cx:.0f}" y1="{y}" x2="{cx:.0f}" y2="{y+ch}" stroke="#a9d6c9"/>')
                for i in range(1, int((ch-20)/18)): out.append(f'<line x1="{x}" y1="{y+20+i*18}" x2="{x+cw}" y2="{y+20+i*18}" stroke="#cfe9e1"/>')
                out.append(text(x+4, y+ch-6, 'Table ' + nm, 9, fill='#0b4d3e', style='italic'))
    # legend
    ly = fh + 52
    lx = 24
    for k in ('EDIT','COMBO','BUTTON','STATIC','TABLE','LIST','IMAGE'):
        out.append(f'<rect x="{lx}" y="{ly}" width="14" height="12" fill="{FILL[k]}" stroke="{STROKE[k]}"/>' + text(lx+18, ly+10, {'EDIT':'Saisie (SAI_)','COMBO':'Combo (COMBO_)','BUTTON':'Bouton (BTN_)','STATIC':'Libellé (LIB_)','TABLE':'Table (TABLE_)','LIST':'Liste (LISTE_/LSI_)','IMAGE':'Image (IMG_)'}[k], 9))
        lx += 125
    out.append('</svg>')
    open(os.path.join(outdir, w['name'] + '.svg'), 'w', encoding='utf-8').write('\n'.join(out))
    print('wrote', w['name'] + '.svg', f'{len(pages)} page(s)')
