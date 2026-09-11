import yaml, json, glob, os, sys, collections
src = sys.argv[1]; out = sys.argv[2]
stats = collections.Counter(); keysets = collections.defaultdict(set)
def code_events(node):
    evs = []
    for pc in (node.get('code_elements') or {}).get('p_codes') or []:
        code = pc.get('code')
        if isinstance(code, str) and code.strip():
            evs.append({'type': pc.get('type'), 'code': code})
    return evs
def walk(ctrls, parent, acc):
    for c in ctrls or []:
        if not isinstance(c, dict): continue
        name = c.get('name'); t = c.get('type'); p = c.get('properties') or {}
        e = {'name': name, 'type': t, 'parent': parent, 'x': p.get('x'), 'y': p.get('y'), 'w': p.get('width'), 'h': p.get('height')}
        extra = {k: v for k, v in p.items() if k not in ('x','y','width','height')}
        if extra: e['props'] = extra
        keysets[t] |= set(c.keys())
        if 'columns' in c:
            e['columns'] = [{'name': col.get('name'), 'type': col.get('type'), 'content': col.get('content'),
                             'w': (col.get('properties') or {}).get('width'), 'events': code_events(col)} for col in c['columns'] if isinstance(col, dict)]
        if 'dropdown' in c:
            dd = c['dropdown']; e['dropdown'] = {k: (v if not isinstance(v, (list, dict)) else f'<{type(v).__name__} {len(v)}>') for k, v in dd.items()} if isinstance(dd, dict) else dd
        e['events'] = code_events(c)
        acc.append(e)
        stats[(t, (name or '').split('_')[0])] += 1
        walk(c.get('controls'), name, acc)
        for i, tab in enumerate(c.get('tabs') or []):
            walk((tab or {}).get('controls'), f"{name}[{i+1}]", acc)
        dd = c.get('dropdown')
        if isinstance(dd, dict):
            walk(dd.get('controls'), f"{name}.dropdown", acc)
            for k in ('window',):
                if isinstance(dd.get(k), dict): walk(dd[k].get('controls'), f"{name}.dropdown", acc)
def menu(opts, acc, depth=0):
    for o in opts or []:
        if not isinstance(o, dict): continue
        acc.append({'depth': depth, 'name': o.get('name'), 'label': o.get('label'), 'events': code_events(o)})
        menu(o.get('options'), acc, depth+1)
result = {}
for f in sorted(glob.glob(os.path.join(src, '*.wdw'))):
    doc = yaml.safe_load(open(f, encoding='utf-8'))
    w = doc.get('window') or {}
    ctrls = []; walk(w.get('controls'), None, ctrls)
    m = []; menu((w.get('menu') or {}).get('options'), m)
    procs = [{'name': pr.get('name'), 'code': pr.get('code')} for pr in (w.get('code_elements') or {}).get('procedures') or []]
    res = doc.get('resources') or {}
    strings = [{'index': s.get('index'), 'text': s.get('text')} for s in ((res.get('string_res') or {}).get('strings') or [])]
    dialogs = [{'label': d.get('label'), 'buttons': [b.get('label') for b in d.get('buttons') or []]} for d in (res.get('dialogs') or [])]
    result[os.path.basename(f)] = {'name': w.get('name'), 'properties': w.get('properties'), 'controls': ctrls, 'menu': m,
        'window_events': code_events(w), 'procedures': procs, 'strings': strings, 'dialogs': dialogs,
        'embedded': (doc.get('embedded_elements') or {}).get('elements'), 'other_keys': [k for k in w.keys() if k not in ('name','identifier','internal_properties','properties','controls','menu','code_elements','languages','popup_menus','message_bar','actionbar','code_parameters')]}
    print(f"{os.path.basename(f):32s} {w.get('properties',{}).get('width')}x{w.get('properties',{}).get('height')}  controls={len(ctrls):3d} menu={len(m)} procs={len(procs)} strings={len(strings)} dialogs={len(dialogs)} winevents={len(result[os.path.basename(f)]['window_events'])}")
json.dump(result, open(out, 'w'), ensure_ascii=False, indent=1)
print("\n=== type -> prefix frequency ===")
for (t, pre), n in sorted(stats.items()): print(f"type {t!s:>8}  {pre:8s} x{n}")
print("\n=== keys per control type ===")
for t, ks in sorted(keysets.items(), key=lambda kv: str(kv[0])): print(t, sorted(ks - {'name','identifier','internal_properties','properties','type','code_elements'}))
