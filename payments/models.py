from io import BytesIO
from uuid import uuid4

from django.core.files import File
from django.db import models
from django.db.models.functions import Now
from djmoney.models.fields import MoneyField
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from bank.mixins import TimestampMixin
from payments.choices import Status


class Invoice(TimestampMixin):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='KZT'
    )
    redirect_url = models.URLField(
        max_length=1023,
    )
    callback_url = models.URLField(
        max_length=1023,
    )
    payment_url = models.URLField(
        max_length=1023,
    )
    callback_data = models.CharField(
        max_length=1023,
    )
    status = models.CharField(
        max_length=8,
        choices=Status.choices
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )
    expiration_date = models.DateTimeField()

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(expiration_date__gte=Now()),
                name='expiration_date_cannot_be_past_date'
            )
        ]


class Receipt(models.Model):
    invoice = models.ForeignKey(
        to=Invoice,
        on_delete=models.PROTECT,
        related_name='receipts'
    )
    pdf_file = models.FileField(upload_to='payments/static/receipts/')

    def generate_pdf(self, items: list):
        # Создание нового PDF-документа
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)

        c.setFont("Times-Roman", 12)

        # Define table properties
        table_x = 50
        table_y = 550
        table_width = 500
        row_height = 30

        # Set table header color
        c.setFillColor(colors.lightblue)
        c.rect(table_x, table_y, table_width, row_height, fill=True)
        c.setFillColor(colors.black)
        c.drawString(table_x + 5, table_y + 5, "Receipt Number: " + f'{self.invoice.id}')

        # Draw table rows with alternating colors
        colors_row1 = [colors.lightgrey, colors.white]
        colors_row2 = [colors.lightyellow, colors.white]
        colors_row = colors_row1

        for item in items:
            # Draw row background
            c.setFillColor(colors_row[0])
            c.rect(table_x, table_y - row_height, table_width, row_height, fill=True)

            # Draw item text
            c.setFillColor(colors.black)
            c.drawString(table_x + 5, table_y - row_height + 5, item)

            # Update row position and switch colors
            table_y -= row_height
            colors_row = colors_row2 if colors_row == colors_row1 else colors_row1

        # Draw total amount row
        c.setFillColor(colors_row[0])
        c.rect(table_x, table_y - row_height, table_width, row_height, fill=True)
        c.setFillColor(colors.black)
        c.drawString(table_x + 5, table_y - row_height + 5, f"Total Amount: {self.invoice.amount}")

        # Finish creating the PDF
        c.showPage()
        c.save()

        # Get the PDF content from the buffer
        buffer.seek(0)
        pdf_file = File(buffer)

        # Save the PDF file in the model
        self.pdf_file.save(f"receipt_{self.id}.pdf", pdf_file)

        # Close the buffer
        buffer.close()
