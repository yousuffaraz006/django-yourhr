# Generated by Django 5.1 on 2024-08-30 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0008_alter_applicant_image_alter_applicant_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
