# 6. Planning et organisation de l'équipe

## 6.1 Équipe et répartition des rôles

L'équipe compte deux membres. Chacun est **propriétaire** de blocs de l'architecture : il les conçoit, les code, les teste et les documente. L'autre membre relit systématiquement son travail. L'évaluation, le rapport et la démonstration sont réalisés en commun.

| | **Amr EL BELLAOUI** | **Soulaimane ELYOUNESSI** |
|---|---|---|
| Rôle principal | Données et recherche, API et interface | Modèle, orchestration et outils |
| Blocs de l'architecture | 8. Ingestion (PyMuPDF, OCR) · 5. Recherche documentaire (Qdrant, embeddings, RRF, reranker) · 2. API (authentification, groupes, PC1, PC3) · 1. Interface Streamlit | 4. Modèle vision-langage (Colab / Kaggle) · 3. Orchestrateur LangGraph (budgets, interruption) · 6. Vérification des citations (PC4) · 7. Serveur et client MCP (PC5, PC6) |
| Responsabilités transverses | Contrôle d'accès (PC2), gestion des secrets, licences, Docker Compose | Sécurité du workflow (PC7), tests d'injection, prompts versionnés |
| Livrable 1 | Corpus famille pompes (relecture de 23 documents), architecture, flux | Corpus famille compresseurs (relecture de 19 documents), risques, planning |
| En commun | Jeu de test et évaluation (S5), fiche de limites, rapport, démonstration | (idem) |

## 6.2 Hypothèses de charge

- **Environ 10 h par personne et par semaine**, soit une capacité d'environ 100 h pour les semaines 2 à 6.
- **GPU** : uniquement Colab et Kaggle gratuits, avec des sessions limitées et des interruptions possibles. Les tâches GPU sont regroupées et préparées à l'avance (notebooks prêts, données en cache).
- **Marge** : environ 15 % du temps n'est pas affecté, pour absorber les imprévus (installation, quotas GPU, autres modules).

## 6.3 Planning des semaines 2 à 6

> **Figure 6.1 – Diagramme de Gantt des semaines 2 à 6** (source : `docs/diagrammes/planning.mmd`)
> Les tâches en rouge sont critiques : si elles glissent, tout le planning glisse.

| Semaine | Objectif | Amr | Soulaimane | Livrable / jalon |
|---|---|---|---|---|
| **S2** (2–8 nov.) | Ingestion, recherche, accès | Environnement Docker Compose, versions et licences figées ; ingestion PyMuPDF + OCR (comparaison Tesseract `fra` / PaddleOCR) ; index Qdrant texte et image avec filtre `groupes_acces` | **Test de chargement Qwen2.5-VL 7B (4 bits) puis 3B sur Colab** : mémoire, latence, lecture des 6 photos. Décision 7B ou 3B | L2 : dépôt documenté, ingestion reproductible |
| **S3** (9–15 nov.) | VLM, citations, sorties structurées | API FastAPI : authentification, groupes, ouverture contrôlée des sources (PC3) | Analyse de photo et rédaction sourcée ; vérification des citations (PC4) ; schéma Pydantic ; prompts versionnés `answer_v1`, `visual_analysis_v1`, `evidence_check_v1` | L3 : question + photo → réponse citant page et figure |
| **S4** (16–22 nov.) | Workflow, MCP, validation humaine | Interface Streamlit : réponse sourcée, sources cliquables, écran d'approbation ; début des données du reranker | Graphe LangGraph (états, budgets, interruption) ; serveur MCP (3 outils, historiques du corpus) ; jeton d'approbation et idempotence | Prototype complet de bout en bout |
| **S5** (23–29 nov.) | Reranker, évaluation, sécurité | Adaptation du reranker (800 à 1 500 exemples, séparation par document) ; comparaison sans / d'origine / adapté (nDCG@5, MRR@10) | Tests de sécurité : 20 tests d'accès et de validation, 20 tests d'injection | Jeu de test d'environ 150 scénarios, évaluation, fiche de limites |
| **S6** (30 nov.–6 déc.) | Déploiement et soutenance | Optimisations, Docker Compose final, README | Mesures de latence (médiane, p95), mémoire GPU, MLflow | L6 : démonstration (scénario nominal, ambiguïté, injection, accès refusé, approbation) |

**Chemin critique.** Le test du modèle en S2 conditionne tout le reste : la taille du contexte, la latence et la qualité de lecture des photos en dépendent. C'est pourquoi il est placé en **tout premier** (risque R07). Le second point critique est la **démonstration finale**. Une version enregistrée sera préparée en secours si Colab est indisponible le jour de la soutenance.

**Version minimale d'abord.** À la fin de S3, une chaîne simple doit fonctionner de bout en bout, même imparfaite : question, recherche filtrée, réponse citée. Les semaines suivantes l'enrichissent. Cela limite le risque d'arriver en S6 avec des blocs excellents mais non intégrés (risques R13 et R14).

## 6.4 Organisation du travail

- **Git.** Une branche par fonctionnalité, fusionnée dans `main` par une *pull request* relue par l'autre membre. Aucun secret commité (`.env` exclu par `.gitignore`).
- **Suivi.** Point hebdomadaire de 30 minutes (avancement, blocages, mise à jour des risques et du planning) ; issues GitHub pour les tâches et les bugs ; questions à l'enseignante posées avant le milieu de chaque semaine.
- **Traçabilité.** Prompts versionnés dans `prompts/`, expériences dans MLflow, corpus et scripts dans `corpus/` et `tools/`.
