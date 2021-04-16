# Generated by Django 2.2.10 on 2021-04-16 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0004_question_question_type'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.CharField(max_length=36, verbose_name='user unique identifier')),
                ('is_anonymous', models.BooleanField(default=False)),
                ('survey', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='surveys.Survey')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('choices', models.ManyToManyField(to='surveys.Choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.Question')),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='users.Response')),
            ],
        ),
    ]
