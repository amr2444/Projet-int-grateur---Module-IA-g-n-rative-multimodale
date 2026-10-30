from ref import MENTION, EQUIPEMENTS

FIG = "build/fig/"


def cover(title, subtitle, ident_rows, extra=None):
    blocks = [("title", title), ("sub", subtitle), ("space", 1.2),
              ("table", ["Rubrique", "Valeur"], ident_rows, [1, 2.2], None, None), ("space", 0.8),
              ("box", "info", "Ce document est <b>synthétique</b> : il a été rédigé pour le projet pédagogique MaintiDoc "
                              "(EMSI 2026). Le site, les marques MD-Pompes / MD-Air, les équipements et les personnes sont fictifs. "
                              "Il ne doit pas être utilisé pour intervenir sur un équipement réel.")]
    if extra:
        blocks += extra
    return blocks


def doc(meta, header, pages, lang="fr"):
    """meta = champs d'inventaire ; pages = liste de listes de blocs."""
    m = dict(meta)
    m.setdefault("langue", lang)
    m["pages"] = pages
    m["title"] = m["titre"]
    m["header"] = header
    m["mention"] = MENTION if lang == "fr" else "Synthetic document – MaintiDoc teaching project (EMSI 2026) – fictitious brands and data"
    m["version_label"] = m["version"]
    return m


def eq_list(*ids):
    return " ; ".join(ids)
