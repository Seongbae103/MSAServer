from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from django.utils import timezone

class User(models.Model):
    # These fields tie to the roles!
    ADMIN = 1
    MANAGER = 2
    EMPLOYEE = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (EMPLOYEE, 'Employee')
    )
    # CQRS의 Entity
    use_in_migrations = True
    user_email = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    birth = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    job = models.CharField(max_length=20)
    user_interests = models.CharField(max_length=20)
    token = models.CharField(max_length=20)
    # role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)

    def __str__(self):
        return f'ID: {self.pk}, \n' \
               f'이메일: {self.user_email} \n' \
               f'비번: {self.password} \n' \
               f'전화번호: {self.phone} \n' \
               f'생년월일: {self.birth} \n' \
               f'주소: {self.address} \n' \
               f'직업: {self.job} \n' \
               f'관심사: {self.user_interests} \n' \
               f'토큰: {self.token} \n' \

    class Meta:
        db_table = "users"
        verbose_name = 'user'
        verbose_name_plural = 'users'

