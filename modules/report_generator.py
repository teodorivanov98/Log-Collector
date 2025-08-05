import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def generate_text_report(diagnostics, output_dir, server_name):
    filepath = os.path.join(output_dir, f"{server_name}_report.txt")
    with open(filepath, 'w') as f:
        for section, content in diagnostics.items():
            f.write(f"==== {section.upper()} ====\n")
            f.write(content + "\n\n")
    return filepath


def generate_html_report(diagnostics, output_dir, server_name):
    html = f"<html><head><title>{server_name} Diagnostics</title></head><body>"
    html += f"<h1>Diagnostics Report for {server_name}</h1>"
    html += f"<p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"

    for section, content in diagnostics.items():
        html += f"<h2>{section}</h2><pre>{content}</pre>"

    html += "</body></html>"

    filepath = os.path.join(output_dir, f"{server_name}_report.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    return filepath


def generate_pdf_report(diagnostics, output_dir, server_name):
    filepath = os.path.join(output_dir, f"{server_name}_report.pdf")
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    text = c.beginText(40, height - 50)
    text.setFont("Helvetica", 10)
    text.textLine(f"Diagnostics Report for {server_name}")
    text.textLine(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    text.textLine("")

    for section, content in diagnostics.items():
        text.textLine(f"==== {section.upper()} ====")
        for line in content.strip().split('\n'):
            text.textLine(line)
        text.textLine("")

    c.drawText(text)
    c.showPage()
    c.save()

    return filepath
