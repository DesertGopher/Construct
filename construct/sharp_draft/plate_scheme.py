import os

from fpdf import FPDF
from pathlib import Path


def top_template(pdf):
    """Верхний штамп"""
    pdf.line(20, 30, 205, 30)
    pdf.line(20, 20, 205, 20)
    pdf.line(35, 5, 35, 30)
    pdf.line(95, 5, 95, 30)
    pdf.line(140, 5, 140, 30)
    pdf.line(155, 5, 155, 30)
    pdf.line(185, 5, 185, 30)
    top_s = f"Поз.{14*' '}Обозначение{19*' '}Наименование{8*' '}Кол.{5*' '}Масса ед кг.{5*' '}Масса"
    pdf.cell(0, 25, top_s, 0, 0, 'R')


def bottom_template(pdf):
    """Нижний штамп"""
    pdf.line(20, 237, 205, 237)
    for i in range(4):
        pdf.line(85, 247+i*15, 205, 247+i*15)

    pdf.line(155, 262, 155, 292)
    pdf.line(170, 262, 170, 277)
    pdf.line(185, 262, 185, 277)
    pdf.line(155, 267, 205, 267)

    pdf.line(85, 237, 85, 292)
    pdf.line(75, 237, 75, 292)
    pdf.line(60, 237, 60, 292)
    pdf.line(40, 237, 40, 292)
    pdf.line(50, 237, 50, 262)
    pdf.line(30, 237, 30, 262)

    for i in range(10):
        pdf.line(20, 242+i*5, 85, 242+i*5)

    pdf.set_font("GOST type A", size=10)
    bottom_s = f" Изм.   Кол   Лист  №док.   Подп.    Дата"
    pdf.text(21, 261, bottom_s)

    bottom_s = f"Стадия     Лист      Листов"
    pdf.text(157, 266, bottom_s)

    pdf.text(21, 266, "Нач. отдела")
    pdf.text(21, 271, "ГИП")
    pdf.text(21, 276, "Проверил")
    pdf.text(21, 281, "Нач. группы")
    pdf.text(21, 286, "Разработал")
    pdf.text(21, 291, "Н. контроль")


def side_template(pdf):
    """Боковой штамп"""
    pdf.line(0, 142, 20, 142)
    pdf.line(0, 208, 20, 208)

    pdf.line(5, 153, 20, 153)
    pdf.line(5, 168, 20, 168)
    pdf.line(5, 188, 20, 188)

    for i in range(4):
        pdf.line(5*i, 142, 5*i, 208)

    pdf.line(6, 292, 20, 292)
    pdf.line(6, 267, 20, 267)
    pdf.line(6, 232, 20, 232)

    pdf.line(6, 208, 6, 292)
    pdf.line(11, 208, 11, 292)


def top_template_text(pdf):
    pdf.set_font("GOST type A", size=12)
    pdf.text(23, 27, "POS")
    pdf.text(55, 27, "OBOZ")
    pdf.text(98, 27, "NAME")
    pdf.text(145, 27, "5")
    pdf.text(170, 27, "6")
    pdf.text(192, 27, "30")

    pdf.set_font("GOST type A", size=10)


def bottom_template_text(pdf, form):
    pdf.set_font("GOST type A", size=12)
    pdf.text(135, 243, str(form.code))
    pdf.text(135, 256, str(form.project))
    pdf.text(110, 271, str(form.object))
    pdf.text(162, 286, str(form.company))

    pdf.set_font("GOST type A", size=10)
    pdf.text(41, 276, str(form.author))
    pdf.text(41, 286, str(form.checker))
    pdf.text(162, 273, "Р")
    pdf.text(177, 273, "1")
    pdf.text(193, 273, "10")


def generate_pdf(form):
    pdf = FPDF(orientation='P', unit='mm', format=(210, 297))
    pdf.add_page()

    directory = Path(__file__).resolve().parent
    ttf_path = os.path.abspath(directory / 'scheme' / 'GOST_A.ttf')
    pdf.add_font('GOST type A', '', ttf_path, uni=True)
    pdf.set_auto_page_break(auto=False, margin=0.0)
    pdf.set_y(0)

    pdf.set_font("GOST type A", size=12)

    top_template(pdf)
    bottom_template(pdf)
    side_template(pdf)

    bottom_template_text(pdf, form)
    top_template_text(pdf)

    pdf.rect(0, 0, 210, 297)
    pdf.set_line_width(0.6)
    pdf.rect(20, 5, 185, 287)

    pdf.set_font("GOST type A", size=10)
    pdf.cell(0, 590, "Формат А4", 0, 0, 'R')
    file_name = "pdf12.pdf"
    pdf_path = os.path.abspath(directory / 'scheme' / file_name)
    pdf.output(pdf_path)
