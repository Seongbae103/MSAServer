from django.db import models

class S_user(models.Model):
    use_in_migration = True
    shop_userid = models.CharField(primary_key=True, max_length=20)
    email = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    point = models.CharField(max_length=20)
    class Meta:
        db_table = "shop_users"
    def __str__(self):
        return f'{self.pk} {self.email} {self.nickname} {self.password} {self.point}'
# Create your models here.
