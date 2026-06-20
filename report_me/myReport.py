"""myReport.py."""

__title__: str = "myReport"
__version__: str = "0.1.0"
__author__: str = "Oliver Rudow"
__email__: str = "oliver.rudow@googlemail.com"
__copyright__: str = "Copyright 2026, Brain Center Höfen"

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import dataclasses
from typing import Optional
from datetime import date
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from file_base_me import myFileBase
from watchlist_definition_me import myReportTopListDefinitions

STR_PDF_REPORT_FILE_NAME: str = "my_shares_report.pdf"

STR_TITLE: str = 'SHARES REPORT'

COL_WIDTH_LARGE = [72, 180, 140, 36, 52, 36, 36, 36, 36, 36, 36, 36]
COL_WIDTH_LARGE_2 = [72, 180, 140, 36, 52, 36, 36, 180, 36]

def on_first_page(canvas, doc) -> None:

    str_title = getattr(doc, 'my_title', __title__)
    str_author = getattr(doc, 'my_author', __author__)
    str_date = getattr(doc, 'my_date', date.today())

    canvas.saveState()
    canvas.setFont('Helvetica-Bold', 24)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(50, 530, str_title)
    canvas.setFont('Helvetica', 12)
    canvas.drawString(50, 510, str_author)
    canvas.setFont('Helvetica', 12)
    canvas.drawString(50, 495, str_date)
    canvas.restoreState()

def on_later_pages(canvas, doc):

    str_page = f"{doc.page}"
    str_author = getattr(doc, 'my_author', __author__)

    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.HexColor('#666666'))
    canvas.drawString(50, 30, str_author)
    canvas.drawRightString(420.95, 30, str_page)
    canvas.restoreState()


@dataclasses.dataclass(init=False)
class MyReport:
    """

    """
    # FileBase
    _my_file: myFileBase.MyFileBase = dataclasses.field(repr=False, default_factory=type(myFileBase.MyFileBase))

    _str_working_directory: str = dataclasses.field(init=False, default=str)

    _str_pdf_report_file_name: str = dataclasses.field(init=False, default=str)

    _str_date_today: str = dataclasses.field(init=False, default=str)

    _str_title: str = dataclasses.field(init=False, default=str)

    _doc: SimpleDocTemplate = dataclasses.field(init=False, default=SimpleDocTemplate)

    _frame_portrait: Frame = dataclasses.field(init=False, default=Frame)

    _template_portrait: PageTemplate = dataclasses.field(init=False, default=PageTemplate)

    _frame_landscape: Frame = dataclasses.field(init=False, default=Frame)

    _template_landscape: PageTemplate = dataclasses.field(init=False, default=PageTemplate)

    _table_heading_style: ParagraphStyle = dataclasses.field(init=False, default=ParagraphStyle)

    _table_style: TableStyle = dataclasses.field(init=False, default=TableStyle)

    _story: list = dataclasses.field(init=False, default=list)

    _list_sectors: list = dataclasses.field(init=False, default=list)

    _list_industries: list = dataclasses.field(init=False, default=list)

    _list_overall_score: list = dataclasses.field(init=False, default=list)

    _list_twenty_day_change: list = dataclasses.field(init=False, default=list)

    _list_combined_overall_score_twenty_day_change: list = dataclasses.field(init=False, default=list)

    _list_combined_overall_score_twenty_day_change_array: list = dataclasses.field(init=False, default=list)

    def __init__(self, str_working_directory: Optional[str] = None,
                 str_pdf_report_filename: Optional[str] = None) -> None:
        super().__init__()

        # init FileBase w/o Config
        self._my_file = myFileBase.MyFileBase()

        # init working directory for Data Base
        if str_working_directory is not None:

            self._my_file.set_directory(str_working_directory)

        else:

            self._my_file.set_directory(myReportTopListDefinitions.STR_DATA_BASE_DIR_NAME)

        if str_pdf_report_filename is not None:

            self._my_file.set_file_name(str_pdf_report_filename)

        else:

            self._my_file.set_file_name(STR_PDF_REPORT_FILE_NAME)

        self._str_date_today = str(date.today())

        self._str_title = STR_TITLE

        self._doc = SimpleDocTemplate(
            self._my_file.get_entire_file_name,
            pagesize=landscape(A4),
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50,
        )

        self._doc.my_title = self._str_title

        self._doc.my_author = __author__

        self._doc.my_date = self._str_date_today

        self._init_table_heading_style()

        self._init_table_style()

        self._story = []

        self._list_sectors = []

        self._list_industries = []

        self._list_overall_score = []

        self._list_twenty_day_change = []

        self._list_combined_overall_score_twenty_day_change = []

        self._list_combined_overall_score_twenty_day_change_array = []

    def _init_table_heading_style(self) -> None:

        styles = getSampleStyleSheet()

        self._table_heading_style = ParagraphStyle(
            name='TableHeading',
            parent=styles['Heading2'],
            fontName='Helvetica',
            fontSize=12,
            spaceAfter=16,
            borderWidth=0,
            borderColor=colors.HexColor('#d0d0d0'),
        )

    def _init_table_style(self) -> None:

        self._table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4e78')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f2f2f2')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ])

    def _built_story(self) -> None:

        self._doc.build(self._story,
                        onFirstPage=on_first_page,
                        onLaterPages=on_later_pages)

    def _built_first_table(self) -> None:

        pdf_table = Table(self._list_sectors)

        pdf_table.setStyle(self._table_style)

        self._story.append(Spacer(1, 70))

        self._story.append(Paragraph("Sectors relative change in percent", self._table_heading_style))

        self._story.append(pdf_table)

    def _built_second_table(self) -> None:

        pdf_table = Table(self._list_industries)

        pdf_table.setStyle(self._table_style)

        self._story.append(Spacer(1, 70))

        self._story.append(Paragraph("Top Industries relative change in percent", self._table_heading_style))

        self._story.append(pdf_table)

    def _built_third_table(self) -> None:

        pdf_table = Table(self._list_overall_score, colWidths=COL_WIDTH_LARGE)

        pdf_table.setStyle(self._table_style)

        self._story.append(Paragraph("Overall Score", self._table_heading_style))

        self._story.append(pdf_table)

    def _built_forth_table(self) -> None:

        pdf_table = Table(self._list_twenty_day_change, colWidths=COL_WIDTH_LARGE)

        pdf_table.setStyle(self._table_style)

        self._story.append(Paragraph("20 day change percent", self._table_heading_style))

        self._story.append(pdf_table)

    def _built_fifth_table(self) -> None:

        pdf_table = Table(self._list_combined_overall_score_twenty_day_change, colWidths=COL_WIDTH_LARGE)

        pdf_table.setStyle(self._table_style)

        self._story.append(Paragraph("combined overall score and 20 day change percent", self._table_heading_style))

        self._story.append(pdf_table)

    def _built_sixth_table(self) -> None:

        pdf_table = Table(self._list_combined_overall_score_twenty_day_change_array, colWidths=COL_WIDTH_LARGE_2)

        pdf_table.setStyle(self._table_style)

        self._story.append(Paragraph("combined overall score and 20 day change percent array", self._table_heading_style))

        self._story.append(pdf_table)

    def set_sector_table(self, list_sectors: list) -> None:

        self._list_sectors = list_sectors

    def set_industries_table(self, list_industries: list) -> None:

        self._list_industries = list_industries

    def set_overall_score_table(self, list_overall_score: list) -> None:

        self._list_overall_score = list_overall_score

    def set_twenty_day_change_table(self, list_twenty_day_change: list) -> None:

        self._list_twenty_day_change = list_twenty_day_change

    def set_combined_overall_score_twenty_day_change_table(self, list_combined_overall_score_twenty_day_change: list) -> None:

        self._list_combined_overall_score_twenty_day_change = list_combined_overall_score_twenty_day_change

    def set_combined_overall_score_twenty_day_change_array_table(self, list_combined_overall_score_twenty_day_change_array: list) -> None:

        self._list_combined_overall_score_twenty_day_change_array = list_combined_overall_score_twenty_day_change_array

    def built_report(self):

        self._built_first_table()

        self._story.append(PageBreak())

        self._built_second_table()

        self._story.append(PageBreak())

        self._built_third_table()

        self._story.append(PageBreak())

        self._built_forth_table()

        self._story.append(PageBreak())

        self._built_fifth_table()

        self._story.append(PageBreak())

        self._built_sixth_table()

        self._built_story()

    def send_report(self) -> None:

        smtp_server = "smtp.gmail.com"

        sender_email = "oliver.rudow@googlemail.com"

        sender_password = "ekpp mxpn ibrl ftii"

        receiver_emails =  ["oliver.rudow@googlemail.com", "simone.rudow@gmx.de"]

        # 2. E-Mail-Nachricht erstellen
        msg = MIMEMultipart()

        msg['From'] = sender_email

        msg['To'] = ", ".join(receiver_emails)

        msg['Subject'] = "Automatischer Dateiversand"

        # E-Mail-Text hinzufügen
        body = "Hallo, im Anhang befindet sich die gewünschte Datei."

        msg.attach(MIMEText(body, 'plain'))

        # 3. Datei einlesen und anhängen
        try:

            with open(self._my_file.get_entire_file_name, "rb") as f:

                part = MIMEApplication(f.read(), Name=self._my_file.get_entire_file_name)

            # Content-Disposition für Dateianhang setzen
            part['Content-Disposition'] = f'attachment; filename="{self._my_file.get_entire_file_name}"'

            msg.attach(part)

        except FileNotFoundError:

            print(f"Die Datei '{self._my_file.get_entire_file_name}' wurde nicht gefunden.")

        try:

            server = smtplib.SMTP_SSL(smtp_server, 465)

            server.login(sender_email, sender_password)

            server.sendmail(sender_email, receiver_emails, msg.as_string())

            print("E-Mail wurde erfolgreich versendet!")

        except Exception as e:

            print(f"Fehler beim Senden: {e}")


if __name__ == "__main__":
    myReport = MyReport()
    myReport.set_sector_table(['test'])
