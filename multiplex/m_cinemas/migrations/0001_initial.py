# Generated by Django 4.1.3 on 2022-11-30 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='M_cinema',
            fields=[
                ('cinema_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('image_url', models.TextField()),
                ('address', models.TextField()),
                ('detail_address', models.TextField()),
            ],
            options={
                'db_table': 'movie_cinemas',
            },
        ),
    ]