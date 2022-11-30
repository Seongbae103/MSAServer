from django.db import models

class S_user(models.Model):
    use_in_migration = True
    shop_userid = models.AutoField(primary_key=True)
    email = models.TextField()
    nickname = models.TextField()
    password = models.TextField()
    point = models.TextField()
    class Meta:
        db_table = "shop_users"
    def __str__(self):
        return f'{self.pk} {self.email} {self.nickname} {self.password} {self.point}'
# Create your models here.
