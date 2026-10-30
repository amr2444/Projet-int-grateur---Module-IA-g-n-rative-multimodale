# MaintiDoc – Assistant documentaire multimodal et agentique pour la maintenance

Projet intégrateur du module **IA générative multimodale** (EMSI 2026, Pr. Mariam CHERRABI).

**Équipe ELBELLAOUI-ELYOUNESSI :** Amr EL BELLAOUI, Soulaimane ELYOUNESSI

## Objectif
MaintiDoc aide les techniciens de maintenance à répondre à des questions techniques (avec photo d'un panneau ou d'un équipement), en citant les pages et figures des manuels, en consultant l'historique des interventions via un outil MCP et en préparant des tickets créés uniquement après validation humaine. Périmètre : deux familles d'équipements fictifs, pompes centrifuges et compresseurs d'air.

## Structure du dépôt
```
.
├── README.md
├── .gitignore
├── docs/
│   ├── diagrammes/            sources des diagrammes (Mermaid)
│   ├── rapport/               sections du rapport du livrable 1 (Markdown)
│   └── journal_verification_corpus.md
├── corpus/
│   ├── inventaire.csv         registre des 42 documents
│   ├── prompts_corpus.md      prompts IA utilisés (P01 à P25)
│   ├── documents/famille_1/   pompes
│   ├── documents/famille_2/   compresseurs
│   └── images/                photos de terrain
└── tools/generation_corpus/   scripts de génération et de contrôle du corpus
```

## Avancement
- [x] Livrable 1 : cadrage, corpus, architecture, flux et accès (en cours : risques, planning)
- [ ] Livrable 2 : dépôt documenté et ingestion
- [ ] Livrables 3 à 6

Aucun secret (clé d'API, mot de passe) ne doit être commité : utiliser un fichier `.env` (ignoré par Git).
