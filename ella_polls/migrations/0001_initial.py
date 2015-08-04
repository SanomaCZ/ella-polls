# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import ella.core.cache.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20150430_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.TextField(verbose_name='Choice text')),
                ('points', models.IntegerField(default=1, null=True, verbose_name='Points', blank=True)),
                ('votes', models.IntegerField(default=0, verbose_name='Votes', blank=True)),
            ],
            options={
                'verbose_name': 'Choice',
                'verbose_name_plural': 'Choices',
            },
        ),
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('text_announcement', models.TextField(default=b'', verbose_name='Text with announcement', blank=True)),
                ('text', models.TextField(verbose_name='Text')),
                ('text_results', models.TextField(verbose_name='Text with results')),
                ('active_from', models.DateTimeField(null=True, verbose_name='Active from', blank=True)),
                ('active_till', models.DateTimeField(null=True, verbose_name='Active till', blank=True)),
                ('publishable_ptr', models.OneToOneField(parent_link=True, related_name='contest_old', primary_key=True, serialize=False, to='core.Publishable')),
            ],
            options={
                'ordering': ('-active_from',),
                'verbose_name': 'Old contest',
                'verbose_name_plural': 'Old contests',
            },
            bases=('core.publishable', models.Model),
        ),
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Date and time')),
                ('name', models.CharField(max_length=200, verbose_name='First name')),
                ('surname', models.CharField(max_length=200, verbose_name='Last name')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('phonenumber', models.CharField(max_length=20, verbose_name='Phone number', blank=True)),
                ('address', models.CharField(max_length=200, verbose_name='Address', blank=True)),
                ('choices', models.TextField(verbose_name='Choices', blank=True)),
                ('count_guess', models.IntegerField(verbose_name='Count guess')),
                ('winner', models.BooleanField(default=False, verbose_name='Winner')),
                ('contest', ella.core.cache.fields.CachedForeignKey(verbose_name='Contest', to='ella_polls.Contest')),
                ('user', ella.core.cache.fields.CachedForeignKey(related_name='contestant_old_set', verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-datetime',),
                'verbose_name': 'Contestant',
                'verbose_name_plural': 'Contestants',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text_announcement', models.TextField(default=b'', verbose_name='Text with announcement', blank=True)),
                ('text', models.TextField(verbose_name='Text')),
                ('text_results', models.TextField(verbose_name='Text with results')),
                ('active_from', models.DateTimeField(null=True, verbose_name='Active from', blank=True)),
                ('active_till', models.DateTimeField(null=True, verbose_name='Active till', blank=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
            ],
            options={
                'ordering': ('-active_from',),
                'verbose_name': 'Poll',
                'verbose_name_plural': 'Polls',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField(verbose_name='Question text')),
                ('allow_multiple', models.BooleanField(default=False, verbose_name='Allow multiple choices')),
                ('allow_no_choice', models.BooleanField(default=False, verbose_name='Allow no choice')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('publishable_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Publishable')),
                ('text_announcement', models.TextField(default=b'', verbose_name='Text with announcement', blank=True)),
                ('text', models.TextField(verbose_name='Text')),
                ('text_results', models.TextField(verbose_name='Text with results')),
                ('active_from', models.DateTimeField(null=True, verbose_name='Active from', blank=True)),
                ('active_till', models.DateTimeField(null=True, verbose_name='Active till', blank=True)),
                ('has_correct_answers', models.BooleanField(verbose_name='Has correct answers')),
            ],
            options={
                'ordering': ('-active_from',),
                'verbose_name': 'Quiz',
                'verbose_name_plural': 'Quizes',
            },
            bases=('core.publishable', models.Model),
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='Title', blank=True)),
                ('text', models.TextField(verbose_name='Quiz results text')),
                ('points_from', models.IntegerField(null=True, verbose_name='Points dimension from')),
                ('points_to', models.IntegerField(null=True, verbose_name='Points dimension to')),
                ('count', models.IntegerField(verbose_name='Count')),
                ('quiz', ella.core.cache.fields.CachedForeignKey(verbose_name='Quiz', to='ella_polls.Quiz')),
            ],
            options={
                'verbose_name': 'Result',
                'verbose_name_plural': 'results',
            },
        ),
        migrations.CreateModel(
            name='SurveyVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True, verbose_name='Time')),
                ('ip_address', models.IPAddressField(null=True, verbose_name='IP Address')),
                ('user', ella.core.cache.fields.CachedForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-time',),
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True, verbose_name='Time')),
                ('ip_address', models.IPAddressField(null=True, verbose_name='IP Address')),
                ('poll', ella.core.cache.fields.CachedForeignKey(verbose_name='Poll', to='ella_polls.Poll')),
                ('user', ella.core.cache.fields.CachedForeignKey(verbose_name='User', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-time',),
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('question_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='ella_polls.Question')),
                ('active_from', models.DateTimeField(verbose_name='Active from')),
                ('active_till', models.DateTimeField(verbose_name='Active till')),
            ],
            options={
                'ordering': ('-active_from',),
                'verbose_name': 'Survey',
                'verbose_name_plural': 'Surveys',
            },
            bases=('ella_polls.question',),
        ),
        migrations.AddField(
            model_name='question',
            name='contest',
            field=ella.core.cache.fields.CachedForeignKey(verbose_name='Contest', blank=True, to='ella_polls.Contest', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=ella.core.cache.fields.CachedForeignKey(verbose_name='Quiz', blank=True, to='ella_polls.Quiz', null=True),
        ),
        migrations.AddField(
            model_name='poll',
            name='question',
            field=ella.core.cache.fields.CachedForeignKey(verbose_name='Question', to='ella_polls.Question', unique=True),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=ella.core.cache.fields.CachedForeignKey(verbose_name='Question', to='ella_polls.Question'),
        ),
        migrations.AddField(
            model_name='surveyvote',
            name='survey',
            field=ella.core.cache.fields.CachedForeignKey(verbose_name='Survey', to='ella_polls.Survey'),
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('contest', 'email')]),
        ),
    ]
