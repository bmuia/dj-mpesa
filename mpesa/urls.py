from django.urls import path
from .views import (
    C2BPaymentValidationView,
    SimulateC2BPaymentView,
    ConfirmationView
)

urlpatterns = [
    path("api/c2b/validate/", C2BPaymentValidationView.as_view()),
    path("api/c2b/simulate/", SimulateC2BPaymentView.as_view()),
    path("api/c2b/confirmation/", ConfirmationView.as_view()),
]
