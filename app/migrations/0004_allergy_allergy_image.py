# Generated by Django 5.1 on 2024-11-16 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_allergy_customuser_allergy'),
    ]

    operations = [
        migrations.AddField(
            model_name='allergy',
            name='allergy_image',
            field=models.ImageField(blank=True, null=True, upload_to='allergies/', verbose_name='アレルギー食材イラスト'),
        ),
    ]