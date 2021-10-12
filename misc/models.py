from django.db import models


class UserLoanInstallmentPaymentSession(models.Model):
    session_id = models.TextField()
