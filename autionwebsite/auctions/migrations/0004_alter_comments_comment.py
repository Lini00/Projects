# Generated by Django 3.2.13 on 2022-08-30 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20220830_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
