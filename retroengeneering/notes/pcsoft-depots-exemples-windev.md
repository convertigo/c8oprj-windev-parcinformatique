---
name: pcsoft-depots-exemples-windev
description: Dépôts GitHub officiels PC SOFT contenant les sources des exemples WinDev (format texte, WinDev 28), utiles comme applications de démonstration à migrer.
metadata:
  type: reference
---

- https://github.com/PCSOFT-WINDEV-code-source (français) et https://github.com/PCSOFT-WINDEV-source-code (anglais) : ~130 dépôts chacun, sources au format texte, données de démo HFSQL dans `Exe/`.
- Bons candidats CRUD métier : `WD-Gestion-de-Parc-informatique` (11 fenêtres, 6 fichiers), `WD-Gestion-Contacts` (5 fenêtres), `WD-Gestion-Commerciale` (24 fenêtres, clients/produits/commandes/factures), `WD-Conges-et-RTT` (13 fenêtres). Licence : exemples didactiques réservés aux détenteurs d'une licence WINDEV.
- Communauté : `Fab2bprog/Windev-Radinus` (finance perso, très gros), `kalemadaniel/gestion_stock_windev`.

**Why:** point de départ rapide pour toute nouvelle démo WinDev → Convertigo ([[windev-parc-informatique-vers-convertigo]]).

**How to apply:** `gh api orgs/PCSOFT-WINDEV-code-source/repos?per_page=100` pour lister, puis `git clone --depth 1`.
