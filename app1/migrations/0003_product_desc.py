# Generated by Django 4.2.4 on 2023-08-17 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_alter_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='desc',
            field=models.CharField(default='', max_length=300),
        ),
    ]