from django.db import models
from blog.b_posts.models import B_post
from blog.b_users.models import B_user


class B_view(models.Model):
    use_in_migration = True
    id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=20)
    created_at = models.CharField(max_length=20)

    b_user = models.ForeignKey(B_user, on_delete=models.CASCADE)
    b_post = models.ForeignKey(B_post, on_delete=models.CASCADE)
    class Meta:
        db_table = "blog_view"
    def __str__(self):
        return f'{self.pk} {self.title} {self.created_at}'
# Create your models here.
