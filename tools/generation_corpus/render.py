"""Moteur de rendu PDF : un document = une liste de pages, chaque page = une liste de blocs.
Le numéro de page de chaque figure / tableau est donc maîtrisé (citations vérifiables)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
                                TableStyle, Image, PageBreak, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader

FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", FD + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("DVBI", FD + "DejaVuSans-BoldOblique.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVBI")

S = {
    "title": ParagraphStyle("t", fontName="DVB", fontSize=20, leading=25, spaceAfter=10, alignment=TA_CENTER),
    "sub": ParagraphStyle("s", fontName="DV", fontSize=12, leading=16, alignment=TA_CENTER, textColor=colors.HexColor("#333333")),
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=13.5, leading=17, spaceBefore=4, spaceAfter=6, textColor=colors.HexColor("#123a6b")),
    "h2": ParagraphStyle("h2", fontName="DVB", fontSize=11, leading=14, spaceBefore=6, spaceAfter=3),
    "p": ParagraphStyle("p", fontName="DV", fontSize=9.6, leading=13.2, spaceAfter=5),
    "li": ParagraphStyle("li", fontName="DV", fontSize=9.6, leading=13, leftIndent=14, bulletIndent=4, spaceAfter=2),
    "cap": ParagraphStyle("c", fontName="DVI", fontSize=8.6, leading=11, alignment=TA_CENTER, spaceAfter=8, spaceBefore=2),
    "cell": ParagraphStyle("cell", fontName="DV", fontSize=8.2, leading=10.2),
    "cells": ParagraphStyle("cells", fontName="DV", fontSize=6.9, leading=8.6),
    "cellbs": ParagraphStyle("cellbs", fontName="DVB", fontSize=6.9, leading=8.6, textColor=colors.white),
    "cellb": ParagraphStyle("cellb", fontName="DVB", fontSize=8.2, leading=10.2, textColor=colors.white),
    "note": ParagraphStyle("n", fontName="DV", fontSize=9.2, leading=12.5),
    "tiny": ParagraphStyle("tiny", fontName="DV", fontSize=5, leading=6, textColor=colors.HexColor("#c8c8c8")),
}

W, H = A4
MARG = 1.8 * cm
CW = W - 2 * MARG


def _table(header, rows, widths=None, head_color="#123a6b"):
    small = len(header) > 7
    data = [[Paragraph(str(h), S["cellbs" if small else "cellb"]) for h in header]]
    for r in rows:
        data.append([Paragraph(str(c), S["cells" if small else "cell"]) for c in r])
    if widths:
        tot = sum(widths)
        widths = [CW * w / tot for w in widths]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(head_color)),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#8a8a8a")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eef2f7")]),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return t


def _box(text, kind="warn"):
    col = {"warn": "#fff3cd", "danger": "#f8d7da", "info": "#e2ecf8"}[kind]
    brd = {"warn": "#d39e00", "danger": "#b02a37", "info": "#123a6b"}[kind]
    lab = {"warn": "ATTENTION", "danger": "DANGER", "info": "NOTE"}[kind]
    t = Table([[Paragraph(f"<b>{lab} –</b> {text}", S["note"])]], colWidths=[CW])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(col)),
                           ("BOX", (0, 0), (-1, -1), 1.2, colors.HexColor(brd)),
                           ("LEFTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 5),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    return t


def build_pdf(doc, out_path):
    """doc: dict(id, title, subtitle, header, version, date, lang, pages=[[blocs]], mention)
    blocs: ('h1',t) ('h2',t) ('p',t) ('ul',[t]) ('ol',[t]) ('table',hdr,rows,widths,caption,elem_id)
           ('fig',png,width_cm,caption,elem_id) ('box',kind,text) ('space',h) ('tiny',t)
    Retourne la liste des éléments visuels [(type, elem_id, page)]."""
    visuals = []
    story = []
    n = len(doc["pages"])
    for pi, page in enumerate(doc["pages"], start=1):
        for b in page:
            k = b[0]
            if k == "title":
                story += [Spacer(1, 3 * cm), Paragraph(b[1], S["title"])]
            elif k == "sub":
                story.append(Paragraph(b[1], S["sub"]))
            elif k in ("h1", "h2", "p"):
                story.append(Paragraph(b[1], S[k]))
            elif k == "tiny":
                story.append(Paragraph(b[1], S["tiny"]))
            elif k in ("ul", "ol"):
                for i, it in enumerate(b[1], 1):
                    story.append(Paragraph(it, S["li"], bulletText="•" if k == "ul" else f"{i}."))
            elif k == "table":
                _, hdr, rows, widths, cap, eid = b
                items = [_table(hdr, rows, widths)]
                if cap:
                    items.append(Paragraph(cap, S["cap"]))
                story.append(KeepTogether(items) if len(rows) < 14 else items[0])
                if cap and len(rows) >= 14:
                    story.append(items[1])
                if eid:
                    visuals.append(("tableau", eid, pi, cap))
            elif k == "fig":
                _, png, wcm, cap, eid = b
                from PIL import Image as PI
                im = PI.open(png)
                w = wcm * cm
                h = w * im.height / im.width
                story.append(KeepTogether([Image(png, width=w, height=h), Paragraph(cap, S["cap"])]))
                visuals.append(("figure", eid, pi, cap))
            elif k == "box":
                story += [_box(b[2], b[1]), Spacer(1, 6)]
            elif k == "space":
                story.append(Spacer(1, b[1] * cm))
        if pi < n:
            story.append(PageBreak())

    def on_page(c, d):
        c.saveState()
        pn = c.getPageNumber()
        c.setFont("DVB", 8)
        c.setFillColor(colors.HexColor("#123a6b"))
        c.drawString(MARG, H - 1.15 * cm, doc["header"])
        c.setFont("DV", 8)
        c.drawRightString(W - MARG, H - 1.15 * cm, f"{doc['version']}")
        c.setStrokeColor(colors.HexColor("#123a6b"))
        c.line(MARG, H - 1.3 * cm, W - MARG, H - 1.3 * cm)
        c.line(MARG, 1.35 * cm, W - MARG, 1.35 * cm)
        c.setFont("DVI", 7)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(MARG, 0.95 * cm, doc.get("mention", ""))
        c.setFont("DV", 8)
        c.drawRightString(W - MARG, 0.95 * cm, f"Page {pn}/{n}")
        c.restoreState()

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    d = BaseDocTemplate(out_path, pagesize=A4, leftMargin=MARG, rightMargin=MARG,
                        topMargin=1.7 * cm, bottomMargin=1.7 * cm, title=doc["title"],
                        author="Équipe ELBELLAOUI-ELYOUNESSI (document synthétique)",
                        subject=doc.get("mention", ""))
    fr = Frame(MARG, 1.7 * cm, CW, H - 3.4 * cm, id="f")
    d.addPageTemplates([PageTemplate("p", frames=[fr], onPage=on_page)])
    d.build(story)
    real = len(PdfReader(out_path).pages)
    if real != n:
        raise RuntimeError(f"{doc['id']}: {real} pages produites au lieu de {n} (débordement)")
    return visuals
