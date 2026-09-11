import json, sys
KIND = {2:'EDIT',3:'STATIC',4:'BUTTON',7:'LIST',8:'IMAGE',9:'TABLE',14:'COMBO',16:'TAB',27:'LISTVIEW'}
d = json.load(open(sys.argv[1])); mode = sys.argv[2]; only = sys.argv[3:]
def fr(x): return x.get('fr-FR') if isinstance(x, dict) else x
for win, w in d.items():
    if only and not any(o in win for o in only): continue
    if mode == 'controls':
        print(f"\n##### {w['name']}  window={w['properties']}")
        for m in w['menu']: print(f"  MENU {'  '*m['depth']}{m['name']} label={fr(m['label'])!r} events={[e['type'] for e in m['events']]}")
        for c in sorted(w['controls'], key=lambda c: (str(c['parent']), c['y'] or 0, c['x'] or 0)):
            print(f"  {c['name']:34s} {KIND.get(c['type'], str(c['type'])):8s} parent={str(c['parent'] or '-'):24s} xywh=({c['x']},{c['y']},{c['w']},{c['h']}) {('props='+json.dumps(c['props'],ensure_ascii=False)) if c.get('props') else ''} {('events='+','.join(str(e['type']) for e in c['events'])) if c['events'] else ''}")
            for col in c.get('columns') or []:
                print(f"      COL {str(col['name']):30s} type={col['type']} w={col['w']} content={json.dumps(col['content'],ensure_ascii=False)[:140]} events={[e['type'] for e in col['events']]}")
            if c.get('dropdown'): print(f"      DROPDOWN {json.dumps(c['dropdown'],ensure_ascii=False)[:400]}")
        print("  STRINGS:", [fr(s['text']) for s in w['strings']])
        for dg in w['dialogs']: print("  DIALOG:", fr(dg['label']), "->", [fr(b) for b in dg['buttons']])
        print("  EMBEDDED:", w['embedded']); print("  OTHER window keys:", w['other_keys'])
    else:
        print(f"\n\n################ CODE {w['name']} ################")
        for e in w['window_events']: print(f"\n--- WINDOW event type={e['type']} ---\n{e['code']}")
        for c in w['controls']:
            for e in c['events']: print(f"\n--- {c['name']} ({KIND.get(c['type'], c['type'])}) event type={e['type']} ---\n{e['code']}")
            for col in c.get('columns') or []:
                for e in col['events']: print(f"\n--- {c['name']}.{col['name']} (COL) event type={e['type']} ---\n{e['code']}")
        for m in w['menu']:
            for e in m['events']: print(f"\n--- MENU {m['name']} event type={e['type']} ---\n{e['code']}")
        for p in w['procedures']: print(f"\n--- PROCEDURE {p['name']} ---\n{p['code']}")
