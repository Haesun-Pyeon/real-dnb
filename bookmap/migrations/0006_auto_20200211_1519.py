# Generated by Django 2.2.6 on 2020-02-11 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookmap', '0005_auto_20200204_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookstore',
            name='img',
            field=models.URLField(blank=True, null=True),
        ),
    ]
