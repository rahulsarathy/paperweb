# Generated by Django 2.2.7 on 2020-04-28 16:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reading_list', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('twitter_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=500)),
                ('reply_to', models.CharField(default=None, max_length=64, null=True)),
                ('quote', models.CharField(default=None, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TwitterCredentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', encrypted_model_fields.fields.EncryptedCharField()),
                ('secret', encrypted_model_fields.fields.EncryptedCharField()),
                ('since_id', models.CharField(default=None, max_length=30, null=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TweetLink',
            fields=[
                ('url', models.URLField(primary_key=True, serialize=False)),
                ('tco_url', models.URLField(default=None, null=True)),
                ('article', models.ForeignKey(db_column='tweetlink_article', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='reading_list.Article')),
                ('tweet_parent', models.ForeignKey(db_column='tweet_parent', on_delete=django.db.models.deletion.CASCADE, to='twitter.Tweet')),
            ],
        ),
    ]
