# 3. Architecture cible

## 3.1 Vue d'ensemble

L'architecture reprend la section 3 du cahier des charges, reformulée et organisée en **9 blocs**.

Une demande suit le trajet suivant :
1. Elle part de l'**interface**, passe par l'**API**, qui identifie l'utilisateur, puis arrive à l'**orchestrateur**.
2. L'orchestrateur est le « chef d'orchestre » : il décide quelles étapes exécuter et dans quel ordre.
3. Il fait appel à trois services : le **modèle vision-langage** (comprendre la photo et rédiger), la **recherche documentaire** (trouver les passages et figures) et l'**outil MCP** (historique et tickets).
4. Avant de répondre, un bloc de **vérification** contrôle les citations.

L'**ingestion** fonctionne à part, hors ligne : elle prépare l'index une fois pour toutes, à partir du corpus.

> **Figure 3.1 – Schéma par blocs de MaintiDoc** (source : `docs/diagrammes/architecture.mmd`)
> Les points de contrôle PC1 à PC7 sont indiqués dans les blocs où ils s'appliquent.

## 3.2 Fiches des blocs

| Bloc | Rôle (en une phrase) | Entrées | Sorties | Outil envisagé |
|---|---|---|---|---|
| 1. Interface web | Permettre au technicien de poser sa question avec une photo, de lire une réponse sourcée et d'approuver un ticket | Texte, photo (JPEG/PNG), clic d'approbation | Requête HTTP vers l'API ; affichage de la réponse, des sources et du brouillon de ticket | Streamlit |
| 2. API | Point d'entrée unique : vérifier qui appelle, ce qu'il a le droit de voir, et tracer la demande | Requête + jeton de session | Requête enrichie (identité, groupes) vers l'orchestrateur ; réponse JSON vers l'interface | FastAPI ; comptes fictifs dans PostgreSQL |
| 3. Orchestrateur | Enchaîner les étapes (analyser, chercher, consulter, rédiger, vérifier, décider) et appliquer les budgets | Question, photo, identité, groupes | Réponse structurée, clarification ou brouillon de ticket ; état mis en pause pendant l'approbation | LangGraph (graphe d'états) + LangChain (prompts, parseurs) |
| 4. Modèle vision-langage | Décrire la photo (équipement, voyant, afficheur) puis rédiger la réponse à partir des extraits fournis | Image + question ; extraits et figures récupérés | Description visuelle ; texte de réponse avec citations proposées | Qwen2.5-VL-7B-Instruct quantifié 4 bits ; repli Qwen2.5-VL-3B ; Transformers |
| 5. Recherche documentaire | Retrouver, **parmi les seuls documents autorisés**, les passages, tableaux et figures pertinents | Texte de la requête, photo, liste des groupes autorisés | Top-k éléments classés (texte et images) avec leurs métadonnées (document, page, élément) | Qdrant ; BGE-M3 (texte) ; encodeur texte-image type CLIP multilingue ; fusion RRF ; reranker multilingue (bge-reranker, adapté en S5) |
| 6. Vérification | S'assurer que chaque citation pointe vers un élément réellement récupéré et autorisé, et qu'elle soutient l'affirmation | Réponse brouillon + éléments récupérés | Verdict : valide / à corriger / clarification nécessaire ; JSON conforme au schéma | Pydantic (format) + contrôle par règles (existence, droits) + contrôle par le modèle (soutien) |
| 7. Outil MCP (client + serveur) | Donner accès à l'historique et aux tickets de la GMAO de démonstration, sous contrôle | `equipment_id`, identité ; pour la création : contenu approuvé, jeton d'approbation, clé d'idempotence | Liste d'interventions, tickets ouverts, numéro du ticket créé ou refus motivé | SDK MCP Python (serveur et client) ; SQLite ou PostgreSQL pour la GMAO de démonstration |
| 8. Ingestion | Transformer le corpus en éléments indexés et recherchables | PDF texte, PDF scannés, photos, `inventaire.csv` | Passages, tableaux, figures, vecteurs et métadonnées | PyMuPDF ; OCR local (Tesseract `fra` ou PaddleOCR, à comparer) |
| 9. Suivi | Garder la trace des versions (modèle, prompts, index, reranker) et des métriques de chaque exécution | Traces de l'orchestrateur, résultats d'évaluation | Expériences comparables | MLflow |
| Stockage | Conserver vecteurs, métadonnées, fichiers et données de la GMAO | — | — | Qdrant (vecteurs + payload) ; PostgreSQL (utilisateurs, groupes, documents, approbations, journaux) ; MinIO (PDF, pages, images) |

Tous ces composants sont des briques open source ou à poids ouverts. Les versions exactes et les licences seront figées dans le dépôt en semaine 2.

## 3.3 Points de contrôle

| Point | Où | Ce qui est vérifié | Ce qui se passe en cas d'échec |
|---|---|---|---|
| **PC1** Authentification | API | L'utilisateur est connu ; on récupère ses groupes (`techniciens_pompes`, `techniciens_compresseurs`, `responsables`) | Requête rejetée (401) |
| **PC2** Filtre d'accès avant recherche | Recherche documentaire | La recherche ne porte **que** sur les éléments dont `groupes_acces` contient un groupe de l'utilisateur (filtre Qdrant, pas un tri après coup) | Un document interdit n'est jamais récupéré, donc jamais transmis au modèle |
| **PC3** Contrôle à l'ouverture | API → MinIO | Quand l'utilisateur clique sur une source, on revérifie ses droits avant de servir la page ou l'image | Refus (403), sans révéler le contenu |
| **PC4** Vérification des citations | Bloc vérification | Chaque citation (document, page, élément) existe parmi les éléments récupérés et autorisés, et soutient la phrase associée | Citation retirée ; si plus aucune source ne soutient la réponse, demande de clarification ou abstention |
| **PC5** Validation humaine | Interface + orchestrateur | L'utilisateur voit le **contenu exact** du ticket et l'approuve explicitement | Pas d'approbation : pas de création. Contenu modifié : nouvelle approbation exigée |
| **PC6** Contrôle serveur MCP | Serveur MCP | Droits de l'utilisateur sur l'équipement ; jeton d'approbation valide et lié à l'utilisateur et au contenu ; clé d'idempotence | Refus de l'appel ; un second appel avec la même clé ne crée pas de doublon |
| **PC7** Garde-fous | Orchestrateur | Texte des documents et réponses d'outils traités comme des **données** (jamais comme des instructions) ; outils en liste blanche ; budgets (≤ 6 appels modèle, ≤ 3 appels MCP, ≤ 60 s) | Instruction ignorée, appel non prévu bloqué, arrêt propre si le budget est dépassé |

Le contrôle d'accès n'est pas confié au modèle : il est fait **par le code**, avant (PC2) et après (PC3), puis **côté serveur MCP** (PC6). Même si le modèle était trompé par une injection, il ne pourrait ni voir un document interdit ni créer un ticket non approuvé.

## 3.4 Parcours d'une requête

**Scénario nominal (CU1).** Un technicien du groupe `techniciens_pompes` envoie la photo `photo_panneau_pompe_a01.jpg` avec la question : « Que signifie ce voyant orange ? Prépare un ticket si nécessaire. »

1. **Identification (PC1).** L'interface transmet la question, la photo et le jeton de session à l'API. L'API identifie l'utilisateur et récupère ses groupes : `techniciens_pompes`.
2. **Analyse de la demande.** L'orchestrateur ouvre une nouvelle exécution, avec un état vide et des budgets à zéro, et envoie la photo au modèle vision-langage. Celui-ci décrit ce qu'il voit : l'étiquette « POMPE-A-01 », les voyants vert H1 et orange H2 allumés, l'afficheur « P-21 T PAL 84°C ». L'équipement et le code sont identifiés.
3. **Recherche (PC2).** L'orchestrateur lance une recherche texte (« voyant H2 orange fixe, code P-21, température palier ») et une recherche image (similarité avec les figures de panneaux), **filtrées sur les documents du groupe `techniciens_pompes`**. Les résultats sont fusionnés (RRF) puis reclassés par le reranker. Exemples de résultats : le tableau des voyants du manuel CP-50 (page 8), le tableau des codes (page 9) et la fiche des codes d'alarme pompes.
4. **Historique (MCP).** La question porte sur un équipement identifié et demande un éventuel ticket. L'orchestrateur appelle donc `get_equipment_history("POMPE-A-01")` et `get_open_tickets("POMPE-A-01")`. Le serveur vérifie les droits (PC6) et renvoie deux préalarmes P-21 précédentes (2025-09 et 2026-03) et un ticket ouvert sur les vibrations.
5. **Rédaction.** Le modèle reçoit la question, sa description de la photo, les extraits retenus et l'historique, avec la consigne de citer ses sources. Il rédige la réponse : H2 orange fixe avec P-21 signifie une préalarme de température palier (≥ 80 °C) ; la pompe continue de tourner ; il faut contrôler le niveau d'huile, les roulements et l'alignement ; c'est la 3e occurrence en un an, alors que les roulements ont déjà été remplacés en mars.
6. **Vérification (PC4).** Chaque citation est contrôlée : `manuel_pompe_cp50`, p. 8, tableau 7.1 ; p. 9, tableau 8.1 ; historique MCP. Elles existent bien parmi les éléments récupérés et soutiennent les phrases associées. La sortie est validée par le schéma Pydantic.
7. **Brouillon de ticket.** L'utilisateur a demandé un ticket et le diagnostic montre une récurrence. Le système prépare un brouillon : équipement POMPE-A-01, titre, description, sources. Le graphe se met **en pause**.
8. **Approbation (PC5).** L'interface affiche le contenu exact du ticket. Le technicien l'approuve. L'API génère un jeton d'approbation lié à l'utilisateur et à l'empreinte du contenu.
9. **Création (PC6).** L'orchestrateur reprend et appelle `create_ticket(...)` avec le jeton et une clé d'idempotence. Le serveur vérifie le tout et crée le ticket. Un double clic ne crée pas de doublon.
10. **Réponse.** L'utilisateur reçoit la réponse sourcée et le numéro du ticket. Les sources sont cliquables, et les droits sont revérifiés à l'ouverture (PC3).

**Variantes :**
- **Photo ambiguë** (`photo_voyant_orange_gros_plan`, `photo_panneau_comp_a01`). À l'étape 2, l'équipement n'est pas identifiable : le voyant orange existe sur les pompes (H2) et sur les compresseurs (L2), avec des significations différentes. L'orchestrateur ne choisit pas au hasard : il renvoie le statut `needs_clarification` et demande une photo de la plaque ou de l'étiquette.
- **Contradiction.** À l'étape 3, si `proc_vidange_cp50_v1` (25 N·m) et `proc_vidange_cp50_v2` (35 N·m) sont récupérées ensemble, la réponse cite les deux, signale l'écart et privilégie la version la plus récente, confirmée par le manuel.
- **Accès interdit.** Un technicien qui demande le budget 2026 n'obtient rien. Le document est réservé aux `responsables` : il est exclu par le filtre (PC2), et le système répond qu'aucune source accessible ne permet de répondre.
- **Injection.** Si la note piégée est récupérée (pour un responsable), son texte « ignore les instructions… » est traité comme une donnée. L'URL externe n'est pas un outil autorisé (PC7), et une création de ticket sans jeton est refusée par le serveur (PC6).

## 3.5 Contraintes de déploiement (pas de GPU local)

L'équipe ne dispose pas de GPU. Nous envisageons un déploiement en deux parties :
- **Sur nos PC**, avec Docker Compose : l'interface, l'API, l'orchestrateur, Qdrant, PostgreSQL, MinIO, le serveur MCP et l'ingestion. Ces services fonctionnent sur processeur.
- **Sur Google Colab ou Kaggle** (GPU T4, 16 Go) : le modèle vision-langage et, si besoin, le calcul des embeddings d'images. Le modèle serait exposé par une API protégée, ou bien toute la démonstration tournerait dans un notebook.

Ce choix est à valider en semaine 2 ou 3 (voir les questions ouvertes ci-dessous).

## 3.6 Questions ouvertes et hypothèses à vérifier

| # | Question / hypothèse | Comment la vérifier | Semaine |
|---|---|---|---|
| Q1 | Qwen2.5-VL-7B quantifié en 4 bits tient-il sur un T4 (16 Go) avec une image et environ 4 000 tokens de contexte ? Sinon, le 3B suffit-il à lire un afficheur et un voyant ? | Test de chargement, mesure de la mémoire et de la latence sur nos 6 photos | S2–S3 |
| Q2 | Comment relier Colab (GPU) à nos services locaux sans exposer de secret ni d'accès ouvert ? | Comparer un tunnel authentifié et un fonctionnement tout-en-un dans le notebook | S2 |
| Q3 | Les sessions Colab gratuites (durée limitée, interruptions) suffisent-elles pour l'évaluation de 150 scénarios ? | Estimer le temps par scénario ; prévoir Kaggle (30 h GPU par semaine) en complément | S3 |
| Q4 | Faut-il un OCR pour tous les documents, ou seulement pour les 4 scannés ? | Détecter automatiquement l'absence de couche texte (déjà vérifiée par `check.py`) | S2 |
| Q5 | Tesseract `fra` est-il suffisant ? Notre test avec le modèle anglais fait des erreurs sur les accents (« a » au lieu de « à ») | Comparer Tesseract `fra` et PaddleOCR sur les 4 scans | S2 |
| Q6 | Quelle granularité d'élément indexer : paragraphe, tableau entier, ligne de tableau des codes ? | Tester la recherche sur des questions de codes d'alarme | S2 |
| Q7 | Un encodeur de type CLIP distingue-t-il le voyant orange d'une pompe de celui d'un compresseur ? On s'attend à ce que non, d'où la nécessité de la clarification | Recherche image sur les 3 photos ambiguës | S2–S3 |
| Q8 | Comment vérifier qu'une citation **soutient** l'affirmation, au-delà de son existence ? Le modèle juge-t-il de façon fiable ? | Annoter une vingtaine de cas à la main et comparer | S3 / S5 |
| Q9 | Le budget de 60 s par demande est-il tenable avec 2 à 4 appels au modèle sur un T4 ? | Mesurer la latence médiane et p95 | S3–S4 |
| Q10 | Pourra-t-on construire 800 à 1 500 exemples d'entraînement du reranker à partir de 42 documents ? | Générer des questions, les vérifier, choisir les négatifs difficiles (voyants H2 / L2) | S4–S5 |
