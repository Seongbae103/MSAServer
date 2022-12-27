from django.db import models

from blog.b_posts.models import B_post
from blog.b_users.models import B_user


class B_comment(models.Model):
    use_in_migration = True
    comment_id = models.CharField(primary_key=True, max_length=20)
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_id = models.CharField(null=True)

    b_user = models.ForeignKey(B_user, on_delete=models.CASCADE)
    b_post = models.ForeignKey(B_post, on_delete=models.CASCADE)

    class Meta:
        db_table = "blog_comments"
    def __str__(self):
        return f'{self.pk} {self.content} {self.created_at} {self.updated_at} {self.parent_id}'
# Create your models here.
