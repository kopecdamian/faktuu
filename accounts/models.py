from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.validators import RegexValidator

# new user model based on basic user model
class CustomUser(AbstractUser):
    nip_number = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)], blank=True, null=True)
    regon_number = models.IntegerField(validators=[MinValueValidator(100000000), MaxValueValidator(999999999)], blank=True, null=True)
    year = models.CharField(
        max_length=4,
        validators=[RegexValidator(regex=r'^\d{4}$', message="Niepoprawny format.")], 
        blank=True, null=True
    )
    bank_account_number = models.CharField(max_length=34, blank=True, null=True) 
    street = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

