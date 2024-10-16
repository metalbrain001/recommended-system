# Generated by Django 4.2.16 on 2024-10-12 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0006_movie_imdbid_movie_tmdbid_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(
                blank=True,
                help_text=(
                    "The groups this user belongs to."
                    "A user will get all permissions"
                    "granted to each of their groups."
                ),
                related_name='user_set',
                related_query_name='user',
                to='auth.group',
                verbose_name='groups',
            ),
        ),
    ]
