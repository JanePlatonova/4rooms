"""Builds fig1_closed_loop.png and closed_loop_teaching_article.docx (TNR 14, 1.5 spacing, journal margins)."""
import math
import re
import subprocess
import zipfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = Path(__file__).parent
MD = HERE / "closed_loop_teaching_article.md"
FIG = HERE / "fig1_closed_loop.png"
REF = HERE / "reference.docx"
OUT = HERE / "closed_loop_teaching_article.docx"

STEPS = [
    "Конспект\n(Markdown, GitHub Pages)",
    "Заняття\n+ локальний запис",
    "YouTube\nавтосубтитри",
    "ШІ-звіт\n(3 критерії)",
    "Беклог\nзобов'язань",
    "Правки\nконспекту",
]


def build_figure():
    fig, ax = plt.subplots(figsize=(6.3, 5.0), dpi=300)
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-1.2, 1.2)
    ax.axis("off")
    rx, ry = 1.4, 0.95
    pts = []
    for i, label in enumerate(STEPS):
        a = 2 * math.pi / 3 - i * 2 * math.pi / len(STEPS)
        x, y = rx * math.cos(a), ry * math.sin(a)
        pts.append((x, y))
        ax.add_patch(FancyBboxPatch((x - 0.5, y - 0.17), 1.0, 0.34, zorder=3,
                                    boxstyle="round,pad=0.02", fc="white", ec="black", lw=1))
        ax.text(x, y, label, ha="center", va="center", fontsize=8, family="serif", zorder=4)
    hw, hh = 0.58, 0.25
    for i in range(len(pts)):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % len(pts)]
        dx, dy = x2 - x1, y2 - y1
        t = min(hw / abs(dx) if dx else math.inf, hh / abs(dy) if dy else math.inf)
        ax.add_patch(FancyArrowPatch((x1 + dx * t, y1 + dy * t), (x2 - dx * t, y2 - dy * t),
                                     zorder=1, arrowstyle="-|>", mutation_scale=12,
                                     lw=1, color="black"))
    ax.text(0, 0, "Наступне\nзаняття", ha="center", va="center", fontsize=9,
            family="serif", style="italic")
    fig.savefig(FIG, bbox_inches="tight", facecolor="white")


def build_reference_docx():
    raw = subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"],
                         check=True, capture_output=True).stdout
    REF.write_bytes(raw)
    tmp = REF.with_suffix(".tmp")
    with zipfile.ZipFile(REF) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "word/styles.xml":
                xml = data.decode("utf-8")
                xml = re.sub(r'w:ascii="[^"]*"', 'w:ascii="Times New Roman"', xml)
                xml = re.sub(r'w:hAnsi="[^"]*"', 'w:hAnsi="Times New Roman"', xml)
                xml = re.sub(r'w:cs="[^"]*"', 'w:cs="Times New Roman"', xml)
                xml = re.sub(r'w:eastAsia="[^"]*"', 'w:eastAsia="Times New Roman"', xml)
                xml = re.sub(r'w:asciiTheme="[^"]*"\s*', "", xml)
                xml = re.sub(r'w:hAnsiTheme="[^"]*"\s*', "", xml)
                xml = re.sub(r'w:eastAsiaTheme="[^"]*"\s*', "", xml)
                xml = re.sub(r'w:cstheme="[^"]*"\s*', "", xml)
                xml = re.sub(r'<w:sz w:val="\d+"\s*/>', '<w:sz w:val="28"/>', xml)
                xml = re.sub(r'<w:szCs w:val="\d+"\s*/>', '<w:szCs w:val="28"/>', xml)
                xml = re.sub(r'<w:color w:val="[^"]*"[^/]*/>', '<w:color w:val="000000"/>', xml)
                xml = re.sub(r"<w:spacing [^/]*/>", '<w:spacing w:before="0" w:after="0" w:line="360" w:lineRule="auto"/>', xml)
                data = xml.encode("utf-8")
            if item.filename == "word/document.xml":
                xml = data.decode("utf-8")
                xml = re.sub(r"<w:pgSz[^/]*/>", '<w:pgSz w:w="11906" w:h="16838"/>', xml)
                xml = re.sub(r"<w:pgMar[^/]*/>", '<w:pgMar w:top="1134" w:right="851" w:bottom="1134" w:left="1701" w:header="709" w:footer="709" w:gutter="0"/>', xml)
                data = xml.encode("utf-8")
            dst.writestr(item, data)
    tmp.replace(REF)


def build_docx():
    md = MD.read_text(encoding="utf-8")
    md = re.sub(r"^\*Рис\. 1\.[^\n]*\*$",
                "![Рис. 1. Замкнутий цикл викладання](fig1_closed_loop.png){width=15cm}",
                md, flags=re.M)
    tmp_md = HERE / "_build.md"
    tmp_md.write_text(md, encoding="utf-8")
    subprocess.run(["pandoc", tmp_md.name, "-o", OUT.name, "--reference-doc", REF.name],
                   cwd=HERE, check=True)
    tmp_md.unlink()
    set_page_layout(OUT)


def set_page_layout(path):
    sect = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
            '<w:pgMar w:top="1134" w:right="851" w:bottom="1134" w:left="1701" '
            'w:header="709" w:footer="709" w:gutter="0"/></w:sectPr>')
    tmp = path.with_suffix(".tmp")
    with zipfile.ZipFile(path) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if item.filename == "word/document.xml":
                xml = re.sub(r"<w:sectPr.*?</w:sectPr>|<w:sectPr\s*/>", "", data.decode("utf-8"), flags=re.S)
                data = xml.replace("</w:body>", sect + "</w:body>").encode("utf-8")
            dst.writestr(item, data)
    tmp.replace(path)


if __name__ == "__main__":
    build_figure()
    build_reference_docx()
    build_docx()
    print(OUT)
