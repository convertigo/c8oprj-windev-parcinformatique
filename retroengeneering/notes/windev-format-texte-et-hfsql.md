---
name: windev-format-texte-et-hfsql
description: Comment lire des sources WinDev 28 au format texte (.wdw YAML, codes de types de champs et d'événements, internal_properties chiffrées) et décoder les fichiers HFSQL Classic .FIC.
metadata:
  type: reference
---

- Les `.wdw/.wdp/.wdg/.wde` en « format texte » sont du YAML valide (PyYAML `safe_load`) : `window.controls[]` avec `name`, `type`, `properties{x,y,width,height}`, `columns[]` (tables), `tabs[]` (onglets), `code_elements.p_codes[]` (code WLangage par événement), `code_elements.procedures[]`, `resources.string_res` et `dialogs` (textes des messages en clair).
- Types de champs : 2 saisie SAI_, 3 libellé LIB_, 4 bouton BTN_, 7 liste LISTE_, 8 image IMG_, 9 table TABLE_, 14 combo COMBO_, 16 onglet ONG_, 27 liste image LSI_. Événements : 18 clic, 33 sélection ligne, 21 affichage ligne, 14 init liste, 32 option de menu, 34 fin d'initialisation fenêtre.
- `internal_properties` (base64) est chiffré : libellés, liaisons fichier, styles et contenu des combos sont illisibles ; les déduire des noms de champs, du code et des états.
- Le modèle de données est en XML dans `<projet>.ana/<projet>.xdd` (FICHIER/RUBRIQUE avec TYPE, TAILLE, TYPE_CLE ; clés composées sans TYPE).
- HFSQL Classic `.FIC` : enregistrement = en-tête 8 octets (statut 0x10/0x80, 2 octets, timestamp 4 octets, 0x00) + 1 octet de bitmap par tranche de 8 rubriques, puis rubriques : texte/date taille+1 (NUL final), mémo 8 octets (vide = 0xFF×8), entiers little-endian ; l'ordre physique peut différer de l'ordre du .xdd (identifiants auto 4 octets souvent en fin). Repérer le premier enregistrement via une valeur texte connue, puis avancer par pas de taille fixe.

- Côté MCP Convertigo : `upsert-crud` exige `database.mode` (ex. `hsqldb`) et rejette les pluriels irréguliers dans `seed.data` ; `databaseobject-tree-apply` accepte des arbres imbriqués jusqu'à ~9 niveaux par appel, au-delà (et avec `batch-call`) l'argument n'est plus parsé : découper par sous-arbres et enchaîner les actions en frères plutôt qu'en profondeur quand l'ordre n'importe pas.

**Why:** évite de re-découvrir le format à chaque nouvel exemple WinDev à migrer.

**How to apply:** réutiliser les scripts `parse_wdw.py`, `decode_fic.py`, `build_spec.py`, `wireframes.py` (dans le zip livré lors de [[windev-parc-informatique-vers-convertigo]]).
