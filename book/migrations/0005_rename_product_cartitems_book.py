# Generated by Django 4.0.5 on 2022-08-30 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0004_rename_book_cartitems_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitems',
            old_name='product',
            new_name='book',
        ),
    ]