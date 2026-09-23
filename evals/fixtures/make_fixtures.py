#!/usr/bin/env python3
"""Generate the fictional test CVs used by the evals.

  python3 evals/fixtures/make_fixtures.py

Creates, next to this script:
  sample-cv-2022.docx / .pdf     an outdated CV (last updated 2022): A4, Cambria,
                                 teal centered header, uppercase teal headings,
                                 one UK spelling and a stale "6 years" claim
  linkedin-export-sample.pdf     a two-column profile shaped like LinkedIn's
                                 "Save to PDF" export (for detection tests)

Everyone and every company here is invented. Requires python-docx and LibreOffice.
"""
from __future__ import annotations

import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "skills" / "cv-refresh" / "scripts"))
from common import docx_to_pdf  # noqa: E402

TEAL = RGBColor(0x1B, 0x6F, 0x72)


def font(run, size, bold=False, color=None, italic=False, name="Cambria"):
    run.font.name = name
    rpr = run._r.get_or_add_rPr()
    rpr.rFonts.set(qn("w:hAnsi"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color


def para(doc, text="", size=10.5, bold=False, color=None, align=None, after=2, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(after)
    if align is not None:
        p.alignment = align
    if text:
        font(p.add_run(text), size, bold, color, italic)
    return p


def heading(doc, text):
    p = para(doc, text.upper(), size=11.5, bold=True, color=TEAL, after=3)
    p.paragraph_format.space_before = Pt(10)


def bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(1)
    font(p.add_run(text), 10.5)


def role(doc, title, company, dates):
    p = para(doc, after=1)
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(6.77), 2)  # right tab
    font(p.add_run(title), 10.5, bold=True)
    font(p.add_run(f", {company}"), 10.5)
    font(p.add_run(f"\t{dates}"), 10.5, italic=True)


def sample_cv():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.27), Inches(11.69)  # A4
    for side in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
        setattr(sec, side, Inches(0.75))
    para(doc, "Jordan Avery", size=22, bold=True, color=TEAL, align=WD_ALIGN_PARAGRAPH.CENTER, after=0)
    para(doc, "Data Engineer", size=12, align=WD_ALIGN_PARAGRAPH.CENTER, after=0)
    para(doc, "Tel Aviv, Israel  |  jordan.avery@example.com  |  linkedin.com/in/jordan-avery-example",
         size=10, align=WD_ALIGN_PARAGRAPH.CENTER, after=6)

    heading(doc, "Profile")
    para(doc, "Data engineer with 6 years of experience building batch data pipelines and BI platforms "
              "for retail and healthcare companies. Comfortable across the stack, from SQL modeling to "
              "Python ETL and dashboarding.")

    heading(doc, "Professional Experience")
    role(doc, "Senior Data Engineer", "Harborlight Logistics", "Apr 2022 – Present")
    bullet(doc, "Joined to build the company's new data platform.")
    role(doc, "Data Engineer", "Quillstone Retail", "Jan 2019 – Mar 2022")
    bullet(doc, "Built and maintained 40+ Airflow DAGs ingesting POS and e-commerce data into Amazon Redshift.")
    bullet(doc, "Migrated legacy SSIS jobs to Python, reducing nightly load time from 5 hours to 2 hours.")
    bullet(doc, "Optimised Redshift distribution and sort keys, cutting dashboard query times by 60%.")
    bullet(doc, "Designed a dimensional sales model used by 120 analysts across 3 countries.")
    bullet(doc, "Worked on data quality checks with Great Expectations.")
    role(doc, "BI Developer", "Pinecrest Health Analytics", "Aug 2016 – Dec 2018")
    bullet(doc, "Developed Tableau dashboards for hospital operations teams.")
    bullet(doc, "Wrote complex SQL for claims analysis in SQL Server.")
    bullet(doc, "Responsible for monthly reporting to 14 client hospitals.")

    heading(doc, "Technical Skills")
    for group, items in (("Languages", "Python, SQL, Bash"),
                         ("Data", "Airflow, Amazon Redshift, Great Expectations, SSIS, Tableau"),
                         ("Cloud", "AWS (S3, Glue, Lambda)")):
        p = para(doc, after=1)
        font(p.add_run(f"{group}: "), 10.5, bold=True)
        font(p.add_run(items), 10.5)

    heading(doc, "Education")
    role(doc, "B.Sc. Industrial Engineering and Management", "Ben-Gurion University of the Negev", "2012 – 2016")

    heading(doc, "Military Service")
    role(doc, "Operations Analyst", "IDF", "2009 – 2012")

    heading(doc, "Languages")
    para(doc, "Hebrew (Native)  ·  English (Fluent)")

    out = HERE / "sample-cv-2022.docx"
    doc.save(out)
    docx_to_pdf(out, HERE)


def cell_margin_none(table):
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "nil")
        borders.append(el)
    tbl_pr.append(borders)


def linkedin_export():
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    for side in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
        setattr(sec, side, Inches(0.5))
    table = doc.add_table(rows=1, cols=2)
    cell_margin_none(table)
    left, right = table.rows[0].cells
    left.width, right.width = Inches(2.3), Inches(5.2)
    gray = RGBColor(0x55, 0x55, 0x55)

    def add(cell, text, size=10, bold=False, color=None, after=2):
        p = cell.add_paragraph()
        p.paragraph_format.space_after = Pt(after)
        font(p.add_run(text), size, bold, color, name="Arial")

    add(left, "Contact", 12, True)
    add(left, "jordan.avery@example.com")
    add(left, "www.linkedin.com/in/jordan-avery-example (LinkedIn)", 9, color=gray, after=10)
    add(left, "Top Skills", 12, True)
    for s in ("Apache Airflow", "Amazon Redshift", "Data Modeling"):
        add(left, s)
    add(left, "Languages", 12, True)
    add(left, "Hebrew (Native or Bilingual)")
    add(left, "English (Full Professional)")

    add(right, "Jordan Avery", 24, True)
    add(right, "Data Engineering Team Lead at Harborlight Logistics", 12)
    add(right, "Tel Aviv District, Israel", 10, color=gray, after=10)
    add(right, "Summary", 14, True)
    add(right, "I build data platforms that people trust. Lakehouse, streaming and analytics engineering "
               "for logistics and retail.", after=10)
    add(right, "Experience", 14, True)
    add(right, "Harborlight Logistics", 12, True)
    add(right, "Data Engineering Team Lead")
    add(right, "January 2024 - Present (2 years 9 months)", 9, color=gray)
    add(right, "Senior Data Engineer")
    add(right, "April 2022 - December 2023 (1 year 9 months)", 9, color=gray, after=8)
    add(right, "Quillstone Retail", 12, True)
    add(right, "Data Engineer")
    add(right, "January 2019 - March 2022 (3 years 3 months)", 9, color=gray)
    add(right, "Built Airflow pipelines into Redshift for POS and e-commerce data. Migrated SSIS jobs to "
               "Python. Designed the dimensional sales model used by analysts in three countries.", after=8)
    add(right, "Pinecrest Health Analytics", 12, True)
    add(right, "BI Developer")
    add(right, "August 2016 - December 2018 (2 years 5 months)", 9, color=gray, after=10)
    add(right, "Education", 14, True)
    add(right, "Ben-Gurion University of the Negev", 12, True)
    add(right, "B.Sc., Industrial Engineering and Management · (2012 - 2016)")
    add(right, "Page 1 of 1", 8, color=gray)
    out = HERE / "linkedin-export-sample.docx"
    doc.save(out)
    docx_to_pdf(out, HERE)
    out.unlink()  # only the PDF is a fixture


if __name__ == "__main__":
    sample_cv()
    linkedin_export()
    print("fixtures written to", HERE)
