from django.db import models
class B_user(models.Model):
    use_in_migration = True
    blog_userid = models.CharField(primary_key=True, max_length=20)
    email = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    birth = models.CharField(max_length=20)
    class Meta:
        db_table = "blog_users"
    def __str__(self):
        return f'{self.pk} {self.email} {self.nickname} {self.password}'
# Create your models here.
