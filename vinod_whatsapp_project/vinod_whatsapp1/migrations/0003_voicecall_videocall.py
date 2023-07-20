# Generated by Django 4.2.2 on 2023-07-20 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vinod_whatsapp1', '0002_groupchat_call'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoiceCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initiated_at', models.DateTimeField(auto_now_add=True)),
                ('call_status', models.CharField(choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing'), ('answered', 'Answered'), ('ended', 'Ended')], max_length=20)),
                ('caller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voice_calls_made', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voice_calls_received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VideoCall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initiated_at', models.DateTimeField(auto_now_add=True)),
                ('call_status', models.CharField(choices=[('incoming', 'Incoming'), ('outgoing', 'Outgoing'), ('answered', 'Answered'), ('ended', 'Ended')], max_length=20)),
                ('caller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_calls_made', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_calls_received', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]