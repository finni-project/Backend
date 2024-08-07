# Generated by Django 5.0.4 on 2024-04-29 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='이메일')),
                ('name', models.CharField(max_length=16, verbose_name='이름')),
                ('birth', models.DateField(null=True, verbose_name='생일')),
                ('is_active', models.BooleanField(default=True, verbose_name='활성화')),
                ('is_staff', models.BooleanField(default=False, verbose_name='관리자')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
