# 5. Analyse des risques

## 5.1 Méthode

Chaque risque est noté selon deux critères, sur une échelle de 1 à 3 :
- la **probabilité** : 1 peu probable, 2 possible, 3 probable ;
- l'**impact** : 1 faible, 2 moyen, 3 fort.

Leur produit donne la **criticité**, de 1 à 9, qui fixe l'ordre de traitement. Les 15 risques identifiés couvrent les quatre volets demandés : technique (et IA), sécurité, données, organisation. Ils incluent les six risques imposés par la consigne : hallucination (R01), fuite entre groupes (R02), ticket non approuvé (R03), erreurs de l'IA dans le corpus (R05), licences (R06) et ressources matérielles (R07).

Chaque risque a un **responsable**, celui qui suit la mesure prévue. La répartition découle des rôles définis en partie 6.

> **Figure 5.1 – Matrice des risques** (`docs/diagrammes/matrice_risques.png`)

## 5.2 Registre des risques

| ID | Risque | Catégorie | P | I | Criticité | Mesure prévue | Responsable |
|---|---|---|---|---|---|---|---|
| R01 | Hallucination et citations non fondées | Technique (IA) | 3 | 3 | **9** | Citations limitées aux éléments réellement récupérés ; vérification PC4 (existence + soutien) ; abstention ou clarification si sources insuffisantes ; mesure en S5 (objectif ≥ 90 % de citations soutenant l'affirmation) | Soulaimane |
| R07 | Ressources matérielles insuffisantes (pas de GPU local, Colab limité) | Technique | 3 | 3 | **9** | Quantification 4 bits ; modèle 3B en repli ; Kaggle (quota GPU hebdomadaire) en complément de Colab ; limites de taille d'image et de contexte ; mise en cache des embeddings ; démonstration enregistrée en secours | Soulaimane |
| R02 | Fuite d'information entre groupes d'accès | Sécurité | 2 | 3 | **6** | Filtre groupes_acces dans la requête Qdrant (PC2) et non après coup ; revérification à l'ouverture (PC3) ; aucun cache partagé entre utilisateurs ; 20 scénarios de test d'accès en S5 | Amr |
| R03 | Création de ticket non approuvée ou en double | Sécurité | 2 | 3 | **6** | Jeton d'approbation signé (utilisateur + empreinte du contenu + expiration) ; contrôle côté serveur MCP (PC6) ; clé d'idempotence ; tests de rejeu et de double clic | Soulaimane |
| R04 | Injection de prompt via un document, une image OCR ou une réponse MCP | Sécurité | 2 | 3 | **6** | Contenus traités comme données (balisés, jamais comme instructions) ; outils en liste blanche ; aucune sortie réseau hors liste ; document piégé du corpus + 20 tests d'injection en S5 | Soulaimane |
| R05 | Erreurs introduites par l'IA dans le corpus | Données | 3 | 2 | **6** | Référentiel unique ; contrôle automatique check.py ; relecture humaine de chaque document (verifie_par) ; journal des erreurs (6 corrigées en S1) | Amr + Soulaimane |
| R11 | Fuite de secrets (clé d'API, jeton de tunnel, mot de passe) dans le dépôt | Sécurité | 2 | 3 | **6** | .env exclu par .gitignore ; secrets injectés à l'exécution ; analyse des secrets (gitleaks) avant chaque rendu ; jamais de secret dans un notebook partagé | Amr |
| R08 | Le VLM lit mal un voyant, une couleur ou un afficheur | Technique (IA) | 2 | 2 | **4** | Test sur les 6 photos dès S3 ; clarification si incertitude ; une ressemblance visuelle ne vaut pas diagnostic ; recoupement avec le code affiché et l'historique | Soulaimane |
| R09 | OCR erroné sur les documents scannés | Données | 2 | 2 | **4** | Modèle OCR français (Tesseract fra ou PaddleOCR, comparés en S2) ; score de confiance conservé dans les métadonnées ; image de la page transmise au VLM en complément | Amr |
| R10 | Réponse fondée sur une version obsolète d'une procédure | Données | 2 | 2 | **4** | Métadonnée version ; règle : citer les deux versions, signaler l'écart, privilégier la plus récente ; tests sur les 2 paires contradictoires | Amr |
| R12 | Latence supérieure au budget (60 s) sur un GPU T4 | Technique | 2 | 2 | **4** | Mesure dès S3 ; limiter les appels au modèle (≤ 6) et la taille du contexte ; vLLM si compatible ; réponses courtes | Soulaimane |
| R13 | Retard dû à la charge (équipe de 2, autres modules) | Organisation | 2 | 2 | **4** | Planning avec marge ; priorité au scénario de démonstration (version minimale d'abord) ; point d'avancement hebdomadaire ; fonctionnalités secondaires en option | Amr + Soulaimane |
| R14 | Dépendance à un seul membre sur une partie critique | Organisation | 2 | 2 | **4** | Revue croisée de chaque fusion de branche ; README et documentation à jour ; chacun sait lancer tout le prototype | Amr + Soulaimane |
| R06 | Licences des documents et des modèles | Données / juridique | 1 | 2 | **2** | Corpus 100 % synthétique (aucun document tiers) ; licences des modèles et bibliothèques vérifiées et figées dans le dépôt en S2 (la licence du modèle de repli 3B peut différer de celle du 7B) | Amr |
| R15 | Adaptation du reranker sans gain mesurable | Technique (IA) | 2 | 1 | **2** | Comparaison honnête sans reranker / reranker d'origine / reranker adapté ; séparation des données par document ; résultat négatif rapporté tel quel | Amr |

## 5.3 Lecture du registre

**Les deux risques les plus critiques (criticité 9)** sont l'hallucination (R01) et le manque de ressources GPU (R07). Ils conditionnent directement la démonstration :
- R01 est traité **par l'architecture**, et pas seulement par le prompt : les citations sont limitées aux éléments réellement récupérés, puis vérifiées (PC4). Faute de source suffisante, le système s'abstient.
- R07 est traité **dès les semaines 2 et 3** par un test de chargement du modèle sur Colab, avant d'écrire le reste du pipeline. Si le 7B ne tient pas, nous basculons tôt sur le 3B, plutôt que de le découvrir en semaine 6.

**Les risques de sécurité (R02, R03, R04, R11)** ont un impact fort, mais une probabilité contenue par des contrôles faits **dans le code, hors du modèle** : filtre d'accès avant la recherche, jeton d'approbation vérifié par le serveur MCP, liste blanche d'outils, secrets hors du dépôt. Chacun sera vérifié par des scénarios de test dédiés en semaine 5. Ces scénarios s'appuient sur le corpus : 3 documents réservés, 1 document piégé.

**R05 (erreurs de l'IA dans le corpus)** n'est pas théorique : il s'est déjà produit 6 fois en semaine 1 (journal E01 à E06). C'est pour cela que nous l'avons noté « probable ».

**Les risques d'organisation (R13, R14)** sont traités en livrant d'abord une **version minimale de bout en bout** : question, recherche, réponse citée. On l'enrichit ensuite.

Le registre est versionné dans le dépôt et relu chaque semaine. Les mesures de la semaine 5 permettront de confirmer ou d'infirmer les probabilités estimées ici.
