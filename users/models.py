from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from .constants import GENDER

# These fields are added so that
# 1. Email field is shown while adding user from admin panel
# 2. Two user with same email will not be created
User._meta.get_field('email').blank = False
User._meta.get_field('email')._unique = True


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='userprofile')
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default='Male')
    dob = models.DateField(blank=True, null=True)
    contact_number = models.CharField(max_length=10, null=True, blank=True)
    loan_amount = models.FloatField(blank=True, null=True)
    loan_term = models.PositiveIntegerField(default=10)
    installment_amount = models.FloatField(blank=True, null=True)
    is_complete = models.BooleanField(default=False)
    is_approved_by_admin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.first_name + ' ' + self.last_name)[:20]


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_save_user_profile(sender, created, instance, **kwargs):
    # only create while new account is created
    if created:
        UserProfile.objects.create(user=instance)
        instance.userprofile.save()
