# Generated by Django 5.1.6 on 2025-03-01 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('society', '0002_post_created_at_post_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
