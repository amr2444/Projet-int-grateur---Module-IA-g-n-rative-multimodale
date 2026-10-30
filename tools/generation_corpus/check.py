"""Contrôles automatiques de cohérence du corpus MaintiDoc.
1. Fichiers <-> inventaire (dans les deux sens), nommage <document_id>.<ext>
2. nb_pages de l'inventaire = pages réelles des PDF
3. Valeurs autorisées (type, format, langue, usage_test, groupes, familles)
4. PDF « scannés » sans couche texte ; PDF texte avec couche texte
5. Équipements cités = équipements du référentiel ; codes d'alarme cités = codes définis
6. Historiques : identifiants INT- présents dans le PDF = référentiel MCP
7. Exigences de la consigne (volume, visuels, scannés, contradictoires, injection)"""
import csv, os, re, subprocess, sys
from pypdf import PdfReader
sys.path.insert(0, ".")
from ref import EQUIPEMENTS, CODES_POMPES, CODES_VS37, CODES_PS11, HISTORIQUES

ROOT = sys.argv[1] if len(sys.argv) > 1 else "../../corpus"
rows = list(csv.DictReader(open(f"{ROOT}/inventaire.csv", encoding="utf-8")))
err, warn = [], []
ok = lambda c, msg: None if c else err.append(msg)

# 1. fichiers <-> inventaire
files = {os.path.relpath(os.path.join(dp, f), ROOT) for dp, _, fs in os.walk(ROOT) for f in fs
         if not f.endswith((".csv", ".md"))}
inv = {r["fichier"] for r in rows}
for f in files - inv: err.append(f"Fichier absent de l'inventaire : {f}")
for f in inv - files: err.append(f"Ligne d'inventaire sans fichier : {f}")
ids = [r["document_id"] for r in rows]
ok(len(ids) == len(set(ids)), "document_id en double")
for r in rows:
    ok(os.path.splitext(os.path.basename(r["fichier"]))[0] == r["document_id"], f"Nom de fichier ≠ document_id : {r['fichier']}")
    ok(re.fullmatch(r"[a-z0-9_]+", r["document_id"]) is not None, f"document_id invalide : {r['document_id']}")

ALLOWED = dict(type_document={"manuel", "procedure", "fiche_securite", "schema", "codes_alarme", "photo", "historique"},
               format={"pdf_texte", "pdf_scanne", "image"}, langue={"fr", "en"}, usage_test={"normal", "contradictoire", "injection", "ambigu"},
               famille_equipement={"pompes", "compresseurs"}, genere_par_ia={"oui", "non"})
GROUPS = {"techniciens_pompes", "techniciens_compresseurs", "responsables"}
codes = {c[0] for c in CODES_POMPES + CODES_VS37 + CODES_PS11}

for r in rows:
    p = os.path.join(ROOT, r["fichier"])
    for k, allowed in ALLOWED.items():
        ok(r[k] in allowed, f"{r['document_id']} : valeur {k}={r[k]!r} non autorisée")
    for g in r["groupe_acces"].split(" ; "): ok(g in GROUPS, f"{r['document_id']} : groupe inconnu {g}")
    for e in r["equipement_id"].split(" ; "): ok(e in EQUIPEMENTS, f"{r['document_id']} : équipement inconnu {e}")
    ok(bool(r["verifie_par"]), f"{r['document_id']} : verifie_par vide")
    if r["format"] != "image":
        n = len(PdfReader(p).pages)
        ok(n == int(r["nb_pages"]), f"{r['document_id']} : nb_pages {r['nb_pages']} ≠ {n} réelles")
        txt = subprocess.run(["pdftotext", p, "-"], capture_output=True, text=True).stdout
        if r["format"] == "pdf_scanne":
            ok(len(txt.strip()) == 0, f"{r['document_id']} : PDF scanné contenant une couche texte")
        else:
            ok(len(txt.strip()) > 200, f"{r['document_id']} : PDF texte sans texte extractible")
            for e in set(re.findall(r"\b(?:POMPE|COMP)-[A-Z]-\d{2}\b", txt)):
                ok(e in EQUIPEMENTS, f"{r['document_id']} : cite un équipement inexistant {e}")
            for c in set(re.findall(r"(?<![-\w])[PAB]-\d{2}\b", txt)):
                ok(c in codes, f"{r['document_id']} : cite un code d'alarme non défini {c}")
            if r["type_document"] == "historique":
                eq = r["equipement_id"]
                want = {h[0] for h in HISTORIQUES[eq]}
                got = set(re.findall(r"INT-\d{4}-\d{4}", txt))
                ok(want == got, f"{r['document_id']} : interventions {got ^ want} incohérentes avec le référentiel MCP")
    else:
        ok(int(r["nb_pages"]) == 1, f"{r['document_id']} : une photo doit avoir nb_pages = 1")

# 7. exigences de la consigne
n = len(rows)
visu = sum(1 for r in rows if r["elements_visuels"] not in ("", "aucun"))
scan = sum(1 for r in rows if r["format"] == "pdf_scanne")
contra = sum(1 for r in rows if r["usage_test"] == "contradictoire")
inj = sum(1 for r in rows if r["usage_test"] == "injection")
ok(30 <= n <= 50, f"{n} documents (30 à 50 attendus)")
ok(visu >= 10, f"{visu} documents visuels (≥ 10)")
ok(scan >= 2, f"{scan} scannés (≥ 2)")
ok(contra >= 2, f"{contra} contradictoires (≥ 2)")
ok(inj >= 1, f"{inj} document piégé (≥ 1)")
fam = {f: sum(1 for r in rows if r["famille_equipement"] == f) for f in ("pompes", "compresseurs")}

print(f"Documents : {n} | par famille : {fam} | avec éléments visuels : {visu} | scannés : {scan} | "
      f"contradictoires : {contra} | injection : {inj} | ambigus : {sum(r['usage_test']=='ambigu' for r in rows)} | "
      f"en anglais : {sum(r['langue']=='en' for r in rows)} | réservés responsables : {sum(r['groupe_acces']=='responsables' for r in rows)}")
print(f"Pages PDF totales : {sum(int(r['nb_pages']) for r in rows if r['format']!='image')}")
if err:
    print(f"\n{len(err)} ERREUR(S) :"); [print(" -", e) for e in err]; sys.exit(1)
print("\nTous les contrôles sont passés.")
