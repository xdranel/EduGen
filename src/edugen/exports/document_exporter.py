from datetime import datetime
from html import escape


class DocumentExporter:
    def to_markdown(self, topic: str, content: str) -> str:
        return f"# EduGen AI Learning Material\n\n**Topic:** {topic}\n\n{content.strip()}\n"

    def to_text(self, topic: str, content: str) -> str:
        return f"EduGen AI Learning Material\nTopic: {topic}\nGenerated: {datetime.now().isoformat()}\n\n{content.strip()}\n"

    def to_html(self, topic: str, content: str) -> str:
        body = escape(content.strip()).replace("\n", "<br>\n")
        return (
            "<!doctype html>\n"
            '<html lang="en">\n'
            "<head><meta charset=\"utf-8\"><title>EduGen AI Export</title></head>\n"
            f"<body><h1>EduGen AI Learning Material</h1><p><strong>Topic:</strong> {escape(topic)}</p><main>{body}</main></body>\n"
            "</html>\n"
        )

    def to_pdf(self, topic: str, content: str) -> bytes:
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.pdfgen import canvas
        except ImportError as error:
            raise RuntimeError("Install reportlab to export PDF files.") from error

        from io import BytesIO

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        y = height - 72
        pdf.setTitle(f"EduGen AI - {topic}")
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(72, y, "EduGen AI Learning Material")
        y -= 28
        pdf.setFont("Helvetica", 11)
        pdf.drawString(72, y, f"Topic: {topic}")
        y -= 28

        for line in content.splitlines():
            if y < 72:
                pdf.showPage()
                pdf.setFont("Helvetica", 11)
                y = height - 72
            pdf.drawString(72, y, line[:100])
            y -= 16

        pdf.save()
        return buffer.getvalue()
