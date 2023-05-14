# Generated by Django 3.2 on 2023-05-14 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_rental_return_due_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='book_images'),
        ),
        migrations.AlterField(
            model_name='rental',
            name='rental_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='rental',
            name='return_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rental',
            name='return_due_date',
            field=models.DateField(default=datetime.date(2023, 5, 21)),
        ),
    ]