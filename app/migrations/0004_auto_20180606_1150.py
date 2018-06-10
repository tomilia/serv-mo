# Generated by Django 2.0.5 on 2018-06-06 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180606_1144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cnsextrafield',
            old_name='image',
            new_name='discount_price',
        ),
        migrations.AddField(
            model_name='cnsextrafield',
            name='original_price',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='cnsextrafield',
            name='period',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='cnsextrafield',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
