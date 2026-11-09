from django.urls import path

from . import views

app_name = "tracker"

urlpatterns = [
    path("", views.index, name="index"),
    path("api/transactions/", views.transaction_list, name="api_list"),
    path("api/transactions/<int:pk>/", views.transaction_detail, name="api_detail"),
]
