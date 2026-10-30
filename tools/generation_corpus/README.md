# Génération du corpus synthétique

Scripts utilisés (avec Claude Opus 5.5, voir `corpus/prompts_corpus.md`) pour produire le corpus.
À exécuter depuis ce dossier :

```bash
pip install -r requirements.txt
python figures.py                    # schémas -> build/fig/
python build.py docs_f1 docs_f2      # PDF (+ versions scannées)
python photos.py                     # photos synthétiques
python inventaire.py                 # corpus/inventaire.csv
python check.py                      # contrôles de cohérence
```

- `ref.py` : référentiel unique (équipements, codes d'alarme, historiques) : source de vérité.
- `check.py` : vérifie fichiers ↔ inventaire, pages, formats, codes et équipements cités, historiques ↔ MCP.
