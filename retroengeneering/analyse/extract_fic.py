# Heuristic HFSQL Classic (.FIC) record extractor: uses the analysis (.xdd) for field order/sizes,
# then searches the record header size (h) and phase that yields clean decodes.
import xml.etree.ElementTree as ET, struct, os, sys, json, re
src, out = sys.argv[1], sys.argv[2]
xdd = [p for p in os.listdir(os.path.join(src, next(d for d in os.listdir(src) if d.endswith('.ana')))) if p.endswith('.xdd')][0]
anadir = os.path.join(src, next(d for d in os.listdir(src) if d.endswith('.ana')))
root = ET.fromstring(open(os.path.join(anadir, xdd), 'rb').read())
files = {}
for fic in root.findall('FICHIER'):
    files[fic.get('Nom')] = [(r.get('Nom'), int(r.findtext('TYPE')), int(r.findtext('TAILLE'))) for r in fic.findall('RUBRIQUE') if r.findtext('TYPE') is not None]
TEXT, DATE, MEMO = {2}, {14}, {29, 30}
def decode(rec, items):
    row, pos, ok = {}, 0, True
    for name, t, sz in items:
        chunk = rec[pos:pos+sz]; pos += sz
        if t in TEXT:
            s = chunk.split(b'\x00')[0].decode('latin-1').rstrip()
            if any(ord(ch) < 32 for ch in s): ok = False
            row[name] = s
        elif t in DATE:
            s = chunk.decode('latin-1', 'replace')
            if s.strip('\x00 ') and not re.fullmatch(r'\d{8}', s): ok = False
            row[name] = s.strip('\x00 ')
        elif t in MEMO:
            row[name] = '<memo>'
        else:
            row[name] = int.from_bytes(chunk[:8], 'little', signed=True) if sz in (1,2,4,8) else chunk.hex()
            if isinstance(row[name], int) and abs(row[name]) > 10**9: ok = False
    return row, ok
result = {}
for fname, items in files.items():
    path = next((os.path.join(src, 'Exe', p) for p in os.listdir(os.path.join(src, 'Exe')) if p.lower() == fname.lower() + '.fic'), None)
    if not path: print("no data file for", fname); continue
    data = open(path, 'rb').read(); L = sum(sz for _, _, sz in items)
    best = None
    for h in range(0, 24):
        R = L + h
        for phase in range(1200, 1200 + R):
            good = 0; rows = []
            for i in range(60):
                s = phase + i * R
                if s + R > len(data): break
                row, ok = decode(data[s + h:s + R], items)
                if ok and any(isinstance(v, str) and v not in ('', '<memo>') for v in row.values()): good += 1; rows.append(row)
            if best is None or good > best[0]: best = (good, h, phase, rows)
    good, h, phase, rows = best
    nrec = (len(data) - phase) // (L + h)
    result[fname] = {'record_size': L + h, 'header_bytes': h, 'phase': phase, 'approx_records': nrec, 'good_in_first_60': good, 'sample': rows[:12]}
    print(f"\n### {fname}: L={L} h={h} R={L+h} phase={phase} approx_records={nrec} good/60={good}")
    for r in rows[:6]: print("   ", r)
json.dump(result, open(out, 'w'), ensure_ascii=False, indent=1)
