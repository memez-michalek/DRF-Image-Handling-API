# Generated by Django 3.2.6 on 2021-10-07 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_app', '0004_alter_link_issued_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='issued_at',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
