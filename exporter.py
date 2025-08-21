import io
from flask import send_file
import pandas as pd
from fpdf import FPDF
from io import BytesIO

def export_to_csv(data):
    """Export DataFrame to CSV and return as Flask response."""
    output = io.StringIO()
    data.to_csv(output, index=False)
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv',
                        as_attachment=True, download_name='inventory.csv')

def export_to_excel(data):
    """Export DataFrame to Excel and return as Flask response."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        data.to_excel(writer, index=False, sheet_name='Inventory')
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        as_attachment=True, download_name='inventory.xlsx')


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def export_to_pdf(data):
    pdf = PDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Needle Inventory Report", ln=True, align='C')
    pdf.ln(10)

    # Refined column widths
    columns = [
        ("Stock Location", 55),
        ("Needle ID", 65),
        ("Min Stock", 25),
        ("Current Stock", 25),
        ("Target Stock", 25)
    ]

    # Table headers
    pdf.set_font("Arial", 'B', 10)
    for col_name, col_width in columns:
        pdf.cell(col_width, 10, col_name, border=1, align='C')
    pdf.ln()

    # Table rows
    pdf.set_font("Arial", '', 10)
    for _, row in data.iterrows():
        pdf.cell(columns[0][1], 10, str(row.get("stock location", "")), border=1)
        pdf.cell(columns[1][1], 10, str(row.get("needle id", "")), border=1)
        pdf.cell(columns[2][1], 10, str(row.get("minimum stock level", "")), border=1, align='R')
        pdf.cell(columns[3][1], 10, str(row.get("current stock level", "")), border=1, align='R')
        pdf.cell(columns[4][1], 10, str(row.get("target stock level", "")), border=1, align='R')
        pdf.ln()

    # Output as Flask response
    pdf_output = BytesIO(pdf.output(dest='S').encode('latin1'))
    pdf_output.seek(0)
    return send_file(pdf_output, download_name="needle_inventory.pdf", as_attachment=True)

