from django import forms

from .models import Transaction


class TransactionForm(forms.ModelForm):
    """Server-side validation for add and edit requests."""

    class Meta:
        model = Transaction
        fields = ["title", "amount", "type", "category", "date"]
        error_messages = {
            "title": {
                "required": "Enter a title.",
                "max_length": "Title must be 100 characters or fewer.",
            },
            "amount": {
                "required": "Enter an amount.",
                "invalid": "Enter a valid amount.",
                "max_digits": "Amount is too large.",
                "max_whole_digits": "Amount is too large.",
                "max_decimal_places": "Use at most 2 decimal places.",
            },
            "type": {
                "required": "Choose income or expense.",
                "invalid_choice": "Choose income or expense.",
            },
            "category": {
                "required": "Choose a category.",
                "max_length": "Category is too long.",
            },
            "date": {
                "required": "Choose a date.",
                "invalid": "Choose a valid date.",
            },
        }
