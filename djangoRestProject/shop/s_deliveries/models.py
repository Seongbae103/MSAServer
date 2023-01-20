from django.db import models
class S_delivery(models.Model):
    use_in_migration = True
    delivery_id = models.CharField(primary_key=True, max_length=20)
    username = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    detail_address = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    class Meta:
        db_table = "shop_deliveries"
    def __str__(self):
        return f'{self.pk} {self.username} {self.address} {self.detail_address}' \
               f' {self.phone}'
# Create your models here.
