from django.db import models
class M_showtime(models.Model):
    use_in_migration = True
    showtime_id = models.CharField(primary_key=True, max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    class Meta:
        db_table = "movie_showtimes"
    def __str__(self):
        return f'{self.pk} {self.start_time} {self.end_time}'
# Create your models here.
