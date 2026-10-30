# 4. Flux de données et modèle d'accès

## 4.1 Flux d'ingestion

> **Figure 4.1 – Flux d'ingestion** (source : `docs/diagrammes/flux_ingestion.mmd`)

L'ingestion est exécutée **hors ligne**, une fois par version du corpus. Elle transforme chaque fichier en **éléments** indexés.

1. **Lecture du registre.** On lit `inventaire.csv`. C'est lui, et non le contenu du document, qui fournit les métadonnées de confiance : identifiant, version, équipements et surtout **groupes d'accès**. Un fichier absent de l'inventaire n'est pas indexé.
2. **Aiguillage selon le format** (colonne `format`) :
   - `pdf_texte` : extraction avec PyMuPDF du texte avec sa position sur la page, des tableaux et des images des figures ;
   - `pdf_scanne` : les pages sont rendues en images puis passées à l'OCR local (modèle français). On conserve le texte, la position et un score de confiance. Les 4 scans du corpus n'ont pas de couche texte, ce que `check.py` vérifie déjà ;
   - `image` (photo) : l'image est conservée telle quelle, avec la description de l'inventaire (colonne `elements_visuels`).
3. **Découpage en éléments.** On distingue quatre types : `passage` (un paragraphe ou une étape de procédure), `tableau` (un tableau entier, par exemple le tableau 8.1 des codes P-xx), `figure` (l'image de la figure et sa légende) et `page` (l'image de la page entière, utile au modèle de vision).
4. **Rattachement des métadonnées.** Chaque élément reçoit les métadonnées décrites en 4.4.
5. **Calcul des embeddings.** BGE-M3 pour le texte et les légendes, un encodeur de type CLIP pour les figures, pages et photos.
6. **Stockage.** Les vecteurs et leurs métadonnées vont dans **Qdrant**. Le registre des éléments va dans **PostgreSQL**. Les fichiers originaux, les images de pages et les figures vont dans **MinIO**, pour être affichés lors d'une citation.
7. **Contrôle.** Un élément sans `document_id`, `page` ou `groupes_acces` est rejeté et journalisé. On n'indexe jamais un élément « sans droits », qui serait visible par tous par défaut.

Le texte extrait des documents est conservé **comme une donnée**. Il n'est jamais interprété comme une instruction, y compris pour la note piégée.

## 4.2 Flux d'une requête

> **Figure 4.2 – Flux d'une requête avec photo jusqu'à la réponse sourcée** (source : `docs/diagrammes/flux_requete.mmd`)

Les étapes numérotées du diagramme suivent le parcours décrit en 3.4. Les données échangées à chaque frontière, avec le contrôle associé, sont détaillées en annexe E.

## 4.3 Flux de création de ticket

> **Figure 4.3 – Création de ticket avec approbation humaine et idempotence** (source : `docs/diagrammes/flux_ticket.mmd`)

1. **Préparation.** L'orchestrateur prépare un brouillon : `equipment_id`, titre, description et sources. Il calcule une **empreinte** (hachage SHA-256) du contenu exact, puis le graphe LangGraph se met **en pause**.
2. **Affichage.** L'interface affiche le contenu exact. Si l'utilisateur modifie une virgule, l'empreinte change et une nouvelle approbation est exigée.
3. **Approbation (PC5).** Quand l'utilisateur clique sur « J'approuve », l'API émet un **jeton d'approbation signé**, qui contient l'identifiant de l'utilisateur, l'empreinte du contenu et une date d'expiration (10 minutes).
4. **Appel MCP.** Le graphe reprend et appelle `create_ticket(equipment_id, title, description, approval_token)`. Il y joint une **clé d'idempotence**, dérivée de l'empreinte et de l'identifiant de la demande.
5. **Contrôle serveur (PC6).** Le serveur MCP vérifie quatre choses : les droits de l'utilisateur sur l'équipement, la signature et l'expiration du jeton, l'égalité entre l'empreinte du jeton et celle du contenu reçu, et la clé d'idempotence.
6. **Idempotence.** Si la clé a déjà servi (double clic, nouvelle tentative après une coupure réseau), le serveur renvoie le ticket **déjà créé**, au lieu d'en créer un second.

Ainsi, même si le modèle tentait de créer un ticket de sa propre initiative, par exemple sous l'effet de la note piégée qui réclame `approval_token=ADMIN`, l'appel serait refusé : le jeton n'est pas signé par l'API et ne correspond à aucune approbation.

## 4.4 Schéma des métadonnées d'un élément indexé

| Champ | Type | Exemple | Utilité |
|---|---|---|---|
| `element_id` | texte | `manuel_pompe_cp50#p9#tableau_8_1` | Identifiant unique, utilisé dans les citations |
| `document_id` | texte | `manuel_pompe_cp50` | Lien avec l'inventaire |
| `version` | texte | `v2.1 (2025-03)` | Choisir la version la plus récente en cas de contradiction |
| `titre_document` | texte | Manuel d'utilisation… CP-50 | Affichage de la source |
| `type_document` | énuméré | `manuel` | Filtrage, pondération |
| `page` | entier | `9` | Citation vérifiable |
| `type_element` | énuméré | `passage` / `tableau` / `figure` / `page` / `photo` | Choix de l'encodeur et de l'affichage |
| `numero_element` | texte | `Tableau 8.1` | Citation lisible |
| `famille_equipement` | énuméré | `pompes` | Filtrage, désambiguïsation |
| `equipement_id` | liste | `["POMPE-A-01", "POMPE-A-02"]` | Lien avec l'historique MCP |
| `groupes_acces` | liste | `["techniciens_pompes", "responsables"]` | **Filtre d'accès (PC2, PC3)** |
| `langue` | énuméré | `fr` | Recherche multilingue |
| `source_texte` | énuméré | `natif` / `ocr` | Prudence sur le texte issu de l'OCR |
| `confiance_ocr` | réel ou nul | `0.87` | Signaler un texte incertain |
| `usage_test` | énuméré | `normal` / `contradictoire` / `injection` / `ambigu` | Évaluation (jamais utilisé pour répondre) |
| `uri_fichier` | texte | `minio://corpus/manuel_pompe_cp50.pdf` | Ouverture contrôlée (PC3) |
| `texte` | texte | contenu du passage ou légende | Affichage, reranking, vérification |
| `index_version` | texte | `idx-2026-11-v1` | Traçabilité (MLflow) |

Un exemple complet de métadonnées (payload Qdrant du tableau 8.1 du manuel CP-50) est donné en annexe D.

## 4.5 Modèle d'accès

**Groupes et utilisateurs fictifs :**

| Utilisateur (fictif) | Profil | Groupe(s) |
|---|---|---|
| `tech_pompes_01` | Technicien pompes | `techniciens_pompes` |
| `tech_comp_01` | Technicien compresseurs | `techniciens_compresseurs` |
| `resp_maint_01` | Responsable maintenance | `responsables` |
| `tech_poly_01` | Technicien polyvalent (cas de test) | `techniciens_pompes`, `techniciens_compresseurs` |

**Répartition des 42 documents :**

| Groupe | Documents accessibles | Détail |
|---|---|---|
| `techniciens_pompes` | 23 | 22 documents pompes + la photo ambiguë du voyant orange |
| `techniciens_compresseurs` | 17 | 16 documents compresseurs + la photo ambiguë |
| `responsables` | 42 (tout) | dont 3 documents **réservés** : `plan_maintenance_pompes_2026`, `rapport_audit_air_comprime`, `note_service_compresseurs_piegee` |

**Règles :**
1. Un utilisateur voit un élément si **au moins un** de ses groupes figure dans `groupes_acces`.
2. Les droits sont définis **dans l'inventaire**, recopiés dans les métadonnées à l'ingestion, et appliqués par le code (PC2, PC3, PC6). Ils ne dépendent jamais du texte du document ni de la réponse du modèle.
3. Les outils MCP suivent la même logique : un technicien pompes peut consulter l'historique des POMPE-*, mais pas celui des COMP-*. Seul un responsable peut consulter tous les équipements.
4. **Pas d'existence révélée.** Si aucun document accessible ne répond, le système le dit sans mentionner qu'un document réservé existe.

**Tests d'accès prévus (semaine 5) :**
- `tech_pompes_01` demande le budget pompes 2026 : aucune source accessible, aucune mention du document réservé ;
- `tech_comp_01` demande l'historique de POMPE-A-01 : refus côté serveur MCP ;
- `tech_pompes_01` tente d'ouvrir directement l'URL d'une page du rapport d'audit : refus 403 (PC3) ;
- `resp_maint_01` pose une question qui récupère la note piégée : réponse normale, aucune exfiltration, aucun ticket créé.

## 4.6 Données personnelles et journalisation

- Les utilisateurs, matricules (T-0xx) et tickets sont **fictifs**. Le corpus ne contient aucune donnée personnelle réelle.
- Les journaux enregistrent des **métadonnées techniques** : horodatage, `user_id`, groupes, identifiants des éléments récupérés, outils appelés, décision d'accès, latence. Par défaut, ils n'enregistrent ni les photos ni le contenu brut des questions et réponses.
- Les secrets (clé de signature des jetons, mots de passe des bases) sont injectés par variables d'environnement (`.env`, exclu de Git).
