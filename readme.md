


# ParcInformatique

**IT asset management — the WinDev sample « WD Gestion de Parc informatique » rebuilt with Convertigo**

Rebuild of the PC SOFT sample application **WD Gestion de Parc informatique** (WinDev 28, HFSQL) as a Convertigo 8.4 NGX application (Ionic / Angular). The 11 WinDev windows, the 6 HFSQL files and the demo data were reverse-engineered from the text-format sources, then reconstructed with the Convertigo MCP: an embedded HSQLDB database seeded with the original demo data, hidden CRUD facade sequences, the generic *entity-pages* UI kit and six purpose-built screens. Panels (list, record, form, floor plan) are laid out side by side on wide screens and stack on mobile; the visual identity is a modern blue theme.

## Functional scope

| WinDev window / report | Convertigo page | Route |
|---|---|---|
| FEN_Principale — machines and clickable floor plan | `ParcPage` | `/parc` |
| FEN_Machine — machine record with its components (2 tabs) | `MachineDetailPage` (3 columns, no tabs) | `/machine` |
| FEN_Lieu — rooms drawn on the floor plan | `LieuxPage` | `/lieux` |
| FEN_Modèle — component models with dynamic characteristic labels | `ModelesGestionPage` | `/modeles-gestion` |
| FEN_Utilisateur — users with title and photo | `UtilisateursGestionPage` | `/utilisateurs-gestion` |
| FEN_Fournisseur, FEN_Composants, FEN_Choix* (pickers) | CRUD kit pages + enriched selects with inline creation | `/emplacements`, `/utilisateurs`, `/fournisseurs`, `/modeles`, `/machines`, `/composants` |
| Etat_Machine, Etat_Utilisateur, Etat_Fournisseur, Etat_Modele, Etat_Composant_Machine, Etat_Composant_Modele | `RapportsPage` (HTML preview, browser print) | `/rapports` |
| — | `Home` dashboard (counters, access to every screen) | `/home` |

## Architecture

- **Data**: embedded HSQLDB (connector `ParcInformatiquedb`), tables `emplacements`, `utilisateurs`, `fournisseurs`, `modeles`, `machines`, `composants` with foreign keys, seeded with the sample data (17 rooms, 50 users, 15 suppliers, 36 models, 69 machines, 49 components).
- **Backend**: hidden facade sequences `parc_*` (list, read, create, update, delete, count per entity; relation lists such as `parc_list_composants_by_machine`; `parc_link_composant` / `parc_unlink_composant` for the stock; `parc_delete_machine_with_composants` / `parc_delete_machine_keep_composants` for the three-way machine deletion). DELETE statements are guarded by `NOT EXISTS` and every `parc_delete_*` returns a `refs` count so the UI can display the WinDev refusal messages.
- **UI**: NGX application `NgxApp`. Generic CRUD kit (`*ListPanel`, `*DetailCard`, `*EditForm` shared components) customised with a title select (Madame / Mademoiselle / Monsieur), relation previews, inline "New" creation of the related record, deletion rules as toasts and a highlighted selected row. Custom pages for the floor plan, the machine record, the management screens and the reports. Application styles: `ParcTheme` (blue design system, responsive floor plan) and `PrintStyle` (`@media print`).
- **Business rules kept from WinDev**: components tab hidden until the machine is saved; deletion refused when a room, user, supplier or model is still referenced; machine deletion with three options (cancel, delete components, put components back in stock); new room traced with two clicks on the plan with overlap check; model characteristics labelled dynamically (`caracteristiqueN` → label of `valeurN`); user photo or default pictogram by title.

## Design system (blue theme)

| Token | Value | Usage |
|---|---|---|
| Primary | `#1d4ed8` | buttons, selection, links |
| Navy | `#0b2a6f` | card titles, table headers |
| Sky | `#0284c7` | accents (plan counters, screen cards) |
| Page background | `#eef3fb` | |
| Surface / border | `#ffffff` / `#d5e0f2` | cards, toolbars, fields |
| Page banner | gradient `#0b2a6f → #1d4ed8 → #0ea5e9` | page header and side menu header |
| Font | IBM Plex Sans | |

Rounded cards with soft shadows, pill toolbars, tables with sticky headers, lists with hover and a blue selection stripe, floor plan on a light blue grid with rooms in a white-to-blue gradient. Dark mode follows `prefers-color-scheme`.

Responsive grid (Ionic breakpoints xs / md / lg / xl): entity pages 12 → 5+7 → 4+4+4 → 3+4+5; machine record 12 → 12+6+6 → 4+4+4; park 12 → 4+8 → 3+9; rooms 12 → 8+4; dashboard counters 2, 3 then 6 per row. The floor plan keeps the WinDev 709×538 coordinate system rendered in percentages, so it scales with the column and clicks are mapped back to the original coordinates.

## Screens

### Dashboard and navigation

![Dashboard](marketplace/01-tableau-de-bord.png)

![Side menu opened from the page banner](marketplace/02-menu-lateral.png)

### IT park (FEN_Principale)

![Machines list and floor plan](marketplace/03-parc-machines-plan.png)

![Machines filtered by the room clicked on the plan](marketplace/04-parc-filtre-salle.png)

### Machine record (FEN_Machine)

![Machine record: form, components and detail side by side](marketplace/05-fiche-machine.png)

![Selected component with its model panel and dynamic labels](marketplace/06-fiche-machine-composant.png)

![Adding a component from the stock](marketplace/07-fiche-machine-stock.png)

### Rooms on the floor plan (FEN_Lieu)

![Rooms management: plan, record and form](marketplace/08-gestion-lieux.png)

### Component models (FEN_Modèle)

![Component models with dynamic characteristic labels](marketplace/09-gestion-modeles.png)

### Users (FEN_Utilisateur)

![Users with title and photo](marketplace/10-gestion-utilisateurs.png)

### Printed reports (Etat_*)

![Machines report](marketplace/11-etats-machines.png)

![Components per machine report](marketplace/12-etats-composants-par-machine.png)

### CRUD kit pages (list, record and form side by side)

![Rooms](marketplace/13-lieux.png)

![Users](marketplace/14-utilisateurs.png)

![Suppliers](marketplace/15-fournisseurs.png)

![Models](marketplace/16-modeles.png)

![Machines](marketplace/17-machines.png)

![Components](marketplace/18-composants.png)

### Mobile layout

![Dashboard on mobile](marketplace/19-mobile-tableau-de-bord.png)

![IT park on mobile](marketplace/20-mobile-parc.png)

![Rooms on mobile](marketplace/21-mobile-lieux.png)

## Running the application

- Studio dev viewer: `http://localhost:47242` (NGX builder).
- Production build: `http://localhost:18080/convertigo/projects/ParcInformatique/DisplayObjects/mobile/home`.
- Screenshots are stored in `marketplace/` and can be regenerated with the headless Chrome script kept in the `retroengeneering/outils` folder.

## Credits

Original sample: PC SOFT, *WD Gestion de Parc informatique* (WinDev 28). Reconstruction: Convertigo MCP, September 2026.




For more technical informations : [documentation](./project.md)

- [Installation](#installation)
- [Mobile Application](#mobile-application)
    - [Pages](#pages)
        - [ComposantsPage](#composantspage)
        - [EmplacementsPage](#emplacementspage)
        - [FournisseursPage](#fournisseurspage)
        - [Home](#home)
        - [LieuxPage](#lieuxpage)
        - [Login](#login)
        - [MachineDetailPage](#machinedetailpage)
        - [MachinesPage](#machinespage)
        - [ModelesGestionPage](#modelesgestionpage)
        - [ModelesPage](#modelespage)
        - [ParcPage](#parcpage)
        - [RapportsPage](#rapportspage)
        - [UtilisateursGestionPage](#utilisateursgestionpage)
        - [UtilisateursPage](#utilisateurspage)
    - [Shared Actions](#shared-actions)
        - [crud_bootstrap_dashboard](#crud_bootstrap_dashboard)
        - [crud_ensure_session](#crud_ensure_session)
    - [Shared Components](#shared-components)
        - [ComposantsDetailCard](#composantsdetailcard)
        - [ComposantsEditForm](#composantseditform)
        - [ComposantsListPanel](#composantslistpanel)
        - [CrudErrorRetryState](#cruderrorretrystate)
        - [CrudLoadingState](#crudloadingstate)
        - [CrudPageHeader](#crudpageheader)
        - [DashboardStatCard](#dashboardstatcard)
        - [EmplacementsDetailCard](#emplacementsdetailcard)
        - [EmplacementsEditForm](#emplacementseditform)
        - [EmplacementsListPanel](#emplacementslistpanel)
        - [FournisseursDetailCard](#fournisseursdetailcard)
        - [FournisseursEditForm](#fournisseurseditform)
        - [FournisseursListPanel](#fournisseurslistpanel)
        - [MachinesDetailCard](#machinesdetailcard)
        - [MachinesEditForm](#machineseditform)
        - [MachinesListPanel](#machineslistpanel)
        - [ModelesDetailCard](#modelesdetailcard)
        - [ModelesEditForm](#modeleseditform)
        - [ModelesListPanel](#modeleslistpanel)
        - [UtilisateursDetailCard](#utilisateursdetailcard)
        - [UtilisateursEditForm](#utilisateurseditform)
        - [UtilisateursListPanel](#utilisateurslistpanel)


## Installation

1. In your Convertigo Studio click on ![](https://github.com/convertigo/convertigo/blob/develop/eclipse-plugin-studio/icons/studio/project_import.gif?raw=true "Import a project in treeview") to import a project in the treeview
2. In the import wizard

   ![](https://github.com/convertigo/convertigo/blob/develop/eclipse-plugin-studio/tomcat/webapps/convertigo/templates/ftl/project_import_wzd.png?raw=true "Import Project")
   
   paste the text below into the `Project remote URL` field:
   <table>
     <tr><td>Usage</td><td>Click the copy button at the end of the line</td></tr>
     <tr><td>To contribute</td><td>

     ```
     ParcInformatique=https://github.com/convertigo/c8oprj-windev-parcinformatique.git:branch=master
     ```
     </td></tr>
     <tr><td>To simply use</td><td>

     ```
     ParcInformatique=https://github.com/convertigo/c8oprj-windev-parcinformatique/archive/master.zip
     ```
     </td></tr>
    </table>
3. Click the `Finish` button. This will automatically import the __ParcInformatique__ project


## Mobile Application

Describes the mobile application global properties

### Pages

#### ComposantsPage

Managed by upsert-ngx-crud-kit (entity-pages page template clone) for ComposantsPage. Mise en page cote a cote (liste | fiche | formulaire) et charte bleue appliquees le 2026-09-11 ; les panneaux ont ete recrees a la main apres restructuration.

#### EmplacementsPage

Managed by upsert-ngx-crud-kit (entity-pages page template clone) for EmplacementsPage. Direct edits may be overwritten; prefer template sources and entity.ui hints.

#### FournisseursPage

Managed by upsert-ngx-crud-kit (entity-pages page template clone) for FournisseursPage. Mise en page cote a cote (liste | fiche | formulaire) et charte bleue appliquees le 2026-09-11 ; les panneaux ont ete recrees a la main apres restructuration.

#### Home

Managed by upsert-ngx-crud-kit (entity-pages page template clone) for Home. Tableau de bord : cartes de comptage responsive (2 / 3 / 6 par ligne), acces aux ecrans, libelles en francais ; charte bleue appliquee le 2026-09-11.

#### LieuxPage

Ecran FEN_Lieu WinDev : plan des locaux cliquable (responsive, repere 709x538 rendu en pourcentages), fiche du lieu, creation par trace d'un rectangle en deux clics avec controle de chevauchement, modification et suppression (refusee si des machines occupent le lieu). Charte bleue sl:ParcTheme.

#### Login

Managed by upsert-ngx-crud-kit (entity-pages page template clone) for Login. Direct edits may be overwritten; prefer template sources and entity.ui hints.

#### MachineDetailPage

Fiche machine (FEN_Machine WinDev) : onglet Machine et onglet Composants.

#### MachinesPage

Managed by upsert-ngx-crud-kit (entity-pages page template clone) for MachinesPage. Mise en page cote a cote (liste | fiche | formulaire) et charte bleue appliquees le 2026-09-11 ; les panneaux ont ete recrees a la main apres restructuration.

#### ModelesGestionPage

Ecran FEN_Modele WinDev : table des modeles de composants (colonne defilante), fiche avec caracteristiques a libelles dynamiques, creation / modification via le formulaire partage, suppression refusee si des composants utilisent le modele, acces aux etats Liste et Details. Charte bleue sl:ParcTheme.

#### ModelesPage

Managed by upsert-ngx-crud-kit (entity-pages page template clone) for ModelesPage. Direct edits may be overwritten; prefer template sources and entity.ui hints.

#### ParcPage

Ecran principal (FEN_Principale WinDev) : machines et plan des locaux cliquable.

#### RapportsPage

Equivalent des etats WinDev (Etat_Machine, Etat_Utilisateur, Etat_Fournisseur, Etat_Modele, Etat_Composant_Machine, Etat_Composant_Modele) : apercu HTML (feuille blanche) puis impression navigateur. L'etat et son parametre sont recus par les globaux parcReport / parcReportId. Barre d'outils parc-toolbar.

#### UtilisateursGestionPage

Ecran FEN_Utilisateur WinDev : table des utilisateurs (colonne defilante), fiche avec civilite et photo (ou pictogramme par defaut selon la civilite), creation / modification via le formulaire partage, suppression refusee si des machines sont affectees, impression de l'etat Utilisateurs. Charte bleue sl:ParcTheme.

#### UtilisateursPage

Managed by upsert-ngx-crud-kit (entity-pages page template clone) for UtilisateursPage. Mise en page cote a cote (liste | fiche | formulaire) et charte bleue appliquees le 2026-09-11 ; les panneaux ont ete recrees a la main apres restructuration.

### Shared Actions

#### crud_bootstrap_dashboard

CRUD entity-pages bootstrap action.

#### crud_ensure_session

Ensure a generated authenticated session exists before CRUD facade calls.

### Shared Components

#### ComposantsDetailCard

Managed by upsert-ngx-crud-kit (entity-pages template clone) for ComposantsDetailCard. Libelles francises le 2026-09-11 (regenere).

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td></td>
</tr>
<tr>
<td>Title</td><td></td>
</tr>
</table>

#### ComposantsEditForm

Managed by upsert-ngx-crud-kit (entity-pages template clone) for ComposantsEditForm. Libelles francises le 2026-09-11 (regenere).

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ActionLabel</td><td></td>
</tr>
<tr>
<td>CreateTitle</td><td></td>
</tr>
<tr>
<td>DeleteLabel</td><td></td>
</tr>
<tr>
<td>DraftSeed</td><td></td>
</tr>
<tr>
<td>EditTitle</td><td></td>
</tr>
<tr>
<td>Mode</td><td></td>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td></td>
</tr>
</table>

**events**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>Cancelled</td><td>Emitted when the user cancels form editing.</td>
</tr>
<tr>
<td>Deleted</td><td>Emitted after a successful delete.</td>
</tr>
<tr>
<td>Saved</td><td>Emitted after a successful create or update.</td>
</tr>
</table>

#### ComposantsListPanel

Managed by upsert-ngx-crud-kit (entity-pages template clone) for ComposantsListPanel. Libelles francises le 2026-09-11.

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ActionLabel</td><td></td>
</tr>
<tr>
<td>PrimaryField</td><td></td>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SecondaryField</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td>Identifiant de la ligne selectionnee, pour surligner la ligne dans la liste.</td>
</tr>
<tr>
<td>Title</td><td></td>
</tr>
</table>

**events**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ItemSelected</td><td>Emitted when the user selects one row from the local list.</td>
</tr>
<tr>
<td>NewRequested</td><td>Emitted when the user wants to create a new row.</td>
</tr>
</table>

#### CrudErrorRetryState

Managed by upsert-ngx-crud-kit (entity-pages template clone) for CrudErrorRetryState. Direct edits may be overwritten; prefer entity.ui hints.

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>Message</td><td></td>
</tr>
</table>

**events**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>Retry</td><td>Emitted when the user asks to retry the current CRUD state.</td>
</tr>
</table>

#### CrudLoadingState

Managed by upsert-ngx-crud-kit (entity-pages template clone) for CrudLoadingState. Direct edits may be overwritten; prefer entity.ui hints.

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>Message</td><td></td>
</tr>
</table>

#### CrudPageHeader

Managed by upsert-ngx-crud-kit (entity-pages template clone) for CrudPageHeader. Direct edits may be overwritten; prefer entity.ui hints.

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>Subtitle</td><td></td>
</tr>
<tr>
<td>Title</td><td></td>
</tr>
</table>

#### DashboardStatCard

Managed by upsert-ngx-crud-kit (entity-pages template clone) for DashboardStatCard. Direct edits may be overwritten; prefer entity.ui hints.

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>Caption</td><td></td>
</tr>
<tr>
<td>Count</td><td></td>
</tr>
<tr>
<td>Title</td><td></td>
</tr>
</table>

#### EmplacementsDetailCard

Managed by upsert-ngx-crud-kit (entity-pages template clone) for EmplacementsDetailCard. Libelles francises le 2026-09-11 (regenere).

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td></td>
</tr>
<tr>
<td>Title</td><td></td>
</tr>
</table>

#### EmplacementsEditForm

Managed by upsert-ngx-crud-kit (entity-pages template clone) for EmplacementsEditForm. Libelles francises le 2026-09-11 (regenere).

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ActionLabel</td><td></td>
</tr>
<tr>
<td>CreateTitle</td><td></td>
</tr>
<tr>
<td>DeleteLabel</td><td></td>
</tr>
<tr>
<td>DraftSeed</td><td></td>
</tr>
<tr>
<td>EditTitle</td><td></td>
</tr>
<tr>
<td>Mode</td><td></td>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td></td>
</tr>
</table>

**events**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>Cancelled</td><td>Emitted when the user cancels form editing.</td>
</tr>
<tr>
<td>Deleted</td><td>Emitted after a successful delete.</td>
</tr>
<tr>
<td>Saved</td><td>Emitted after a successful create or update.</td>
</tr>
</table>

#### EmplacementsListPanel

Managed by upsert-ngx-crud-kit (entity-pages template clone) for EmplacementsListPanel. Direct edits may be overwritten; prefer entity.ui hints.

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ActionLabel</td><td></td>
</tr>
<tr>
<td>PrimaryField</td><td></td>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SecondaryField</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td>Identifiant de la ligne selectionnee, pour surligner la ligne dans la liste.</td>
</tr>
<tr>
<td>Title</td><td></td>
</tr>
</table>

**events**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ItemSelected</td><td>Emitted when the user selects one row from the local list.</td>
</tr>
<tr>
<td>NewRequested</td><td>Emitted when the user wants to create a new row.</td>
</tr>
</table>

#### FournisseursDetailCard

Managed by upsert-ngx-crud-kit (entity-pages template clone) for FournisseursDetailCard. Libelles francises le 2026-09-11 (regenere).

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td></td>
</tr>
<tr>
<td>Title</td><td></td>
</tr>
</table>

#### FournisseursEditForm

Managed by upsert-ngx-crud-kit (entity-pages template clone) for FournisseursEditForm. Libelles francises le 2026-09-11 (regenere).

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ActionLabel</td><td></td>
</tr>
<tr>
<td>CreateTitle</td><td></td>
</tr>
<tr>
<td>DeleteLabel</td><td></td>
</tr>
<tr>
<td>DraftSeed</td><td></td>
</tr>
<tr>
<td>EditTitle</td><td></td>
</tr>
<tr>
<td>Mode</td><td></td>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td></td>
</tr>
</table>

**events**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>Cancelled</td><td>Emitted when the user cancels form editing.</td>
</tr>
<tr>
<td>Deleted</td><td>Emitted after a successful delete.</td>
</tr>
<tr>
<td>Saved</td><td>Emitted after a successful create or update.</td>
</tr>
</table>

#### FournisseursListPanel

Managed by upsert-ngx-crud-kit (entity-pages template clone) for FournisseursListPanel. Libelles francises le 2026-09-11.

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ActionLabel</td><td></td>
</tr>
<tr>
<td>PrimaryField</td><td></td>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SecondaryField</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td>Identifiant de la ligne selectionnee, pour surligner la ligne dans la liste.</td>
</tr>
<tr>
<td>Title</td><td></td>
</tr>
</table>

**events**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ItemSelected</td><td>Emitted when the user selects one row from the local list.</td>
</tr>
<tr>
<td>NewRequested</td><td>Emitted when the user wants to create a new row.</td>
</tr>
</table>

#### MachinesDetailCard

Managed by upsert-ngx-crud-kit (entity-pages template clone) for MachinesDetailCard. Libelles francises le 2026-09-11 (regenere).

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td></td>
</tr>
<tr>
<td>Title</td><td></td>
</tr>
</table>

#### MachinesEditForm

Managed by upsert-ngx-crud-kit (entity-pages template clone) for MachinesEditForm. Libelles francises le 2026-09-11 (regenere).

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ActionLabel</td><td></td>
</tr>
<tr>
<td>CreateTitle</td><td></td>
</tr>
<tr>
<td>DeleteLabel</td><td></td>
</tr>
<tr>
<td>DraftSeed</td><td></td>
</tr>
<tr>
<td>EditTitle</td><td></td>
</tr>
<tr>
<td>Mode</td><td></td>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td></td>
</tr>
</table>

**events**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>Cancelled</td><td>Emitted when the user cancels form editing.</td>
</tr>
<tr>
<td>Deleted</td><td>Emitted after a successful delete.</td>
</tr>
<tr>
<td>Saved</td><td>Emitted after a successful create or update.</td>
</tr>
</table>

#### MachinesListPanel

Managed by upsert-ngx-crud-kit (entity-pages template clone) for MachinesListPanel. Libelles francises le 2026-09-11.

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ActionLabel</td><td></td>
</tr>
<tr>
<td>PrimaryField</td><td></td>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SecondaryField</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td>Identifiant de la ligne selectionnee, pour surligner la ligne dans la liste.</td>
</tr>
<tr>
<td>Title</td><td></td>
</tr>
</table>

**events**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ItemSelected</td><td>Emitted when the user selects one row from the local list.</td>
</tr>
<tr>
<td>NewRequested</td><td>Emitted when the user wants to create a new row.</td>
</tr>
</table>

#### ModelesDetailCard

Managed by upsert-ngx-crud-kit (entity-pages template clone) for ModelesDetailCard. Libelles francises le 2026-09-11 (regenere).

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td></td>
</tr>
<tr>
<td>Title</td><td></td>
</tr>
</table>

#### ModelesEditForm

Managed by upsert-ngx-crud-kit (entity-pages template clone) for ModelesEditForm. Libelles francises le 2026-09-11 (regenere).

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ActionLabel</td><td></td>
</tr>
<tr>
<td>CreateTitle</td><td></td>
</tr>
<tr>
<td>DeleteLabel</td><td></td>
</tr>
<tr>
<td>DraftSeed</td><td></td>
</tr>
<tr>
<td>EditTitle</td><td></td>
</tr>
<tr>
<td>Mode</td><td></td>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td></td>
</tr>
</table>

**events**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>Cancelled</td><td>Emitted when the user cancels form editing.</td>
</tr>
<tr>
<td>Deleted</td><td>Emitted after a successful delete.</td>
</tr>
<tr>
<td>Saved</td><td>Emitted after a successful create or update.</td>
</tr>
</table>

#### ModelesListPanel

Managed by upsert-ngx-crud-kit (entity-pages template clone) for ModelesListPanel. Libelles francises le 2026-09-11.

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ActionLabel</td><td></td>
</tr>
<tr>
<td>PrimaryField</td><td></td>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SecondaryField</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td>Identifiant de la ligne selectionnee, pour surligner la ligne dans la liste.</td>
</tr>
<tr>
<td>Title</td><td></td>
</tr>
</table>

**events**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ItemSelected</td><td>Emitted when the user selects one row from the local list.</td>
</tr>
<tr>
<td>NewRequested</td><td>Emitted when the user wants to create a new row.</td>
</tr>
</table>

#### UtilisateursDetailCard

Managed by upsert-ngx-crud-kit (entity-pages template clone) for UtilisateursDetailCard. Libelles francises le 2026-09-11 (regenere).

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td></td>
</tr>
<tr>
<td>Title</td><td></td>
</tr>
</table>

#### UtilisateursEditForm

Managed by upsert-ngx-crud-kit (entity-pages template clone) for UtilisateursEditForm. Libelles francises le 2026-09-11 (regenere).

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ActionLabel</td><td></td>
</tr>
<tr>
<td>CreateTitle</td><td></td>
</tr>
<tr>
<td>DeleteLabel</td><td></td>
</tr>
<tr>
<td>DraftSeed</td><td></td>
</tr>
<tr>
<td>EditTitle</td><td></td>
</tr>
<tr>
<td>Mode</td><td></td>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td></td>
</tr>
</table>

**events**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>Cancelled</td><td>Emitted when the user cancels form editing.</td>
</tr>
<tr>
<td>Deleted</td><td>Emitted after a successful delete.</td>
</tr>
<tr>
<td>Saved</td><td>Emitted after a successful create or update.</td>
</tr>
</table>

#### UtilisateursListPanel

Managed by upsert-ngx-crud-kit (entity-pages template clone) for UtilisateursListPanel. Libelles francises le 2026-09-11.

**variables**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ActionLabel</td><td></td>
</tr>
<tr>
<td>PrimaryField</td><td></td>
</tr>
<tr>
<td>RefreshToken</td><td></td>
</tr>
<tr>
<td>SecondaryField</td><td></td>
</tr>
<tr>
<td>SelectedId</td><td>Identifiant de la ligne selectionnee, pour surligner la ligne dans la liste.</td>
</tr>
<tr>
<td>Title</td><td></td>
</tr>
</table>

**events**

<table>
<tr>
<th>name</th><th>comment</th>
</tr>
<tr>
<td>ItemSelected</td><td>Emitted when the user selects one row from the local list.</td>
</tr>
<tr>
<td>NewRequested</td><td>Emitted when the user wants to create a new row.</td>
</tr>
</table>



