from decimal import Decimal

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Transaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=100)),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=12,
                        validators=[
                            django.core.validators.MinValueValidator(
                                Decimal("0.01"), message="Amount must be greater than 0."
                            )
                        ],
                    ),
                ),
                ("type", models.CharField(choices=[("income", "Income"), ("expense", "Expense")], max_length=7)),
                ("category", models.CharField(max_length=50)),
                ("date", models.DateField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-date", "-id"],
            },
        ),
        migrations.AddConstraint(
            model_name="transaction",
            constraint=models.CheckConstraint(
                condition=models.Q(("amount__gt", 0)), name="transaction_amount_positive"
            ),
        ),
    ]
