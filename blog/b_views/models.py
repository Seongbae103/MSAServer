from django.db import models
from blog.b_posts.models import B_post
from blog.b_users.models import B_user


class B_view(models.Model):
    use_in_migration = True
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    created_at = models.DateTimeField()

    b_user = models.ForeignKey(B_user, on_delete=models.CASCADE)
    b_post = models.ForeignKey(B_post, on_delete=models.CASCADE)
    class Meta:
        db_table = "blog_view"
    def __str__(self):
        return f'{self.pk} {self.title} {self.created_at}'
# Create your models here.
