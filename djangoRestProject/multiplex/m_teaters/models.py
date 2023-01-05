from django.db import models
class M_theater(models.Model):
    use_in_migration = True
    theater_id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=20)
    seat = models.CharField(max_length=20)
    class Meta:
        db_table = "movie_theaters"
    def __str__(self):
        return f'{self.pk} {self.title} {self.seat}'
# Create your models here.
