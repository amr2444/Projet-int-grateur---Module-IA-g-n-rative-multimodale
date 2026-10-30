"""Produit corpus/inventaire.csv (UTF-8, séparateur virgule) à partir de build/meta.json."""
import csv, json, re

META = "build/meta.json"
OUT = "../../corpus/inventaire.csv"
COLS = ["document_id", "fichier", "titre", "famille_equipement", "equipement_id", "type_document", "version", "nb_pages", "langue",
        "format", "elements_visuels", "provenance", "licence", "genere_par_ia", "outil_ia", "verifie_par", "corrections",
        "groupe_acces", "usage_test", "remarques"]

# Corrections issues du journal de vérification (journal_verification.md)
CORR = {
    "proc_vidange_cp50_v1": "E01 : couple 35 N·m retiré du schéma (contredisait le texte v1 à 25 N·m)",
    "historique_pompe_a_01": "E02 : tableau élargi (identifiants INT- coupés)",
    "historique_pompe_b_01": "E02 : tableau élargi (identifiants INT- coupés)",
    "historique_comp_a_01": "E02 : tableau élargi (identifiants INT- coupés)",
    "historique_comp_b_02": "E02 : tableau élargi (identifiants INT- coupés)",
    "rapport_audit_air_comprime": "E03 : titre de figure corrigé (3 compresseurs et non local LC1)",
    "photo_panneau_comp_a01": "E04 : reflet repositionné sur le code ; E05 : teinte orange corrigée",
    "photo_panneau_pompe_a01": "E05 : teinte orange du voyant corrigée",
    "photo_voyant_orange_gros_plan": "E05 : teinte orange du voyant corrigée",
    "codes_alarme_pompes": "E06 : identifiants abrégés A-02 écrits en entier",
    "schema_pid_station_sp1": "E06 : identifiants abrégés A-02 écrits en entier",
}


def label(kind, eid, page):
    num = re.sub(r"^[a-z]+_", "", eid).replace("_", ".")
    prefix = {"figure": "fig", "planche": "planche", "folio": "folio", "schema": "schéma", "tableau": "tableau", "table": "tableau"}
    p = eid.split("_")[0]
    return f"{prefix.get(p, 'fig' if kind == 'figure' else 'tableau')} {num} p.{page}"


def main():
    meta = json.load(open(META))
    rows = []
    for did in sorted(meta, key=lambda k: (meta[k]["fichier"])):
        m = meta[did]
        vis = " ; ".join(label(*v) for v in m.get("visuels", [])) or m.get("elements_visuels", "aucun")
        rows.append({
            "document_id": did, "fichier": m["fichier"], "titre": m["titre"], "famille_equipement": m["famille"],
            "equipement_id": m["equipement_id"], "type_document": m["type_document"], "version": m["version"],
            "nb_pages": m["nb_pages"], "langue": m.get("langue", "fr"), "format": m["format"], "elements_visuels": vis,
            "provenance": "synthetique", "licence": "synthetique", "genere_par_ia": "oui",
            "outil_ia": f"Claude Opus 5.5 (prompt {m['prompt']})", "verifie_par": m["verifie_par"],
            "corrections": CORR.get(did, "aucune"), "groupe_acces": m["groupe_acces"], "usage_test": m["usage_test"],
            "remarques": m.get("remarques", ""),
        })
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "lignes ->", OUT)


if __name__ == "__main__":
    main()
