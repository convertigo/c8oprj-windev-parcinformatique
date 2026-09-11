---
name: convertigo-ngx-tree-apply-pieges
description: Pièges vérifiés en construisant des pages NGX Convertigo par databaseobject-tree-apply (attributs liés, événements ionChange, guillemets, tables HTML, Alert)
metadata:
  type: feedback
---

Vérifié le 2026-09-11 sur Convertigo 8.5 (template NGX 8.4.0.53) en lisant le code généré dans `_private/ionic/src/app` :

- Un `UIAttribute` dont `attrName` est entre crochets (`[disabled]`, `[ngStyle]`, `[class.x]`, `[fill]`) doit avoir `attrValue` en mode SCRIPT ; en mode PLAIN la valeur est émise entre quotes (chaîne littérale toujours vraie, ngStyle inerte).
- Pour un `UIControlEvent`, `eventName` pilote l'attribut généré : `onChange` devient `(change)`, qui ne se déclenche pas sur `ion-select`. Utiliser `eventName: ionChange` + `attrName: (ionChange)` ; la valeur est dans `parent.out.detail.value`.
- Une valeur SCRIPT liée dans le template (UIUseVariable, Label, etc.) est insérée dans un attribut HTML entre guillemets doubles : n'utiliser que des chaînes à simples quotes sans apostrophe (`"Modifier l'utilisateur"` casse le HTML). Les propriétés d'actions (Alert, Toast, SetLocal) sont du TS et acceptent les guillemets doubles.
- `AlertAction` résout `parent.out` avec `{data, role}` : `data` = `valueN` du bouton cliqué, `role: 'cancel'` pour un bouton `cancelN`.
- Tables HTML : `ngx.components.UIElement#UIElement` avec `tagName` table/thead/tbody/tr/th/td ; un `UIControlDirective` If peut être enfant direct d'un ForEach (ng-container). Pas de fonctions fléchées dans les `{{ }}` : précalculer les listes aplaties dans des SetLocal.
- Un composant partagé peut être utilisé dans un autre (`UIUseShared` sous `Card.Content` d'un `UISharedRegularComponent`), hors du `<form>` pour éviter les formulaires imbriqués.
- Les formulaires du kit lient les champs en `[ngModel]` one-way sur `local.draft` : mettre à jour `local.draft = Object.assign({}, draft, {x})` change le contrôle sans écraser la saisie des autres champs.
- Les frères d'une chaîne d'actions démarrent en parallèle : figer l'état lu (ex. `clickStep`) dans un SetLocal parent avant des IfAction frères.
- `EmitEventAction` a pour classe `ngx.components.UIDynamicEmit`, pas `UIDynamicAction` ; pour déplacer un nœud existant, `databaseobject-move` est plus sûr que le recréer.
- L'outil `requestable-execute` est bloqué par le classificateur pour les transactions de suppression : tester les gardes SQL par lecture (count) plutôt que par exécution.

**Why:** ces erreurs ne produisent aucune erreur de compilation, seulement des écrans inertes au runtime.

**How to apply:** relire `grep` sur le HTML généré après chaque lot d'attributs/événements ; voir aussi [[windev-parc-informatique-vers-convertigo]].

## Piège majeur (2026-09-11) : `tree-apply` mode merge REMPLACE les enfants nommés qui portent un `className`

- Un `tree-apply` `at: self` sur un parent avec `children: [{name, className, properties, children}]` visant des enfants EXISTANTS (ex. GridCol) a supprimé et recréé ces enfants (résumé `deleted: 3, replaced: 3`) : tout leur contenu (UIUseShared, événements, actions) a été perdu et le projet sauvegardé aussitôt (pas de retour arrière possible ; pas d'historique Eclipse pour les yaml).
- **Why:** le merge apparie par nom, mais dès qu'un `className` est fourni sur un enfant existant, il est recréé à neuf.
- **How to apply:** pour modifier un nœud existant, cibler ce nœud lui-même (`target` = son qname, `at: self`, `tree: {properties: {...}}` sans `className` ni `children`). Pour ajouter un enfant, `at: inside` avec un seul nœud. Ne jamais lister des enfants existants avec `className` sous un parent. Toujours relire `tree-get` + le HTML généré après une mutation structurelle, avant d'enchaîner. La restauration s'est faite en recréant les nœuds depuis le transcript et les composants partagés intacts (sp:*ListPanel/DetailCard/EditForm : émissions `{ id: row.id, row }`, `{ id, mode }`, `{ id }`).
- `batch-call` (optimizeMutations par défaut) ne déclenche la régénération des sources que pour le premier objet touché ; avec `optimizeMutations: false` il ne sauvegarde ni ne régénère rien. Après un lot, refaire un `tree-apply` individuel (ex. sur `comment`) sur chaque page ou composant partagé modifié, ou n'utiliser que des appels individuels. Les styles de page (`pg:X.Content.sl:PageStyle`) sont compilés avec un préfixe de classe (spécificité supérieure aux styles applicatifs `sl:*`). Le bean menu s'appelle `ngx.components.UIDynamicElement#MenuButton` (palette-list avec filter `MenuButton`).
