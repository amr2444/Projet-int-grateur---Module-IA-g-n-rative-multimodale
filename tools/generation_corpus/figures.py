"""Figures techniques synthétiques (matplotlib) – schémas simplifiés, non contractuels."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon, FancyArrowPatch

OUT = "build/fig"
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
COL = {"vert": "#2e9e44", "orange": "#f08c00", "rouge": "#d62828", "bleu": "#1d6fd6", "off": "#bfbfbf"}


def _save(fig, name):
    p = f"{OUT}/{name}.png"
    fig.savefig(p, dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return p


def _ax(w=8, h=5):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def _box(ax, x, y, w, h, txt, fc="white", ec="black", fs=8, lw=1.2, r=0.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
    if txt:
        ax.text(x + w / 2, y + h / 2, txt, ha="center", va="center", fontsize=fs)


def _arrow(ax, x1, y1, x2, y2, col="black", lw=1.4, ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12, color=col, lw=lw, linestyle=ls))


def panel(kind="pompes", lit=None):
    """Face avant d'un panneau. lit = dict(id -> (couleur, mode)) pour les voyants allumés (schéma)."""
    fig, ax = _ax(7.5, 5)
    ax.set_xlim(0, 15); ax.set_ylim(0, 10)
    _box(ax, 0.3, 0.3, 14.4, 9.4, "", fc="#d9dde2", lw=2, r=0.3)
    if kind == "pompes":
        title, vy = "ARMOIRE POMPES – FACE AVANT", [("H1", "vert", "MARCHE"), ("H2", "orange", "ALERTE"),
                                                   ("H3", "rouge", "DÉFAUT"), ("H4", "bleu", "MANQUE D'EAU")]
        disp = "P-21  T PAL 82°C"
        btn = [("S1", "MARCHE", "#2e9e44"), ("S2", "ARRÊT", "#d62828"), ("S3", "ACQUIT.", "#333333")]
    elif kind == "vs37":
        title, vy = "CONTRÔLEUR MD-Air VS-37", [("L1", "vert", "EN CHARGE"), ("L2", "orange", "ALERTE / ENTRETIEN"),
                                               ("L3", "rouge", "ARRÊT DÉFAUT")]
        disp = "A-12  T REF 101°C"
        btn = [("I", "MARCHE", "#2e9e44"), ("O", "ARRÊT", "#d62828"), ("R", "RESET", "#333333")]
    else:
        title, vy = "COFFRET MD-Air PS-11", [("V1", "vert", "SOUS TENSION"), ("V2", "orange", "TEMP. CULASSE"),
                                            ("V3", "rouge", "ARRÊT SÉCU.")]
        disp = "P 8.2 bar   312 h"
        btn = [("I", "MARCHE", "#2e9e44"), ("O", "ARRÊT", "#d62828")]
    ax.text(7.5, 9.1, title, ha="center", fontsize=10, weight="bold")
    _box(ax, 3.5, 6.6, 8, 1.6, disp, fc="#1f3d1f", ec="black", fs=11)
    ax.texts[-1].set_color("#9cff9c"); ax.texts[-1].set_family("DejaVu Sans Mono")
    ax.text(7.5, 6.25, "Afficheur (code + mesure)", ha="center", fontsize=7, style="italic")
    n = len(vy)
    for i, (vid, c, lab) in enumerate(vy):
        x = 15 * (i + 1) / (n + 1)
        on = lit and vid in lit
        ax.add_patch(Circle((x, 4.6), 0.75, fc=COL[c] if on else "#e8e8e8", ec=COL[c], lw=3))
        ax.text(x, 3.45, vid, ha="center", fontsize=9, weight="bold")
        ax.text(x, 2.95, lab, ha="center", fontsize=7)
    for i, (bid, lab, c) in enumerate(btn):
        x = 15 * (i + 1) / (len(btn) + 1)
        ax.add_patch(Rectangle((x - 0.6, 1.0), 1.2, 1.0, fc=c, ec="black"))
        ax.text(x, 1.5, bid, ha="center", va="center", color="white", fontsize=8, weight="bold")
        ax.text(x, 0.6, lab, ha="center", fontsize=6.5)
    return fig


def courbe_cp50():
    fig, ax1 = plt.subplots(figsize=(7, 4))
    q = np.linspace(0, 70, 100)
    h = 40 - 0.0032 * q ** 2
    eta = 78 * (1 - ((q - 50) / 50) ** 2)
    npsh = 1.5 + 0.00068 * q ** 2
    ax1.plot(q, h, color="#123a6b", lw=2, label="HMT (m)")
    ax1.plot(q, npsh * 5, color="#d62828", lw=1.5, ls="--", label="NPSH requis (m) ×5")
    ax1.axvline(50, color="gray", ls=":"); ax1.text(50.5, 41, "Point nominal\n50 m³/h – 32 m", fontsize=7)
    ax1.set_xlabel("Débit Q (m³/h)"); ax1.set_ylabel("Hauteur (m)"); ax1.set_ylim(0, 45); ax1.grid(alpha=.3)
    ax2 = ax1.twinx(); ax2.plot(q, np.clip(eta, 0, None), color="#2e9e44", lw=1.5, label="Rendement (%)")
    ax2.set_ylabel("Rendement (%)"); ax2.set_ylim(0, 100)
    l1, n1 = ax1.get_legend_handles_labels(); l2, n2 = ax2.get_legend_handles_labels()
    ax1.legend(l1 + l2, n1 + n2, loc="lower left", fontsize=7)
    ax1.set_title("Courbes caractéristiques CP-50 à 2900 tr/min (eau 20 °C)", fontsize=9)
    return fig


def vue_eclatee_cp50():
    fig, ax = _ax(9, 4.6)
    ax.set_xlim(0, 22); ax.set_ylim(-1, 10)
    parts = [  # (x, w, h, label, n°)
        (0.5, 2.2, 6, "Corps\nvolute", 1), (3.4, 1.0, 4.6, "Roue", 2), (5.0, 0.6, 3.2, "Écrou\nde roue", 3),
        (6.3, 1.2, 3.6, "Garniture\nmécanique", 4), (8.2, 0.8, 4.8, "Couvercle\ngarniture", 5),
        (9.7, 3.0, 4.0, "Lanterne /\npalier", 6), (13.3, 0.8, 2.6, "Roulement\n6307 C3", 7),
        (14.6, 0.8, 2.4, "Roulement\n6306 C3", 8), (16.0, 1.0, 3.0, "Accouple-\nment", 9), (17.8, 3.6, 5.2, "Moteur\n7,5 kW", 10)]
    ax.plot([0.3, 21.7], [5, 5], color="gray", ls="-.", lw=0.8)
    for i, (x, w, h, lab, n) in enumerate(parts):
        _box(ax, x, 5 - h / 2, w, h, "", fc="#e6ecf3")
        yl = 5 - h / 2 - 0.3 if i % 2 == 0 else 1.0
        ax.text(x + w / 2, yl, lab, ha="center", va="top", fontsize=6.5)
        ax.add_patch(Circle((x + w / 2, 5 + h / 2 + 0.7), 0.42, fc="white", ec="#d62828", lw=1.3))
        ax.text(x + w / 2, 5 + h / 2 + 0.7, str(n), ha="center", va="center", fontsize=7, color="#d62828", weight="bold")
    ax.text(11, 9.6, "Vue éclatée simplifiée – pompe CP-50", ha="center", weight="bold")
    return fig


def coupe_garniture():
    fig, ax = _ax(7, 3.8)
    ax.set_xlim(0, 14); ax.set_ylim(0, 7)
    ax.add_patch(Rectangle((0, 3.1), 14, 0.8, fc="#bfbfbf", ec="black")); ax.text(12.5, 3.5, "Arbre Ø 35", fontsize=7, va="center")
    for y in (3.9, 1.6):
        ax.add_patch(Rectangle((3, y), 1.4, 1.5, fc="#ffd27f", ec="black"))     # grain tournant
        ax.add_patch(Rectangle((4.4, y), 1.0, 1.5, fc="#9ec5fe", ec="black"))   # grain fixe
        ax.add_patch(Rectangle((1.2, y), 1.6, 1.5, fc="white", ec="black", hatch="////"))  # ressort
        ax.add_patch(Rectangle((5.6, y - 0.3), 2.4, 2.1, fc="#e6ecf3", ec="black"))  # couvercle
    ax.annotate("A – Grain tournant (carbone)", (3.7, 5.4), (0.2, 6.6), fontsize=7, arrowprops=dict(arrowstyle="->"))
    ax.annotate("B – Grain fixe (SiC)", (4.9, 5.4), (5.5, 6.6), fontsize=7, arrowprops=dict(arrowstyle="->"))
    ax.annotate("C – Ressort", (2.0, 1.6), (0.2, 0.4), fontsize=7, arrowprops=dict(arrowstyle="->"))
    ax.annotate("D – Couvercle de garniture\n(4 vis M10)", (6.8, 1.3), (8.6, 0.3), fontsize=7, arrowprops=dict(arrowstyle="->"))
    ax.text(0.2, 5.6, "← Côté fluide (corps de pompe)", fontsize=7, color="#1d6fd6")
    return fig


def alignement():
    fig, ax = _ax(8, 3.6)
    ax.set_xlim(0, 16); ax.set_ylim(0, 7)
    _box(ax, 0.5, 2, 5, 3, "Pompe", fc="#e6ecf3"); _box(ax, 10.5, 1.8, 5, 3.4, "Moteur", fc="#e6ecf3")
    ax.add_patch(Rectangle((5.5, 3.2), 2.2, 0.6, fc="#bfbfbf", ec="black")); ax.add_patch(Rectangle((8.3, 3.2), 2.2, 0.6, fc="#bfbfbf", ec="black"))
    ax.add_patch(Rectangle((7.5, 2.6), 0.5, 1.8, fc="#ffd27f", ec="black")); ax.add_patch(Rectangle((8.0, 2.6), 0.5, 1.8, fc="#ffd27f", ec="black"))
    ax.add_patch(Circle((8.0, 5.6), 0.55, fc="white", ec="black")); ax.text(8.0, 5.6, "⌀", ha="center", va="center")
    ax.plot([8.0, 8.0], [5.05, 4.4], color="black")
    ax.text(8.0, 6.5, "Comparateur radial (R)", ha="center", fontsize=7)
    ax.annotate("Comparateur axial (A)\nsur la face du demi-accouplement", (7.9, 2.6), (5.0, 0.4), fontsize=7, arrowprops=dict(arrowstyle="->"))
    ax.text(13, 0.8, "Cales d'épaisseur sous pattes moteur", fontsize=7, ha="center")
    for x in (11.2, 14.8):
        ax.add_patch(Rectangle((x - 0.4, 1.5), 0.8, 0.3, fc="#555555"))
    ax.text(8, 0.0, "Tolérances : radial ≤ 0,05 mm – angulaire ≤ 0,05 mm / 100 mm", ha="center", fontsize=7.5, weight="bold")
    return fig


def pid_station():
    fig, ax = _ax(9, 5)
    ax.set_xlim(0, 20); ax.set_ylim(0, 11)
    _box(ax, 0.5, 2, 3, 6, "Bâche\nT-101", fc="#dbe9ff")
    ax.text(2, 8.4, "LSL-101", fontsize=7, ha="center"); ax.plot([0.5, 3.5], [3.0, 3.0], color="#1d6fd6", ls="--")
    for i, (y, tag) in enumerate([(7.5, "POMPE-A-01"), (3.5, "POMPE-A-02")]):
        ax.plot([3.5, 6], [y - 1, y - 1], color="black", lw=1.5)
        ax.add_patch(Polygon([[6, y - 1.6], [6, y - 0.4], [6.8, y - 1]], fc="white", ec="black"))  # vanne
        ax.text(6.3, y - 2.1, f"V-1{i}1", fontsize=6.5)
        ax.text(7.6, y + 0.3, "PI", fontsize=6.5); ax.add_patch(Circle((7.8, y - 0.2), 0.3, fc="white", ec="black"))
        ax.plot([6.8, 9], [y - 1, y - 1], color="black", lw=1.5)
        ax.add_patch(Circle((10, y - 1), 1.0, fc="#e6ecf3", ec="black", lw=1.5)); ax.text(10, y - 1, "P", ha="center", va="center", weight="bold")
        ax.text(10, y + 0.3, tag, fontsize=7, ha="center", weight="bold")
        ax.plot([11, 13], [y - 1, y - 1], color="black", lw=1.5)
        ax.add_patch(Polygon([[13, y - 1.6], [13, y - 0.4], [13.8, y - 1]], fc="white", ec="black")); ax.text(13.1, y - 2.1, "CL (clapet)", fontsize=6.5)
        ax.plot([13.8, 16], [y - 1, y - 1], color="black", lw=1.5); ax.plot([16, 16], [y - 1, 5.5], color="black", lw=1.5)
    ax.plot([16, 19.5], [5.5, 5.5], color="black", lw=2); _arrow(ax, 18.5, 5.5, 19.6, 5.5)
    ax.text(17.8, 6, "Vers réseau\nrefroidissement", fontsize=7, ha="center")
    ax.add_patch(Circle((17.0, 4.5), 0.35, fc="white", ec="black")); ax.text(17.0, 4.5, "PT", fontsize=6, ha="center", va="center"); ax.text(17.5, 4.0, "PT-103", fontsize=6.5)
    ax.text(10, 10.3, "Schéma P&ID simplifié – Station de pompage SP1", ha="center", weight="bold")
    return fig


def elec_armoire_pompes():
    fig, ax = _ax(9, 5.2)
    ax.set_xlim(0, 20); ax.set_ylim(0, 11)
    for y, l in [(10, "L1"), (9.5, "L2"), (9, "L3")]:
        ax.plot([0.5, 19.5], [y, y], color="black", lw=1); ax.text(0, y, l, fontsize=7, va="center")
    for x, name in [(4, "POMPE-A-01"), (11, "POMPE-A-02")]:
        for dx in (-0.4, 0, 0.4):
            ax.plot([x + dx, x + dx], [9 if dx == 0.4 else (9.5 if dx == 0 else 10), 4], color="black", lw=0.8)
        _box(ax, x - 1, 7.6, 2, 0.8, "Q1 disj.", fs=6.5); _box(ax, x - 1, 6.2, 2, 0.8, "KM1 contact.", fs=6.5)
        _box(ax, x - 1, 4.8, 2, 0.8, "F1 thermique", fs=6.5)
        ax.add_patch(Circle((x, 3.2), 1.0, fc="#e6ecf3", ec="black")); ax.text(x, 3.2, "M\n3~", ha="center", va="center", fontsize=8)
        ax.text(x, 1.7, name + "\n7,5 kW", ha="center", fontsize=7)
    _box(ax, 15, 2.2, 4.5, 7.5, "", fc="#fafafa")
    ax.text(17.25, 9.2, "Circuit commande 24 V", ha="center", fontsize=7, weight="bold")
    for i, (vid, c, lab) in enumerate([("H1", "vert", "Marche"), ("H2", "orange", "Alerte"), ("H3", "rouge", "Défaut"), ("H4", "bleu", "Manque eau")]):
        y = 8.2 - i * 1.4
        ax.add_patch(Circle((16, y), 0.35, fc=COL[c], ec="black")); ax.text(16.6, y, f"{vid} – {lab}", fontsize=7, va="center")
    ax.text(17.25, 2.6, "API : entrées PTC, LS-102,\nLSL-101, PT-103, VT-104", ha="center", fontsize=6.5)
    ax.text(10, 0.5, "Schéma électrique simplifié – armoire AP-SP1 (non contractuel)", ha="center", weight="bold", fontsize=8)
    return fig


def coupe_cm80():
    fig, ax = _ax(9, 3.8)
    ax.set_xlim(0, 22); ax.set_ylim(0, 8)
    ax.add_patch(Rectangle((0.5, 3.6), 21, 0.8, fc="#bfbfbf", ec="black"))
    _box(ax, 0.8, 1.5, 2.5, 5, "Aspiration", fs=7, fc="#dbe9ff")
    for i in range(5):
        x = 4 + i * 2.6
        _box(ax, x, 1.3, 2.2, 5.4, "", fc="#e6ecf3")
        ax.add_patch(Rectangle((x + 0.6, 2.2), 1.0, 3.6, fc="#ffd27f", ec="black"))
        ax.text(x + 1.1, 7.0, f"Étage {i+1}", ha="center", fontsize=6.5)
    _box(ax, 17.3, 1.5, 2.2, 5, "Refoule-\nment", fs=7, fc="#dbe9ff")
    ax.text(20.7, 2.4, "Butée\n7309 BEP", fontsize=6.5, ha="center")
    ax.text(11, 0.3, "Coupe simplifiée – pompe multicellulaire CM-80 (5 roues en série)", ha="center", weight="bold", fontsize=8)
    return fig


def circuit_vs37():
    fig, ax = _ax(9, 5.4)
    ax.set_xlim(0, 20); ax.set_ylim(0, 12)
    _box(ax, 0.3, 8.5, 2.6, 1.6, "Filtre à air\n(Δp A-31)", fs=7, fc="#f1f1f1")
    _box(ax, 4.0, 8.0, 3.2, 2.6, "Élément de\ncompression\nà vis", fs=7, fc="#e6ecf3")
    _box(ax, 8.6, 6.0, 3.6, 5.0, "Réservoir\nséparateur\nhuile", fs=7, fc="#fff1d6")
    _box(ax, 13.5, 9.0, 2.6, 1.6, "Séparateur\n(Δp A-32)", fs=7, fc="#f1f1f1")
    _box(ax, 13.5, 5.2, 2.8, 2.4, "Radiateur\nair/huile", fs=7, fc="#e2f3e5")
    _box(ax, 17.2, 9.0, 2.5, 1.6, "Clapet PM\n→ réseau", fs=7)
    _box(ax, 8.6, 1.5, 2.6, 1.6, "Filtre huile", fs=7, fc="#f1f1f1")
    _box(ax, 4.0, 1.5, 3.0, 1.6, "Thermostat\n(vanne 3 voies)", fs=7, fc="#f1f1f1")
    _box(ax, 17.2, 5.6, 2.5, 1.6, "Purgeur\n(A-40)", fs=7)
    _arrow(ax, 2.9, 9.3, 4.0, 9.3, "#1d6fd6"); _arrow(ax, 7.2, 9.3, 8.6, 9.3, "#7a4b00")
    _arrow(ax, 12.2, 9.8, 13.5, 9.8, "#1d6fd6"); _arrow(ax, 16.1, 9.8, 17.2, 9.8, "#1d6fd6")
    _arrow(ax, 10.4, 6.0, 10.0, 3.1, "#7a4b00"); _arrow(ax, 8.6, 2.3, 7.0, 2.3, "#7a4b00")
    _arrow(ax, 7.0, 2.9, 13.5, 6.0, "#7a4b00", ls="--"); _arrow(ax, 13.5, 6.6, 7.2, 8.4, "#7a4b00")
    _arrow(ax, 5.5, 3.1, 5.5, 8.0, "#7a4b00", ls=":")
    _arrow(ax, 16.3, 6.4, 17.2, 6.4, "#1d6fd6")
    ax.text(2.6, 11.5, "— air comprimé", color="#1d6fd6", fontsize=7.5); ax.text(7.5, 11.5, "— huile", color="#7a4b00", fontsize=7.5)
    ax.text(10.5, 4.6, "TT-201 (T refoulement)", fontsize=6.5); ax.text(9.9, 11.2, "PT-202", fontsize=6.5)
    ax.text(10, 0.3, "Circuit air / huile simplifié – compresseur VS-37", ha="center", weight="bold", fontsize=8)
    return fig


def elec_vs37():
    fig, ax = _ax(9, 4.6)
    ax.set_xlim(0, 20); ax.set_ylim(0, 10)
    for y, l in [(9.3, "L1"), (8.8, "L2"), (8.3, "L3")]:
        ax.plot([0.5, 13], [y, y], color="black"); ax.text(0, y, l, fontsize=7, va="center")
    _box(ax, 1.5, 6.4, 2.4, 1.0, "Q1 sectionneur", fs=6.5); _box(ax, 1.5, 4.9, 2.4, 1.0, "Relais ordre\nphases (A-22)", fs=6)
    _box(ax, 5.0, 6.4, 1.6, 1.0, "KM1 ligne", fs=6.5); _box(ax, 7.0, 6.4, 1.6, 1.0, "KM2 étoile", fs=6.5); _box(ax, 9.0, 6.4, 1.8, 1.0, "KM3 triangle", fs=6.5)
    ax.add_patch(Circle((8, 3.6), 1.2, fc="#e6ecf3", ec="black")); ax.text(8, 3.6, "M1\n37 kW", ha="center", va="center", fontsize=7)
    ax.add_patch(Circle((11.5, 3.6), 0.8, fc="#e6ecf3", ec="black")); ax.text(11.5, 3.6, "M2\nventil.", ha="center", va="center", fontsize=6)
    for x in (5.8, 7.8, 9.9):
        ax.plot([x, x], [8.3, 7.4], color="black", lw=0.8); ax.plot([x, 8], [6.4, 4.8], color="black", lw=0.8)
    _box(ax, 14, 1.5, 5.5, 7.5, "", fc="#fafafa")
    ax.text(16.75, 8.4, "Contrôleur MD-Air", ha="center", fontsize=7.5, weight="bold")
    for i, t in enumerate(["TT-201 temp. refoulement", "PT-202 pression", "PDS-203 Δp filtre air", "PDS-204 Δp séparateur", "Purgeur électronique", "Sorties L1 / L2 / L3"]):
        ax.text(14.3, 7.6 - i * 0.95, "▪ " + t, fontsize=6.5)
    ax.text(10, 0.4, "Schéma électrique simplifié – démarrage étoile-triangle VS-37", ha="center", weight="bold", fontsize=8)
    return fig


def schema_ps11():
    fig, ax = _ax(8, 4.4)
    ax.set_xlim(0, 18); ax.set_ylim(0, 10)
    ax.add_patch(FancyBboxPatch((1, 1), 15, 3.4, boxstyle="round,pad=0,rounding_size=1.6", fc="#e6ecf3", ec="black", lw=1.5))
    ax.text(8.5, 2.7, "Réservoir 500 L", ha="center", fontsize=8)
    _box(ax, 3, 5.2, 4, 2.4, "Groupe de\ncompression\n2 cyl. en V", fs=7, fc="#fff1d6")
    _box(ax, 9, 5.2, 3, 2.0, "Moteur\n11 kW", fs=7)
    ax.plot([7, 9], [6.6, 6.6], color="black", lw=3); ax.text(8, 7.0, "Courroies SPA", fontsize=6.5, ha="center")
    ax.add_patch(Circle((14, 6.2), 0.8, fc="white", ec="black")); ax.text(14, 6.2, "bar", fontsize=6, ha="center", va="center")
    ax.text(14, 7.3, "Manomètre", fontsize=6.5, ha="center"); ax.plot([14, 14], [5.4, 4.4], color="black")
    _box(ax, 15.5, 5.0, 2.2, 1.2, "Soupape\n11 bar", fs=6.5)
    _box(ax, 11, 0.0, 2.6, 0.8, "Purge manuelle", fs=6.5)
    ax.text(9, 9.3, "Schéma d'ensemble – compresseur à piston PS-11", ha="center", weight="bold")
    return fig


def audit_conso():
    fig, ax = plt.subplots(figsize=(7, 3.2))
    mois = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun", "Jul", "Aoû", "Sep"]
    kwh = [15200, 14800, 15600, 15100, 15900, 17400, 18100, 16900, 15300]
    fuite = [31, 30, 32, 29, 30, 33, 34, 32, 28]
    ax.bar(mois, kwh, color="#123a6b"); ax.set_ylabel("kWh / mois")
    ax2 = ax.twinx(); ax2.plot(mois, fuite, color="#d62828", marker="o"); ax2.set_ylabel("Taux de fuite estimé (%)"); ax2.set_ylim(0, 40)
    ax.set_title("Consommation électrique des 3 compresseurs (LC1 + atelier) – 2026", fontsize=9)
    return fig


def build_all():
    figs = {
        "panel_pompes": lambda: panel("pompes", lit={"H1": 1, "H2": 1}),
        "panel_vs37": lambda: panel("vs37", lit={"L1": 1, "L2": 1}),
        "panel_ps11": lambda: panel("ps11", lit={"V1": 1}),
        "courbe_cp50": courbe_cp50, "vue_eclatee_cp50": vue_eclatee_cp50, "coupe_garniture": coupe_garniture,
        "alignement": alignement, "pid_station": pid_station, "elec_armoire_pompes": elec_armoire_pompes,
        "coupe_cm80": coupe_cm80, "circuit_vs37": circuit_vs37, "elec_vs37": elec_vs37,
        "schema_ps11": schema_ps11, "audit_conso": audit_conso,
    }
    return {k: _save(f(), k) for k, f in figs.items()}


if __name__ == "__main__":
    print(build_all())
