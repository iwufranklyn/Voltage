# Generated by Django 4.0.5 on 2022-06-13 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_product_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'managed': True, 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='available',
            new_name='display',
        ),
        migrations.AddField(
            model_name='product',
            name='trending',
            field=models.BooleanField(default=False),
        ),
    ]
