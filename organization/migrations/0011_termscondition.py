# Generated by Django 3.1.5 on 2021-02-05 10:43

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0010_companyaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='TermsCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_text', ckeditor_uploader.fields.RichTextUploadingField()),
            ],
        ),
    ]
