# Generated by Django 4.1.3 on 2022-11-30 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='B_user',
            fields=[
                ('blog_userid', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.TextField()),
                ('nickname', models.TextField()),
                ('password', models.TextField()),
            ],
            options={
                'db_table': 'blog_users',
            },
        ),
    ]
