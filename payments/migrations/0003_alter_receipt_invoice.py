# Generated by Django 4.2.2 on 2023-06-25 01:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0002_receipt"),
    ]

    operations = [
        migrations.AlterField(
            model_name="receipt",
            name="invoice",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="receipts",
                to="payments.invoice",
            ),
        ),
    ]