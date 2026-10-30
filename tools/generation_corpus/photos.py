"""Photos synthétiques de terrain (panneaux, voyants, plaques, manomètre) générées par script.
Effets « photo » : perspective, vignettage, reflet, bruit, flou, compression JPEG."""
import math, os, json, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = "../../corpus/images"
FD = "/usr/share/fonts/truetype/dejavu/"
os.makedirs(OUT, exist_ok=True)
F = lambda s, b=False, mono=False: ImageFont.truetype(FD + ("DejaVuSansMono-Bold.ttf" if mono else ("DejaVuSans-Bold.ttf" if b else "DejaVuSans.ttf")), s)
C = {"vert": (40, 170, 70), "orange": (255, 140, 0), "rouge": (220, 40, 40), "bleu": (30, 110, 220)}


def lamp(d, im, x, y, r, col, on):
    if on:
        glow = Image.new("RGBA", im.size, (0, 0, 0, 0))
        g = ImageDraw.Draw(glow)
        for k in range(14, 0, -1):
            a = int(10 + 8 * (14 - k))
            g.ellipse([x - r - 4 * k, y - r - 4 * k, x + r + 4 * k, y + r + 4 * k], fill=col + (max(0, 60 - 4 * k),))
        im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
        d.ellipse([x - r, y - r, x + r, y + r], fill=tuple(min(255, c + 25) for c in col), outline=(40, 40, 40), width=6)
        d.ellipse([x - r // 3, y - r // 2, x + r // 6, y - r // 6], fill=(255, 250, 230))
    else:
        d.ellipse([x - r, y - r, x + r, y + r], fill=tuple(int(c * 0.35) + 60 for c in col), outline=(40, 40, 40), width=6)


def photo_fx(im, seed, persp=0.06, blur=1.0, glare=None, noise=7, dark=0.35, rot=2.0):
    rnd = random.Random(seed)
    im = im.convert("RGB")
    w, h = im.size
    # perspective (quadrilatère)
    dx, dy = persp * w, persp * h
    quad = [rnd.uniform(0, dx), rnd.uniform(0, dy), rnd.uniform(0, dx), h - rnd.uniform(0, dy),
            w - rnd.uniform(0, dx), h - rnd.uniform(0, dy), w - rnd.uniform(0, dx), rnd.uniform(0, dy)]
    im = im.transform((w, h), Image.QUAD, quad, resample=Image.BICUBIC)
    im = im.rotate(rnd.uniform(-rot, rot), resample=Image.BICUBIC, fillcolor=(70, 70, 75))
    a = np.asarray(im).astype(np.float32)
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w * rnd.uniform(0.35, 0.65), h * rnd.uniform(0.35, 0.65)
    vig = 1 - dark * (((xx - cx) / w) ** 2 + ((yy - cy) / h) ** 2) * 2.2
    a *= vig[..., None]
    a *= np.array([1.03, 1.0, 0.94])  # dominante chaude (éclairage atelier)
    if glare:
        gx, gy, gr = glare
        gl = np.exp(-(((xx - gx * w) ** 2 + (yy - gy * h) ** 2) / (2 * (gr * w) ** 2)))
        a += 235 * gl[..., None]
    a += np.random.default_rng(seed).normal(0, noise, a.shape)
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))
    return im


def tag(d, x, y, text, w=330):
    d.rounded_rectangle([x, y, x + w, y + 70], 8, fill=(250, 250, 240), outline=(30, 30, 30), width=3)
    d.text((x + w / 2, y + 35), text, font=F(34, True), fill=(20, 20, 20), anchor="mm")


def panel_pompe():
    im = Image.new("RGBA", (1600, 1200), (95, 98, 105, 255)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([120, 90, 1480, 1110], 30, fill=(205, 208, 212), outline=(60, 60, 60), width=8)
    d.text((800, 160), "ARMOIRE AP-SP1", font=F(46, True), fill=(30, 30, 30), anchor="mm")
    tag(d, 635, 205, "POMPE-A-01")
    d.rectangle([420, 310, 1180, 450], fill=(25, 50, 25), outline=(10, 10, 10), width=6)
    d.text((800, 380), "P-21  T PAL 84°C", font=F(58, mono=True), fill=(150, 255, 150), anchor="mm")
    for i, (vid, col, lab, on) in enumerate([("H1", "vert", "MARCHE", True), ("H2", "orange", "ALERTE", True),
                                             ("H3", "rouge", "DÉFAUT", False), ("H4", "bleu", "MANQUE D'EAU", False)]):
        x = 320 + i * 320
        lamp(d, im, x, 640, 80, C[col], on); d = ImageDraw.Draw(im)
        d.text((x, 770), vid, font=F(40, True), fill=(20, 20, 20), anchor="mm"); d.text((x, 820), lab, font=F(28), fill=(20, 20, 20), anchor="mm")
    for i, (b, col) in enumerate([("S1", (40, 150, 60)), ("S2", (200, 40, 40)), ("S3", (40, 40, 40))]):
        x = 480 + i * 320
        d.rectangle([x - 60, 900, x + 60, 1010], fill=col, outline=(0, 0, 0), width=4); d.text((x, 955), b, font=F(36, True), fill="white", anchor="mm")
    return photo_fx(im, 11, persp=0.05, blur=1.1, glare=(0.78, 0.22, 0.06))


def panel_comp():
    im = Image.new("RGBA", (1600, 1200), (120, 118, 112, 255)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([140, 110, 1460, 1090], 40, fill=(52, 58, 66), outline=(20, 20, 20), width=8)
    d.text((800, 190), "MD-Air", font=F(52, True), fill=(230, 230, 230), anchor="mm")
    tag(d, 635, 230, "COMP-A-0", w=330)
    d.rectangle([905, 222, 1010, 310], fill=(70, 60, 50))  # étiquette partiellement masquée (ruban adhésif)
    d.rectangle([420, 340, 1180, 480], fill=(25, 45, 30), outline=(10, 10, 10), width=6)
    d.text((800, 410), "A-12  T REF 103°C", font=F(56, mono=True), fill=(150, 255, 150), anchor="mm")
    for i, (vid, col, on) in enumerate([("L1", "vert", True), ("L2", "orange", True), ("L3", "rouge", False)]):
        x = 400 + i * 400
        lamp(d, im, x, 670, 85, C[col], on); d = ImageDraw.Draw(im)
        d.text((x, 805), vid, font=F(40, True), fill=(235, 235, 235), anchor="mm")
    for i, (b, col) in enumerate([("I", (40, 150, 60)), ("O", (200, 40, 40)), ("R", (90, 90, 90))]):
        x = 480 + i * 320
        d.ellipse([x - 60, 900, x + 60, 1020], fill=col, outline=(0, 0, 0), width=4); d.text((x, 960), b, font=F(40, True), fill="white", anchor="mm")
    # reflet fort sur la partie gauche de l'afficheur : le code d'alarme est illisible
    gl = Image.new("RGBA", im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(gl)
    g.ellipse([470, 300, 830, 520], fill=(255, 255, 250, 255))
    im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(28)))
    return photo_fx(im, 23, persp=0.08, blur=1.4, glare=None, dark=0.45)


def voyant_gros_plan():
    im = Image.new("RGBA", (1200, 900), (170, 172, 176, 255)); d = ImageDraw.Draw(im)
    lamp(d, im, 600, 430, 230, C["orange"], True); d = ImageDraw.Draw(im)
    d.text((600, 780), "ALERTE", font=F(60, True), fill=(30, 30, 30), anchor="mm")
    return photo_fx(im, 31, persp=0.04, blur=2.0, dark=0.5)


def plaque(blur_strong=False):
    im = Image.new("RGBA", (1500, 1000), (110, 115, 125, 255)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([150, 120, 1350, 880], 20, fill=(198, 200, 196), outline=(80, 80, 80), width=6)
    for (x, y) in [(190, 160), (1310, 160), (190, 840), (1310, 840)]:
        d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=(150, 150, 150), outline=(60, 60, 60), width=3)
    d.text((750, 210), "MD-Pompes", font=F(64, True), fill=(20, 40, 90), anchor="mm")
    lines = [("Type", "CP-50"), ("N° série", "CP50-21-0457"), ("Q nom.", "50 m³/h"), ("H nom.", "32 m"),
             ("n", "2900 tr/min"), ("P max", "10 bar"), ("T max", "90 °C"), ("Année", "2021")]
    for i, (k, v) in enumerate(lines):
        y = 320 + i * 66
        d.text((260, y), k, font=F(40), fill=(30, 30, 30)); d.text((680, y), v, font=F(40, True), fill=(10, 10, 10))
    if blur_strong:
        im = im.filter(ImageFilter.GaussianBlur(9))
        return photo_fx(im, 47, persp=0.1, blur=3.5, glare=(0.55, 0.5, 0.13), dark=0.55, rot=6)
    return photo_fx(im, 41, persp=0.05, blur=1.0, glare=(0.85, 0.2, 0.05))


def manometre():
    im = Image.new("RGBA", (1200, 1200), (140, 145, 150, 255)); d = ImageDraw.Draw(im)
    cx, cy, R = 600, 560, 430
    d.ellipse([cx - R - 30, cy - R - 30, cx + R + 30, cy + R + 30], fill=(60, 60, 60))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(245, 245, 240))
    a0, a1 = 225, -45  # 0 à 16 bar
    ang = lambda v: math.radians(a0 - (a0 - a1) * v / 16)
    for v10 in range(10, 16 * 10 + 1):
        pass
    d.arc([cx - R + 40, cy - R + 40, cx + R - 40, cy + R - 40], start=-a0 + (a0 - a1) * 10 / 16, end=-a1, fill=(220, 30, 30), width=30)
    for v in range(0, 17):
        t = ang(v); r1 = R - 20; r2 = R - (75 if v % 2 == 0 else 50)
        d.line([cx + r1 * math.cos(t), cy - r1 * math.sin(t), cx + r2 * math.cos(t), cy - r2 * math.sin(t)], fill=(10, 10, 10), width=8 if v % 2 == 0 else 4)
        if v % 2 == 0:
            r3 = R - 125
            d.text((cx + r3 * math.cos(t), cy - r3 * math.sin(t)), str(v), font=F(48, True), fill=(10, 10, 10), anchor="mm")
    d.text((cx, cy + 170), "bar", font=F(50), fill=(10, 10, 10), anchor="mm")
    d.text((cx, cy + 240), "MD-Air  PS-11", font=F(34), fill=(60, 60, 60), anchor="mm")
    t = ang(8.2)
    d.line([cx, cy, cx + (R - 90) * math.cos(t), cy - (R - 90) * math.sin(t)], fill=(20, 20, 20), width=14)
    d.ellipse([cx - 35, cy - 35, cx + 35, cy + 35], fill=(30, 30, 30))
    d.rectangle([520, 1060, 680, 1200], fill=(180, 150, 60))
    return photo_fx(im, 53, persp=0.05, blur=1.2, glare=(0.35, 0.3, 0.07))


PHOTOS = [
    dict(id="photo_panneau_pompe_a01", f=panel_pompe, titre="Photo – armoire AP-SP1, panneau POMPE-A-01 en préalarme (H2 orange fixe, P-21)",
         famille="pompes", equipement_id="POMPE-A-01", version="2026-09 (prise de vue)", elements_visuels="voyants H1 vert et H2 orange allumés ; afficheur « P-21 T PAL 84°C » ; étiquette POMPE-A-01",
         groupe_acces="techniciens_pompes ; responsables", usage_test="normal", verifie_par="Amr", prompt="P25",
         remarques="Cas nominal CU1 : équipement et code lisibles ; réponse attendue manuel_pompe_cp50 p.8-9"),
    dict(id="photo_plaque_cp50", f=lambda: plaque(False), titre="Photo – plaque signalétique pompe CP-50 (POMPE-A-01)", famille="pompes",
         equipement_id="POMPE-A-01", version="2026-09 (prise de vue)", elements_visuels="plaque lisible : type CP-50, série CP50-21-0457",
         groupe_acces="techniciens_pompes ; responsables", usage_test="normal", verifie_par="Amr", prompt="P25",
         remarques="Permet d'identifier l'équipement par le numéro de série (manuel p.3)"),
    dict(id="photo_plaque_floue_pompe", f=lambda: plaque(True), titre="Photo – plaque signalétique floue et inclinée (illisible)", famille="pompes",
         equipement_id="POMPE-A-01", version="2026-09 (prise de vue)", elements_visuels="plaque floue, reflet, texte illisible",
         groupe_acces="techniciens_pompes ; responsables", usage_test="ambigu", verifie_par="Amr", prompt="P25",
         remarques="Test CU5 : le système doit demander une nouvelle photo au lieu de deviner"),
    dict(id="photo_panneau_comp_a01", f=panel_comp, titre="Photo – contrôleur compresseur VS-37, voyant L2 orange, afficheur avec reflet",
         famille="compresseurs", equipement_id="COMP-A-01", version="2026-08 (prise de vue)",
         elements_visuels="voyants L1 vert et L2 orange allumés ; code d'alarme masqué par un reflet (seul « REF 103°C » lisible) ; étiquette « COMP-A-0? » partiellement masquée",
         groupe_acces="techniciens_compresseurs ; responsables", usage_test="ambigu", verifie_par="Soulaimane", prompt="P25",
         remarques="Voyant orange proche de celui de la pompe A ; identifiant incomplet (A-01 ou A-02) : clarification attendue"),
    dict(id="photo_voyant_orange_gros_plan", f=voyant_gros_plan, titre="Photo – gros plan d'un voyant orange « ALERTE » sans contexte",
         famille="compresseurs", equipement_id="COMP-A-01 ; POMPE-A-01", version="2026-09 (prise de vue)", elements_visuels="un voyant orange allumé, libellé ALERTE",
         groupe_acces="techniciens_compresseurs ; techniciens_pompes ; responsables", usage_test="ambigu", verifie_par="Soulaimane", prompt="P25",
         remarques="Ambigu : voyant compatible pompe (H2) ou compresseur (L2) ; classé famille compresseurs par convention"),
    dict(id="photo_manometre_ps11", f=manometre, titre="Photo – manomètre du réservoir du compresseur PS-11 (≈ 8,2 bar)", famille="compresseurs",
         equipement_id="COMP-B-02", version="2026-09 (prise de vue)", elements_visuels="cadran 0-16 bar, aiguille ≈ 8,2 bar, zone rouge ≥ 10 bar",
         groupe_acces="techniciens_compresseurs ; responsables", usage_test="normal", verifie_par="Soulaimane", prompt="P25",
         remarques="Lecture d'une valeur analogique par le VLM ; cohérent avec la plage 8-10 bar du pressostat"),
]


def main():
    meta_path = "build/meta.json"
    meta = json.load(open(meta_path))
    for p in PHOTOS:
        im = p["f"]()
        im.save(f"{OUT}/{p['id']}.jpg", quality=82)
        rec = {k: v for k, v in p.items() if k != "f"}
        rec.update(fichier=f"images/{p['id']}.jpg", nb_pages=1, format="image", langue="fr", type_document="photo",
                   titre=p["titre"], visuels=[])
        meta[p["id"]] = rec
        print("OK", p["id"])
    json.dump(meta, open(meta_path, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
