# Generated by Django 5.1 on 2024-08-30 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0010_alter_applicant_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='docs/'),
        ),
    ]
