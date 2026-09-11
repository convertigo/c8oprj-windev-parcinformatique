# Decoder for the HFSQL Classic data files of WD-Gestion-de-Parc-informatique (layouts established from hex dumps).
# Record = [8-byte header][null bitmap: 1 byte per 8 items][fields]; text/date = size+1 (NUL terminated), memo = 8-byte pointer, ints LE.
import re, json, sys, os
src, out = sys.argv[1], sys.argv[2]
LAYOUT = {  # file: (record size, first-record anchor regex, anchor field offset in record, fields[(name, offset, size, kind)])
 'LIEU':        (90,  rb"Salle de r", 9,  [('IDLieu',78,4,'int'),('Emplacement',9,40,'txt'),('Commentaire',50,8,'memo'),('Rectangle',58,19,'txt'),('Picto',82,8,'memo')]),
 'MACHINE':     (90,  rb"MCH241", 9,     [('IDMachine',86,4,'int'),('NomMachine',9,40,'txt'),('InitialesUtilisateur',50,10,'txt'),('AdresseIP',61,20,'txt'),('IDLieu',82,4,'int')]),
 'UTILISATEUR': (82,  rb"Yves\x00", 9,   [('Initiales',9,10,'txt'),('Tel',20,20,'txt'),('NomComplet',41,30,'txt'),('Photo',72,8,'memo'),('Civilite',80,2,'int')]),
 'FOURNISSEUR': (418, rb"COMPAQ", 9,     [('IDFournisseur',414,4,'int'),('NomFournisseur',9,40,'txt'),('Adresse',50,300,'txt'),('Tel',351,20,'txt'),('TelSAV',372,20,'txt'),('Fax',393,20,'txt')]),
 'COMPOSANT':   (169, rb"5811YUX", 18,   [('IDCOMPOSANT',10,8,'int'),('NSerie',18,20,'txt'),('DateAchat',39,8,'date'),('Garantie',48,20,'txt'),('NumRetour',69,20,'txt'),('DateRetour',90,8,'date'),('DateRenvoi',99,8,'date'),('Commentaire',108,8,'memo'),('NomMachine',116,40,'txt'),('IDMODELE',157,8,'int'),('IDFournisseur',165,4,'int')]),
 'MODELE':      (447, rb"POWEREDGE 2100", 10, [('NomModele',10,30,'txt'),('MarqueModele',41,30,'txt'),('TypeModele',72,30,'txt'),('Caracteristique1',103,30,'txt'),('Caracteristique2',134,30,'txt'),('Caracteristique3',165,30,'txt'),('Caracteristique4',196,30,'txt'),('Valeur1',227,50,'txt'),('Valeur2',278,50,'txt'),('Valeur3',329,50,'txt'),('Valeur4',380,50,'txt'),('Commentaire',431,8,'memo'),('IDMODELE',439,8,'int')]),
}
def txt(b): return b.split(b'\x00')[0].decode('latin-1').rstrip()
def clean(s): return all(ord(ch) >= 32 for ch in s) and '\xff' not in s and '\x7f' not in s
result = {}
for fname, (R, anchor, aoff, fields) in LAYOUT.items():
    path = next(os.path.join(src, 'Exe', p) for p in os.listdir(os.path.join(src, 'Exe')) if p.lower() == fname.lower() + '.fic')
    data = open(path, 'rb').read()
    first = re.search(anchor, data).start() - aoff
    # walk backwards to catch earlier records too
    start = first
    while start - R >= 0 and data[start - R] in (0x10, 0x80, 0x00, 0x90, 0x30): start -= R
    rows, bad = [], 0
    for s in range(start, len(data) - R + 1, R):
        rec = data[s:s+R]; row = {'_status': rec[0]}
        ok = True
        for name, off, size, kind in fields:
            chunk = rec[off:off+size]
            if kind == 'txt':
                v = txt(chunk); ok &= clean(v); row[name] = v
            elif kind == 'date':
                v = txt(chunk); ok &= (v == '' or re.fullmatch(r'\d{8}', v) is not None); row[name] = f"{v[:4]}-{v[4:6]}-{v[6:]}" if v else None
            elif kind == 'memo':
                row[name] = None if chunk in (b'\xff'*8, b'\x00'+b'\xff'*7, b'\x00'*8) else '<memo>'
            else:
                row[name] = int.from_bytes(chunk, 'little', signed=True)
        keyfield = fields[1][0] if fields[0][3] == 'int' and fields[0][0].upper().startswith('ID') else fields[0][0]
        idf = next((f[0] for f in fields if f[3] == 'int' and f[0].upper().startswith('ID') and f[0].upper() != 'IDLIEU' or f[0] == 'IDLieu' and fname == 'LIEU'), None)
        if idf and row.get(idf, 1) <= 0: ok = False
        if fname == 'MODELE' and (not row.get('TypeModele') or not row.get('NomModele')): ok = False
        if not ok or not row.get(keyfield): bad += 1; continue
        rows.append(row)
    result[fname] = rows
    print(f"### {fname}: R={R} start={start} rows={len(rows)} rejected={bad} statuses={sorted(set(r['_status'] for r in rows))}")
    for r in rows[:3]: print("   ", {k: v for k, v in r.items() if k != '_status'})
json.dump(result, open(out, 'w'), ensure_ascii=False, indent=1)
# FK consistency
lieux = {r['IDLieu'] for r in result['LIEU']}; mach = {r['NomMachine'] for r in result['MACHINE']}
users = {r['Initiales'] for r in result['UTILISATEUR']}; four = {r['IDFournisseur'] for r in result['FOURNISSEUR']}; mod = {r['IDMODELE'] for r in result['MODELE']}
print("\nFK checks:")
print(" machines.IDLieu in lieux:", sum(r['IDLieu'] in lieux for r in result['MACHINE']), "/", len(result['MACHINE']), " (0 =", sum(r['IDLieu']==0 for r in result['MACHINE']), ")")
print(" machines.Initiales in users:", sum(r['InitialesUtilisateur'] in users for r in result['MACHINE']), " empty:", sum(r['InitialesUtilisateur']=='' for r in result['MACHINE']))
print(" composants.NomMachine in machines:", sum(r['NomMachine'] in mach for r in result['COMPOSANT']), " stock(empty):", sum(r['NomMachine']=='' for r in result['COMPOSANT']), "/", len(result['COMPOSANT']))
print(" composants.IDMODELE in modeles:", sum(r['IDMODELE'] in mod for r in result['COMPOSANT']))
print(" composants.IDFournisseur in fournisseurs:", sum(r['IDFournisseur'] in four for r in result['COMPOSANT']), " zero:", sum(r['IDFournisseur']==0 for r in result['COMPOSANT']))
print(" lieux ids:", sorted(lieux)); print(" fournisseur ids:", sorted(four)); print(" civilites:", sorted({r['Civilite'] for r in result['UTILISATEUR']}))
import collections; print(" types de modele:", collections.Counter(r['TypeModele'] for r in result['MODELE']).most_common(12))
