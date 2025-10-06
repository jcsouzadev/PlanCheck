from flask import render_template, make_response
import pandas as pd
from io import BytesIO
from weasyprint import HTML

def gerar_pdf(template, **kwargs):
    """Gera um PDF a partir de um template HTML"""
    html_out = render_template(template, **kwargs)
    pdf = HTML(string=html_out).write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=relatorio.pdf'
    return response

def gerar_excel(dataframe, filename='relatorio.xlsx'):
    """Gera um arquivo Excel a partir de um DataFrame do pandas"""
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    dataframe.to_excel(writer, index=False, sheet_name='Relatório')
    writer.close()
    output.seek(0)
    response = make_response(output.read())
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response
