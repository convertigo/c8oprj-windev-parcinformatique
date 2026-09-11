# Builds the Convertigo `upsert-crud` spec (entities, relations, UI hints, seed) from the decoded HFSQL data.
# v2: entity LIEU exposed as `emplacements` (regular English inflection), no singular/plural overrides, default connector.
import json, sys, argparse
ap = argparse.ArgumentParser(); ap.add_argument('seed'); ap.add_argument('out'); ap.add_argument('--project', default='ParcInformatique')
ap.add_argument('--machines', type=int, default=10, help='machines whose components are seeded'); ap.add_argument('--stock', type=int, default=15); ap.add_argument('--full', action='store_true')
a = ap.parse_args(); S = json.load(open(a.seed))
lieux, users, fours, models, machines, comps = S['LIEU'], S['UTILISATEUR'], S['FOURNISSEUR'], S['MODELE'], S['MACHINE'], S['COMPOSANT']
lieu_id = {r['IDLieu']: i+1 for i, r in enumerate(lieux)}; user_id = {r['Initiales']: i+1 for i, r in enumerate(users)}
four_id = {r['IDFournisseur']: i+1 for i, r in enumerate(fours)}; mach_id = {r['NomMachine']: i+1 for i, r in enumerate(machines)}
if a.full: sel_comps = comps
else:
    with_comp = [m['NomMachine'] for m in machines if any(c['NomMachine'] == m['NomMachine'] for c in comps)]
    keep = set(with_comp[:a.machines])
    sel_comps = [c for c in comps if c['NomMachine'] in keep] + [c for c in comps if c['NomMachine'] == ''][:a.stock]
used = {c['IDMODELE'] for c in sel_comps}
sel_models = models if a.full else [m for m in models if m['IDMODELE'] in used]
model_id = {m['IDMODELE']: i+1 for i, m in enumerate(sel_models)}
sel_comps = [c for c in sel_comps if c['IDMODELE'] in model_id]
def row(d): return {k: v for k, v in d.items() if v not in (None, '')}
def photo(c): return 'images/visage_femme.gif' if c in (1, 2) else 'images/visage_homme.gif'
seed = {
 'emplacements': [row({'nom': r['Emplacement'], 'rectangle': r['Rectangle']}) for r in lieux],
 'utilisateurs': [row({'initiales': r['Initiales'], 'civilite': r['Civilite'], 'nom_complet': r['NomComplet'], 'tel': r['Tel'], 'photo': photo(r['Civilite'])}) for r in users],
 'fournisseurs': [row({'nom': r['NomFournisseur'], 'adresse': r['Adresse'], 'tel': r['Tel'], 'tel_sav': r['TelSAV'], 'fax': r['Fax']}) for r in fours],
 'modeles': [row({'type_modele': m['TypeModele'], 'nom_modele': m['NomModele'], 'marque': m['MarqueModele'], 'caracteristique1': m['Caracteristique1'], 'valeur1': m['Valeur1'], 'caracteristique2': m['Caracteristique2'], 'valeur2': m['Valeur2'], 'caracteristique3': m['Caracteristique3'], 'valeur3': m['Valeur3'], 'caracteristique4': m['Caracteristique4'], 'valeur4': m['Valeur4']}) for m in sel_models],
 'machines': [row({'nom_machine': r['NomMachine'], 'adresse_ip': r['AdresseIP'], 'emplacement_id': lieu_id.get(r['IDLieu']), 'utilisateur_id': user_id.get(r['InitialesUtilisateur'])}) for r in machines],
 'composants': [row({'n_serie': c['NSerie'], 'date_achat': c['DateAchat'], 'garantie': c['Garantie'], 'num_retour': c['NumRetour'], 'date_retour': c['DateRetour'], 'date_renvoi': c['DateRenvoi'], 'machine_id': mach_id.get(c['NomMachine']), 'modele_id': model_id[c['IDMODELE']], 'fournisseur_id': four_id.get(c['IDFournisseur'])}) for c in sel_comps],
}
def F(name, column, type_, **kw): return {'name': name, 'column': column, 'type': type_, **kw}
ID = {'name': 'Id', 'type': 'INT', 'primary': True}
spec = {
 'project': a.project,
 'database': {'mode': 'hsqldb'},
 'facade': {'prefix': 'parc'},
 'ui': {'entryPage': 'Home', 'variant': 'entity-pages'},
 'relations': [
  {'name': 'machine_emplacement', 'type': 'many-to-one', 'fromEntity': 'machines', 'fromField': 'emplacement_id', 'toEntity': 'emplacements', 'toField': 'id', 'label': 'Emplacement'},
  {'name': 'machine_utilisateur', 'type': 'many-to-one', 'fromEntity': 'machines', 'fromField': 'utilisateur_id', 'toEntity': 'utilisateurs', 'toField': 'id', 'label': 'Utilisateur'},
  {'name': 'composant_machine', 'type': 'many-to-one', 'fromEntity': 'composants', 'fromField': 'machine_id', 'toEntity': 'machines', 'toField': 'id', 'label': 'Machine'},
  {'name': 'composant_modele', 'type': 'many-to-one', 'fromEntity': 'composants', 'fromField': 'modele_id', 'toEntity': 'modeles', 'toField': 'id', 'label': 'Modèle', 'required': True},
  {'name': 'composant_fournisseur', 'type': 'many-to-one', 'fromEntity': 'composants', 'fromField': 'fournisseur_id', 'toEntity': 'fournisseurs', 'toField': 'id', 'label': 'Fournisseur'},
 ],
 'entities': [
  {'name': 'emplacements', 'displayLabel': 'Lieux', 'fields': [ID, F('Nom','nom','VARCHAR(40)', unique=True, required=True), F('Commentaire','commentaire','TEXT'), F('Rectangle','rectangle','VARCHAR(19)'), F('Picto','picto','VARCHAR(255)')],
   'ui': {'listFields': ['nom','rectangle'], 'formFields': ['nom','commentaire','rectangle','picto'], 'fieldLabels': {'nom': 'Nom du lieu', 'commentaire': 'Commentaire', 'rectangle': 'Rectangle sur le plan (x1,y1,x2,y2)', 'picto': 'Pictogramme'}}},
  {'name': 'utilisateurs', 'displayLabel': 'Utilisateurs', 'fields': [ID, F('Initiales','initiales','VARCHAR(10)', unique=True, required=True), F('Civilite','civilite','INT'), F('NomComplet','nom_complet','VARCHAR(30)'), F('Tel','tel','VARCHAR(20)'), F('Photo','photo','VARCHAR(255)')],
   'ui': {'listFields': ['initiales','tel','nom_complet'], 'formFields': ['civilite','initiales','tel','nom_complet','photo'], 'fieldLabels': {'initiales': 'Utilisateur', 'civilite': 'Civilité (1 Mme, 2 Mlle, 3 M.)', 'nom_complet': 'Nom complet', 'tel': 'Téléphone', 'photo': 'Photo'}}},
  {'name': 'fournisseurs', 'displayLabel': 'Fournisseurs', 'fields': [ID, F('Nom','nom','VARCHAR(40)', unique=True, required=True), F('Adresse','adresse','VARCHAR(300)'), F('Tel','tel','VARCHAR(20)'), F('TelSav','tel_sav','VARCHAR(20)'), F('Fax','fax','VARCHAR(20)')],
   'ui': {'listFields': ['nom','adresse','tel','tel_sav','fax'], 'formFields': ['nom','tel','tel_sav','fax','adresse'], 'fieldLabels': {'nom': 'Nom', 'adresse': 'Adresse', 'tel': 'Téléphone', 'tel_sav': 'Téléphone SAV', 'fax': 'Fax'}}},
  {'name': 'modeles', 'displayLabel': 'Modèles', 'fields': [ID, F('TypeModele','type_modele','VARCHAR(30)', required=True), F('NomModele','nom_modele','VARCHAR(30)', required=True), F('Marque','marque','VARCHAR(30)'),
     F('Caracteristique1','caracteristique1','VARCHAR(30)'), F('Valeur1','valeur1','VARCHAR(50)'), F('Caracteristique2','caracteristique2','VARCHAR(30)'), F('Valeur2','valeur2','VARCHAR(50)'),
     F('Caracteristique3','caracteristique3','VARCHAR(30)'), F('Valeur3','valeur3','VARCHAR(50)'), F('Caracteristique4','caracteristique4','VARCHAR(30)'), F('Valeur4','valeur4','VARCHAR(50)'), F('Commentaire','commentaire','TEXT')],
   'ui': {'listFields': ['type_modele','nom_modele','marque','commentaire'], 'formFields': ['nom_modele','marque','type_modele','caracteristique1','valeur1','caracteristique2','valeur2','caracteristique3','valeur3','caracteristique4','valeur4','commentaire'],
          'fieldLabels': {'type_modele': 'Type', 'nom_modele': 'Nom du modèle', 'marque': 'Marque', 'caracteristique1': 'Caractéristique 1 (libellé)', 'valeur1': 'Valeur 1', 'caracteristique2': 'Caractéristique 2 (libellé)', 'valeur2': 'Valeur 2', 'caracteristique3': 'Caractéristique 3 (libellé)', 'valeur3': 'Valeur 3', 'caracteristique4': 'Caractéristique 4 (libellé)', 'valeur4': 'Valeur 4', 'commentaire': 'Commentaire'}}},
  {'name': 'machines', 'displayLabel': 'Machines', 'fields': [ID, F('NomMachine','nom_machine','VARCHAR(40)', unique=True, required=True), F('AdresseIp','adresse_ip','VARCHAR(20)'), F('EmplacementId','emplacement_id','INT'), F('UtilisateurId','utilisateur_id','INT')],
   'ui': {'listFields': ['nom_machine','utilisateur_id','emplacement_id','adresse_ip'], 'formFields': ['nom_machine','emplacement_id','utilisateur_id','adresse_ip'], 'fieldLabels': {'nom_machine': 'Nom de la machine', 'adresse_ip': 'Adresse IP', 'emplacement_id': 'Emplacement', 'utilisateur_id': 'Utilisateur'},
          'relationFields': {'emplacement_id': {'control': 'select', 'optionLabelField': 'nom', 'optionValueField': 'id', 'placeholder': 'Choisir un lieu'}, 'utilisateur_id': {'control': 'select', 'optionLabelField': 'initiales', 'optionValueField': 'id', 'placeholder': 'Choisir un utilisateur'}}}},
  {'name': 'composants', 'displayLabel': 'Composants', 'fields': [ID, F('NSerie','n_serie','VARCHAR(20)', required=True), F('DateAchat','date_achat','DATE'), F('Garantie','garantie','VARCHAR(20)'), F('NumRetour','num_retour','VARCHAR(20)'), F('DateRetour','date_retour','DATE'), F('DateRenvoi','date_renvoi','DATE'), F('Commentaire','commentaire','TEXT'),
     F('MachineId','machine_id','INT'), F('ModeleId','modele_id','INT', required=True), F('FournisseurId','fournisseur_id','INT')],
   'ui': {'listFields': ['n_serie','modele_id','machine_id','fournisseur_id','date_achat'], 'formFields': ['n_serie','modele_id','date_achat','fournisseur_id','garantie','num_retour','date_retour','date_renvoi','commentaire','machine_id'],
          'fieldLabels': {'n_serie': 'Numéro de série', 'date_achat': "Date d'achat", 'garantie': 'Garantie', 'num_retour': 'Numéro de retour', 'date_retour': 'Date de retour', 'date_renvoi': 'Date de renvoi', 'commentaire': 'Commentaires', 'machine_id': 'Machine (vide = en stock)', 'modele_id': 'Modèle (type de composant)', 'fournisseur_id': 'Fournisseur'},
          'relationFields': {'machine_id': {'control': 'select', 'optionLabelField': 'nom_machine', 'optionValueField': 'id', 'placeholder': 'En stock'}, 'modele_id': {'control': 'autocomplete', 'optionLabelField': 'nom_modele', 'optionValueField': 'id', 'placeholder': 'Choisir un modèle'}, 'fournisseur_id': {'control': 'select', 'optionLabelField': 'nom', 'optionValueField': 'id', 'placeholder': 'Choisir un fournisseur'}}}},
 ],
 'seed': {'enabled': True, 'data': seed},
}
json.dump(spec, open(a.out, 'w'), ensure_ascii=False, indent=1)
if a.out.endswith('.json'): open(a.out[:-5] + '.min.json', 'w').write(json.dumps(spec, ensure_ascii=False, separators=(',', ':')))
print(f"{a.out}: " + ', '.join(f"{k}={len(v)}" for k, v in seed.items()) + f"  ({len(json.dumps(spec, ensure_ascii=False))//1024} KB, compact {len(json.dumps(spec, ensure_ascii=False, separators=(',',':')))} chars)")
