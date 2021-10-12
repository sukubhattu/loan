from django.db import models

import uuid

from .constants import LOAN_TYPE, LOAN_STATUS

from users.models import UserProfile


class LoanOrder(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_loan')
    loan_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    loan_amount = models.FloatField()
    loan_term = models.PositiveIntegerField()
    loan_type = models.CharField(max_length=2, choices=LOAN_TYPE)
    loan_status = models.CharField(max_length=20, default='processing', choices=LOAN_STATUS)
    is_approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


class LoanOrderItem(models.Model):
    loan = models.ForeignKey(LoanOrder, on_delete=models.CASCADE, related_name='loan')
    installment_amount = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
