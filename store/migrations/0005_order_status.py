# Generated by Django 3.1.5 on 2021-01-20 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20210120_2011'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]
