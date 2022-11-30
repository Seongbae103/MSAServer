from django.db import models
class S_product(models.Model):
    use_in_migration = True
    product_id = models.AutoField(primary_key=True)
    name = models.TextField()
    price = models.TextField()
    image_url = models.TextField()
    class Meta:
        db_table = "shop_products"
    def __str__(self):
        return f'{self.pk} {self.name} {self.price} {self.image_url}'
# Create your models here.
