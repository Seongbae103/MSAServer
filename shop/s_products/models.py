from django.db import models
class S_product(models.Model):
    use_in_migration = True
    product_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField()
    price = models.CharField()
    image_url = models.CharField()
    class Meta:
        db_table = "shop_products"
    def __str__(self):
        return f'{self.pk} {self.name} {self.price} {self.image_url}'
# Create your models here.
