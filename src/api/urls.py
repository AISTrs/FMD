from django.urls import path, re_path
from . import views

urlpatterns = [
    path('api/committee_expense_data/<int:fiscal_id>/', views.get_committee_expense_data),
    re_path(r'^api/fiscal_data/(?:(?P<fiscal_id>\d+)/)?$', views.get_fiscal_data),
    re_path(r'^api/budget_data/(?:(?P<fiscal_id>\d+)/)?$', views.get_budget_data),
    re_path(r'^api/expense_data/(?:(?P<fiscal_id>\d+)/)?$', views.get_expense_data),
]