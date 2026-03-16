# utils/pdf.py

import os
import re
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem,
    HRFlowable,
)


def _clean_inline_markdown(text: str) -> str:
    if not text:
        return ""

    text = text.strip()

    # remove negrito markdown **texto**
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

    # remove itálico simples *texto*
    text = re.sub(r"(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)

    return text.strip()


def _parse_markdown_lines(text: str):
    """
    Converte texto estilo markdown simples em blocos estruturados:
    - title
    - heading
    - subheading
    - bullet
    - paragraph
    """
    blocks = []

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            blocks.append(("spacer", ""))
            continue

        if line.startswith("### "):
            blocks.append(("heading", _clean_inline_markdown(line[4:])))
            continue

        if line.startswith("#### "):
            blocks.append(("subheading", _clean_inline_markdown(line[5:])))
            continue

        if line.startswith("- "):
            blocks.append(("bullet", _clean_inline_markdown(line[2:])))
            continue

        if re.match(r"^\d+\.\s+", line):
            blocks.append(("bullet", _clean_inline_markdown(re.sub(r"^\d+\.\s+", "", line))))
            continue

        blocks.append(("paragraph", _clean_inline_markdown(line)))

    return blocks


def _add_header_footer(canvas, doc):
    canvas.saveState()

    width, height = A4

    # linha superior
    canvas.setStrokeColor(colors.HexColor("#D1D5DB"))
    canvas.setLineWidth(0.6)
    canvas.line(20 * mm, height - 18 * mm, width - 20 * mm, height - 18 * mm)

    # cabeçalho
    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(colors.HexColor("#1F2937"))
    canvas.drawString(20 * mm, height - 14 * mm, "AgentAI Nexus - Relatório Executivo")

    # rodapé
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawString(20 * mm, 10 * mm, f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    canvas.drawRightString(width - 20 * mm, 10 * mm, f"Página {doc.page}")

    canvas.restoreState()


def generate_pdf(text, path, title="Relatório Executivo", subtitle="Análise Estratégica Gerada por IA"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        leftMargin=22 * mm,
        rightMargin=22 * mm,
        topMargin=28 * mm,
        bottomMargin=18 * mm,
        title=title,
        author="AgentAI Nexus",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#111827"),
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "CustomSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#6B7280"),
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=8,
    )

    subheading_style = ParagraphStyle(
        "CustomSubHeading",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#334155"),
        spaceBefore=6,
        spaceAfter=5,
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=16,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=8,
    )

    bullet_style = ParagraphStyle(
        "CustomBullet",
        parent=body_style,
        leftIndent=4,
        firstLineIndent=0,
        spaceAfter=4,
    )

    meta_style = ParagraphStyle(
        "MetaStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#94A3B8"),
        spaceAfter=10,
    )

    elements = []

    # capa simples / topo elegante
    elements.append(Paragraph(title, title_style))
    elements.append(Paragraph(subtitle, subtitle_style))
    elements.append(
        Paragraph(
            f"Documento gerado automaticamente em {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
            meta_style,
        )
    )
    elements.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor("#CBD5E1")))
    elements.append(Spacer(1, 10))

    blocks = _parse_markdown_lines(text)

    bullet_buffer = []

    def flush_bullets():
        nonlocal bullet_buffer
        if bullet_buffer:
            bullet_items = [
                ListItem(Paragraph(item, bullet_style), leftIndent=0) for item in bullet_buffer
            ]
            elements.append(
                ListFlowable(
                    bullet_items,
                    bulletType="bullet",
                    start="circle",
                    leftIndent=12,
                    bulletFontName="Helvetica",
                    bulletFontSize=8,
                )
            )
            elements.append(Spacer(1, 6))
            bullet_buffer = []

    for block_type, content in blocks:
        if block_type == "spacer":
            flush_bullets()
            elements.append(Spacer(1, 4))

        elif block_type == "heading":
            flush_bullets()
            elements.append(Paragraph(content, heading_style))

        elif block_type == "subheading":
            flush_bullets()
            elements.append(Paragraph(content, subheading_style))

        elif block_type == "bullet":
            bullet_buffer.append(content)

        elif block_type == "paragraph":
            flush_bullets()
            elements.append(Paragraph(content, body_style))

    flush_bullets()

    doc.build(elements, onFirstPage=_add_header_footer, onLaterPages=_add_header_footer)
    return path