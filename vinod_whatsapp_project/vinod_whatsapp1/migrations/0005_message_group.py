# Generated by Django 4.2.2 on 2023-07-20 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vinod_whatsapp1', '0004_video_image_document_audio'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_messages', to='vinod_whatsapp1.group'),
        ),
    ]