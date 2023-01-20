from django.db import models
class M_theaterTicket(models.Model):
    use_in_migration = True
    theater_ticket_id = models.CharField(primary_key=True, max_length=20)
    x = models.IntegerField()
    y = models.IntegerField()
    class Meta:
        db_table = "movie_theater_tickets"
    def __str__(self):
        return f'{self.pk} {self.x} {self.y}'
# Create your models here.
