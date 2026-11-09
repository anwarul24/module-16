import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .forms import TransactionForm
from .models import Transaction


def index(request):
    return render(request, "tracker/index.html")


def serialize(t):
    return {
        "id": t.id,
        "title": t.title,
        "amount": float(t.amount),
        "type": t.type,
        "category": t.category,
        "date": t.date.isoformat(),
    }


def parse_json(request):
    try:
        data = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def invalid(form):
    errors = {field: messages[0] for field, messages in form.errors.items()}
    return JsonResponse({"errors": errors}, status=400)


@require_http_methods(["GET", "POST"])
def transaction_list(request):
    if request.method == "GET":
        return JsonResponse([serialize(t) for t in Transaction.objects.all()], safe=False)

    data = parse_json(request)
    if data is None:
        return JsonResponse({"message": "Invalid JSON body."}, status=400)
    form = TransactionForm(data)
    if not form.is_valid():
        return invalid(form)
    return JsonResponse(serialize(form.save()), status=201)


@require_http_methods(["PUT", "DELETE"])
def transaction_detail(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return JsonResponse({"message": "Transaction not found."}, status=404)

    if request.method == "DELETE":
        transaction.delete()
        return HttpResponse(status=204)

    data = parse_json(request)
    if data is None:
        return JsonResponse({"message": "Invalid JSON body."}, status=400)
    form = TransactionForm(data, instance=transaction)
    if not form.is_valid():
        return invalid(form)
    return JsonResponse(serialize(form.save()))
