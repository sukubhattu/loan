from django.db import models

import uuid

from .constants import LOAN_TYPE, LOAN_STATUS

from users.models import UserProfile


class LoanOrder(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_loan')
    loan_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    loan_amount = models.FloatField()
    loan_remaining_amount = models.FloatField()
    loan_term = models.PositiveIntegerField()
    loan_type = models.CharField(max_length=2, choices=LOAN_TYPE)
    loan_status = models.CharField(max_length=20, default='processing', choices=LOAN_STATUS)
    is_approved = models.BooleanField(default=False)
    is_complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.loan_id)

    @classmethod
    def create_loan_order(cls, user_id, loan_type, loan_amount, loan_term):
        user_profile = UserProfile.objects.get(user_id=user_id)
        incomplete_loan_orders = cls.objects.filter(
            user_id=user_profile.id, loan_status='processing', is_approved=False, loan_type=loan_type
        )
        incomplete_loan_orders.update(loan_status='ignored')
        cls.objects.create(
            user=user_profile,
            loan_amount=loan_amount,
            loan_remaining_amount=loan_amount,
            loan_term=loan_term,
            loan_type=loan_type,
        )


class LoanOrderItem(models.Model):
    loan = models.ForeignKey(LoanOrder, on_delete=models.CASCADE, related_name='loan_order')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_loan_item')
    installment_amount = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
