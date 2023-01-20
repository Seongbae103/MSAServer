from django.db import models
class S_order(models.Model):
    use_in_migration = True
    order_id = models.CharField(primary_key=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "shop_orders"
    def __str__(self):
        return f'{self.pk} {self.created_at}'
# Create your models here.
