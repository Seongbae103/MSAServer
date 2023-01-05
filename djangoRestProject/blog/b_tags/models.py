from django.db import models

from blog.b_posts.models import B_post


class B_tag(models.Model):
    use_in_migration = True
    tag_id = models.CharField(primary_key=True, max_length=20)
    title = models.CharField(max_length=20)

    b_post = models.ForeignKey(B_post, on_delete=models.CASCADE)

    class Meta:
        db_table = "blog_tags"
    def __str__(self):
        return f'{self.pk} {self.title}'
# Create your models here.
