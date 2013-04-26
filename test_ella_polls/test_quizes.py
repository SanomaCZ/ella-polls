# -*- coding: utf-8 -*-
import re
from datetime import datetime, timedelta

from django.test import TestCase

from nose import tools

from test_ella.test_core import create_basic_categories
from test_ella import template_loader

from ella_polls.models import Quiz, Question, Choice, Result

try:
    from django.utils.timezone import now
except ImportError:
    now = datetime.now

QCOUNT = 3
CCOUNT = 2


class QuizTestCase(TestCase):
    def setUp(self):
        super(QuizTestCase, self).setUp()
        now_datetime = now()
        day = timedelta(days=1)
        create_basic_categories(self)

        self.quiz = Quiz.objects.create(
                title='My first quiz',
                slug='my-first-quiz',
                description='some description',
                category=self.category,
                text_announcement='Text with announcement',
                text='Some text',
                active_from=now_datetime - day,
                active_till=now_datetime + day,
                publish_from=now_datetime - day,
                published=True
            )
        self.questions = [
                Question.objects.create(
                    quiz=self.quiz,
                    question='What %d?' % n,
                ) for n in range(QCOUNT)
            ]
        self.choices = []
        for i in range(QCOUNT):
            q = self.questions[i]
            answers = [
                    Choice.objects.create(
                        question=q,
                        choice='Choice %d' % n,
                        points=n,
                    ) for n in range(CCOUNT)
                ]
            self.choices.append(answers)

        self.results = [
                Result.objects.create(
                    quiz=self.quiz,
                    title='You\'ve done good',
                    text='Really, you have!',
                    count=0,
                )
            ]

input_re = re.compile('name="([^"]+)" value="([^"]+)"')

class TestWizard(QuizTestCase):
    def setUp(self):
        super(TestWizard, self).setUp()
        self.url = self.quiz.get_absolute_url()

    def test_step(self):
        template_loader.templates['page/step.html'] = ''
        template_loader.templates['page/result.html'] = ''
        c = self.client
        response = c.get(self.url)

        for x in range(QCOUNT):
            tools.assert_equals(200, response.status_code)
            tools.assert_equals('page/step.html', response.template.name)

            data = {
                response.context['step_field']: response.context['step0'],
            }
            for name, value in input_re.findall(response.context['previous_fields']):
                data[name] = value

            form = response.context['form']
            data[form.add_prefix('choice')] = self.choices[int(response.context['step0'])][0].pk
            response = c.post(self.url, data)

        tools.assert_equals(200, response.status_code)
        tools.assert_equals('page/result.html', response.template.name)
        result = Result.objects.get(pk=self.results[0].pk)
        tools.assert_equals(1, result.count)


