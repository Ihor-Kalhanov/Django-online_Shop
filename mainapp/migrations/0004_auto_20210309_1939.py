# Generated by Django 3.1.7 on 2021-03-09 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20210309_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smartphone',
            name='sd_volume_max',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Max OP'),
        ),
    ]
