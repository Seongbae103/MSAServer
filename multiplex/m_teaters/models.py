from django.db import models
class M_theater(models.Model):
    use_in_migration = True
    theater_id = models.AutoField(primary_key=True)
    title = models.TextField()
    seat = models.TextField()
    class Meta:
        db_table = "movie_theaters"
    def __str__(self):
        return f'{self.pk} {self.title} {self.seat}'
# Create your models here.
