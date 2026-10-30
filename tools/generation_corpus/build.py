"""Génère le corpus : PDF texte, puis conversion en « scan » des documents marqués pdf_scanne.
Écrit build/meta.json (métadonnées + éléments visuels détectés) utilisé par inventaire.py."""
import json, os, sys, subprocess, random, glob, tempfile
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
from render import build_pdf

OUT = "../../corpus"
META = "build/meta.json"


def scanify(pdf_path, seed=0):
    """Rastérise chaque page, ajoute inclinaison, bruit, flou, grain papier : PDF image sans couche texte."""
    rnd = random.Random(seed)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["pdftoppm", "-r", "130", "-gray", "-png", pdf_path, f"{td}/p"], check=True)
        pages = []
        for f in sorted(glob.glob(f"{td}/p*.png")):
            im = Image.open(f).convert("L")
            im = im.rotate(rnd.uniform(-1.2, 1.2), resample=Image.BICUBIC, expand=False, fillcolor=255)
            a = np.asarray(im).astype(np.float32)
            a = a * 0.92 + 12 + np.random.default_rng(seed).normal(0, 9, a.shape)          # grain
            grad = np.linspace(0, 18, a.shape[1])[None, :]                                    # éclairage inégal
            a = np.clip(a - grad, 0, 255).astype(np.uint8)
            im = Image.fromarray(a).filter(ImageFilter.GaussianBlur(0.6))
            im = ImageEnhance.Contrast(im).enhance(1.15)
            pages.append(im.convert("RGB"))
        pages[0].save(pdf_path, save_all=True, append_images=pages[1:], resolution=130)


def main(modules):
    meta = json.load(open(META)) if os.path.exists(META) else {}
    for mod in modules:
        m = __import__(mod)
        for i, d in enumerate(m.all_docs()):
            path = f"{OUT}/{d['dossier']}/{d['id']}.pdf"
            vis = build_pdf(d, path)
            if d["format"] == "pdf_scanne":
                scanify(path, seed=i + 7)
            rec = {k: v for k, v in d.items() if k not in ("pages",)}
            rec.update(fichier=f"{d['dossier']}/{d['id']}.pdf", nb_pages=len(d["pages"]),
                       visuels=[(t, e, p) for t, e, p, _ in vis])
            meta[d["id"]] = rec
            print(f"OK {d['id']:45s} {len(d['pages']):3d} p  {d['format']}")
    json.dump(meta, open(META, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
