from django.db import models

from blog.b_posts.models import B_post


class B_tag(models.Model):
    use_in_migration = True
    tag_id = models.AutoField(primary_key=True)
    title = models.TextField()

    b_post = models.ForeignKey(B_post, on_delete=models.CASCADE)

    class Meta:
        db_table = "blog_tags"
    def __str__(self):
        return f'{self.pk} {self.title}'
# Create your models here.
