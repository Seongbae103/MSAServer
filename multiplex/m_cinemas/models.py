from django.db import models
class M_cinema(models.Model):
    use_in_migration = True
    cinema_id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=20)
    image_url = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    detail_address = models.CharField(max_length=20)
    class Meta:
        db_table = "movie_cinemas"
    def __str__(self):
        return f'{self.pk} {self.title} {self.image_url} {self.address}' \
               f' {self.detail_address}'
# Create your models here.
