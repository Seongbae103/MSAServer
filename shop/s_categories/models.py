from django.db import models
class S_category(models.Model):
    use_in_migration = True
    category_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20)
    class Meta:
        db_table = "shop_categories"
    def __str__(self):
        return f'{self.pk} {self.name}'
# Create your models here.
