import random
from uuid import uuid4

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    contact_number = PhoneNumberField(blank=True, null=True, verbose_name="Contact Number")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    address = models.TextField(blank=True, null=True, verbose_name="Residence Address")
    document = models.FileField(blank=True, null=True, upload_to='documents/', verbose_name="Aadhar Card")
    share_no = models.PositiveIntegerField(blank=True, null=True, verbose_name="No of Share")
    share_price = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=2,
                                      verbose_name="Price of Share")
    referral_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return "ID Pin: {}".format(self.username)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only generate referral code for new objects
            self.referral_code = get_random_string(10).upper()
        super(User, self).save(*args, **kwargs)


class SystemMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='%(class)s_created_by')
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                    related_name='%(class)s_modified_by')

    class Meta:
        abstract = True


class IDPinGenerate(SystemMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    id_pin = models.PositiveIntegerField(unique=True, validators=[
        MinValueValidator(10000000),
        MaxValueValidator(99999999)
    ])
    share_no = models.PositiveIntegerField(verbose_name="No of Share")
    share_price = models.FloatField(verbose_name="Price of Share")
    created_user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True,
                                     related_name='%(class)s_created_user')

    def __str__(self):
        return "ID Pin: {} Share No: {} Share Price: {}".format(self.id_pin, self.share_no, self.share_price)

    def save(self, *args, **kwargs):
        if not self.id_pin:
            self.id_pin = self.generate_unique_id_pin()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_unique_id_pin():
        while True:
            id_pin = random.randint(10000000, 99999999)
            if not IDPinGenerate.objects.filter(id_pin=id_pin).exists():
                return id_pin
