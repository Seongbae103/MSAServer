from django.db import models
class M_user(models.Model):
    use_in_migration = True
    movie_userid = models.CharField(primary_key=True, max_length=20)
    email = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    age = models.CharField(max_length=20)
    class Meta:
        db_table = "movie_users"
    def __str__(self):
        return f'{self.pk} {self.email} {self.nickname} {self.password} {self.age}'
# Create your models here.
