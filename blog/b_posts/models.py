from django.db import models

from blog.b_users.models import B_user


class B_post(models.Model):
    use_in_migration = True
    post_id = models.AutoField(primary_key=True)
    title = models.TextField()
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    b_user = models.ForeignKey(B_user, on_delete=models.CASCADE)
    class Meta:
        db_table = "blog_posts"
    def __str__(self):
        return f'{self.pk} {self.title} {self.content} {self.create_at}' \
               f' {self.updated_at}'
# Create your models here.
