# Projet xclaude — WD Gestion de Parc informatique (WinDev) reconstruit en Convertigo

Dossier de travail Claude Code regroupant tout ce qui a été produit le 2026-09-11 : voir `README.md` pour l'inventaire.

## Repères
- Analyse fonctionnelle et technique : `analyse/ANALYSE_ECRANS.md` (charte graphique et règles d'édition MCP au §9).
- Projet Convertigo : `convertigo/ParcInformatique/` (sources `_c8oProject/*.yaml`) ; l'instance vivante est dans `/Users/opic/runtime-New84/ParcInformatique` et s'édite via le MCP Convertigo (projet `ParcInformatique`, application NGX `NgxApp`).
- Application en production : http://localhost:18080/convertigo/projects/ParcInformatique/DisplayObjects/mobile/home ; viewer de dev : http://localhost:47242.
- Captures d'écran : `captures/` ; régénération : `OUT=captures PROFILE=/tmp/xclaude-chrome node outils/captures-headless-chrome.mjs`.

## Règles apprises (MCP Convertigo, voir `notes/convertigo-ngx-tree-apply-pieges.md`)
- Modifier un objet existant : `databaseobject-tree-apply` avec `at: self` et `properties` seules ; ajouter : `at: inside` avec un seul nœud ; ne jamais relister des enfants existants avec `className` (ils sont recréés vides).
- `batch-call` ne régénère les sources que du premier objet touché : après un lot, refaire un appel individuel par page ou composant modifié.
- Vérifier après chaque mutation : `databaseobject-tree-get` puis le HTML généré dans `_private/ionic/src/app`, et `mobile-builder-open` (`stateOnly`, `wait`) pour l'état de compilation.
