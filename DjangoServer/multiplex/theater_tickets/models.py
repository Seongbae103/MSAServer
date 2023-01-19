from django.db import models
from security.users.models import User
class TheaterTicket(models.Model):
    use_in_migration = True
    theater_ticket_id = models.AutoField(primary_key=True)
    x = models.IntegerField()
    y = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = "movie_theater_tickets"
    def __str__(self):
        return f'{self.pk} {self.x} {self.y}'