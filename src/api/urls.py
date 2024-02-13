from django.urls import path
from . import views

urlpatterns = [
    path("api/ledgerdata/", views.get_ledger_data)
]
