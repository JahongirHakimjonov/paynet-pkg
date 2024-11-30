# Generated by Django 5.1.3 on 2024-11-30 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PaynetTransaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.IntegerField()),
                ("account_id", models.BigIntegerField()),
                ("transaction_id", models.BigIntegerField(unique=True)),
                ("service_id", models.IntegerField(blank=True, null=True)),
                (
                    "status",
                    models.IntegerField(
                        choices=[
                            (1, "Successfully completed"),
                            (2, "Cancelled transaction"),
                            (3, "Transaction not found"),
                        ],
                        default=3,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
