# Generated by Django 3.2.6 on 2021-10-07 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='default/')),
                ('smaller_thumbnail', models.ImageField(editable=False, upload_to='')),
                ('bigger_thumbnail', models.ImageField(editable=False, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('is_bigger_thmbnail_avalible', models.BooleanField(default=False)),
                ('is_original_upload_link_avalible', models.BooleanField(default=False)),
                ('expiring_link', models.BooleanField(default=False)),
                ('smaller_thumbnail_size', models.IntegerField(default=200)),
                ('bigger_thumbnail_size', models.IntegerField(default=400)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='image_app.plan')),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_direction', models.URLField(unique=True)),
                ('issued_at', models.DateTimeField()),
                ('timeout', models.IntegerField(default=300)),
                ('is_expired', models.BooleanField(default=False)),
                ('img', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='image_app.img')),
            ],
        ),
        migrations.AddField(
            model_name='img',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='image_app.user'),
        ),
    ]
