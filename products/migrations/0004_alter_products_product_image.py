# Generated by Django 3.2 on 2023-02-18 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_products_has_colours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='product_image',
            field=models.ImageField(blank=True, default='placeholder', null=True, upload_to='', verbose_name='image'),
        ),
    ]
