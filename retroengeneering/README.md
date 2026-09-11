# xclaude — Reconstruction de « WD Gestion de Parc informatique » (WinDev) en Convertigo

Tout ce qui a été produit dans la conversation Claude du 2026-09-11 (rétro-ingénierie de l'exemple PC SOFT, rail CRUD Convertigo, écrans sur mesure, mise en page côte à côte et charte graphique bleue).

| Dossier / fichier | Contenu |
|---|---|
| `analyse/ANALYSE_ECRANS.md` | Document d'analyse complet : méthode, modèle HFSQL, fiches des 11 fenêtres, états, correspondance WinDev → Convertigo NGX, plan de reconstruction (étapes 1 à 5 réalisées), charte graphique (§9) |
| `analyse/convertigo-crud-spec*.json` | Spécifications `upsert-crud` (démo 4 machines, démo complète, version `full` avec toutes les données) |
| `analyse/wireframes/*.svg` | Maquettes filaires des 11 fenêtres WinDev (positions réelles) |
| `analyse/wdw.json`, `seed_data.json`, `seed_sample.json`, `dump_code_*.txt` | Extraction brute des fenêtres, données de démo décodées depuis les fichiers HFSQL, code WLangage par fenêtre |
| `analyse/*.py` | Scripts rejouables : `parse_wdw.py`, `decode_fic.py`, `extract_fic.py`, `build_spec.py`, `wireframes.py`, `dump_inventory.py`, `build_page.py` |
| `analyse-parc-informatique.zip` | Archive livrée en cours de conversation (analyse + wireframes + scripts) |
| `artefact/ecrans-parc-informatique.html` | Page de synthèse « Écrans WD Gestion de Parc » (source de l'artefact publié) |
| `sources/WD-Gestion-de-Parc-informatique/` | Dépôt PC SOFT cloné (entrée de l'analyse, WinDev 28 format texte) |
| `convertigo/ParcInformatique/` | Projet Convertigo produit (sources `_c8oProject/*.yaml`, `c8oProject.yaml`, build de production `DisplayObjects/mobile`) ; le dossier `_private` (node_modules, build de dev) est exclu — à réimporter dans un Studio/serveur Convertigo 8.4+ |
| `captures/01…18-*.png` | Captures 1366×900 de chaque écran de l'application en production : tableau de bord, menu, parc (liste + plan, filtre par salle), fiche machine (3 colonnes, composant sélectionné, ajout depuis le stock), gestion des lieux / modèles / utilisateurs, états, les 6 pages du kit (liste, fiche, formulaire côte à côte) |
| `captures/19…21-mobile-*.png` | Vues mobile 390×844 (tableau de bord, parc, lieux) |
| `outils/captures-headless-chrome.mjs` | Script Node (Chrome headless + CDP) qui rejoue le parcours et régénère les captures : `OUT=... PROFILE=... node captures-headless-chrome.mjs` |
| `notes/*.md` | Notes de travail : synthèse du projet, pièges du MCP Convertigo (`tree-apply`, `batch-call`), format texte WinDev / HFSQL, dépôts d'exemples PC SOFT |

Application : `http://localhost:18080/convertigo/projects/ParcInformatique/DisplayObjects/mobile/home` (serveur Convertigo local, projet `ParcInformatique`).
