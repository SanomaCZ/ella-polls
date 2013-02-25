from django.contrib import admin
from django.forms.util import ValidationError
from django.forms.models import BaseInlineFormSet
from django.forms import ModelForm, ValidationError
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, ugettext

from ella.core.admin import ListingInlineAdmin
from ella.core.cache import get_cached_object_or_404

from ella_polls.models import Poll, Contest, Contestant, Quiz, Result, Choice, \
    Vote, Question, Result, Survey


class DateSpanModelForm(ModelForm):
    def clean(self):
        d = super(DateSpanModelForm, self).clean()
        if not self.is_valid():
            return d
        if d['active_from'] and d['active_till'] and d['active_from'] > d['active_till']:
            raise ValidationError(_('Active till must be later than active from.'))
        return d


class ContestForm(DateSpanModelForm):
    class Meta:
        model = Contest


class QuizForm(DateSpanModelForm):
    class Meta:
        model = Quiz


class SurveyForm(DateSpanModelForm):
    class Meta:
        model = Survey


class PollForm(DateSpanModelForm):
    class Meta:
        model = Poll


class ResultForm(ModelForm):
    class Meta:
        model = Result

    def __init__(self, *args, **kwargs):
        super(ResultForm, self).__init__(*args, **kwargs)
        self.fields['count'].required = False

    def clean(self):
        self.cleaned_data = super(ResultForm, self).clean()
        if not self.cleaned_data['count']:
            self.cleaned_data['count'] = u'0'
        if not self.is_valid():
            return
            return self.cleaned_data


class ResultFormset(BaseInlineFormSet):
    def clean(self):
        if not self.is_valid():
            return

        validation_error = None
        for i, d in ((i, d) for i, d in enumerate(self.cleaned_data) if d):
            if d['points_from'] > d['points_to']:
                validation_error = ValidationError(ugettext(
                        'Invalid score interval %(points_from)s - %(points_to)s.'
                        'Points dimension from can not be greater than point dimension to.') % d
                )
                self.forms[i]._errors = {'points_to': validation_error.messages}
        if validation_error:
            raise ValidationError, ugettext('Invalid score intervals')

        intervals = [(form_data['points_from'], form_data['points_to'])
            for form_data in self.cleaned_data if form_data]
        intervals.sort()
        for i in xrange(len(intervals) - 1):
            if intervals[i][1] + 1 > intervals[i + 1][0]:
                raise ValidationError, ugettext('Score %s is covered by two answers.') % (intervals[i][1])
            elif intervals[i][1] + 1 < intervals[i + 1][0]:
                raise ValidationError, ugettext('Score %s is not covered by any answer.') % (intervals[i][1] + 1)
        return self.cleaned_data


class ResultTabularOptions(admin.TabularInline):
    model = Result
    orm = ResultForm
    extra = 5
    formset = ResultFormset


class ChoiceTabularOptions(admin.TabularInline):
    model = Choice
    extra = 5


class QuestionOptions(admin.ModelAdmin):
    """
    Admin options for Question model:
        * edit inline choices
    """
    inlines = (ChoiceTabularOptions,)
    ordering = ('question',)
    search_fields = ('question', 'quiz__title', 'contest__title')
    #list_filter = ('quiz__title', 'contest__title',)
    #rich_text_fields = {'small': ('question',)}


class ChoiceOptions(admin.ModelAdmin):
    """
    Admin options for Choices
    """
    ordering = ('question', 'choice')
    list_display = ('question', 'choice', 'votes', 'points')
    search_fields = ('choice',)


class VoteOptions(admin.ModelAdmin):
    """
    Admin options for votes
    """
    ordering = ('time',)
    list_display = ('time', 'poll', 'user', 'ip_address')


class ContestantOptions(admin.ModelAdmin):
    """
    Admin options for Contestant
    """
    ordering = ('datetime',)
    list_display = ('name', 'surname', 'user', 'datetime', 'contest', 'points', 'winner')



class ContestOptions(admin.ModelAdmin):
    def __call__(self, request, url):
        if url and url.endswith('correct_answers'):
            pk = url.split('/')[-2]
            contest = get_cached_object_or_404(Contest, pk=pk)
            contestants = contest.get_correct_answers()
            title = u"%s '%s': %s" % (Contest._meta.verbose_name, contest.title, _('Correct Answers'))
            module_name = Contestant._meta.module_name
            return render_to_response('admin/polls/answer/correct.html',
                {'contestants' : contestants, 'title' : title, 'module_name' : module_name})
        return super(ContestOptions, self).__call__(request, url)

    form = ContestForm
    list_display = ('title', 'category', 'active_from', 'correct_answers',
        'get_all_answers_count', 'pk', 'get_domain_url',)
    list_filter = ('category', 'active_from',)
    search_fields = ('title', 'text', 'text_results',)
    inlines = [ ListingInlineAdmin ]
    raw_id_fields = ('photo',)
    prepopulated_fields = {'slug' : ('title',)}
    # rich_text_fields = {'small': ('text_announcement', 'text', 'text_results',)}
    #rich_text_fields = {'small': ('description',), None: ('text',)}

    def correct_answers(self, obj):
        """
        Admin's list column with a link to the list of contestants with
        correct answers on the current contest
        """
        return mark_safe(u'<a href="%s/correct_answers/">%s - %s</a>' %
            (obj.id, _('Correct Answers'), obj.title))
    correct_answers.allow_tags = True

    def get_all_answers_count(self, obj):
        return Contestant.objects.filter(contest=obj).count()
    get_all_answers_count.short_description = _('Participants in total')


class QuizOptions(admin.ModelAdmin):
    form = QuizForm
    list_display = ('title', 'category', 'active_from', 'pk', 'get_domain_url',)
    list_filter = ('category', 'active_from',)
    search_fields = ('title', 'desc', 'text', 'text_results',)
    inlines = [ ResultTabularOptions, ListingInlineAdmin ]
    raw_id_fields = ('photo',)
    prepopulated_fields = {'slug' : ('title',)}
    # rich_text_fields = {'small': ('text', 'text_results',)}
    #rich_text_fields = {'small': ('description',), None: ('text',)}
    suggest_fields = {'authors': ('name', 'slug',), }


class PollOptions(admin.ModelAdmin):
    # rich_text_fields = {'small': ('text', 'text_results',)}
    #rich_text_fields = {'small': ('text',)}
    form = PollForm
    list_display = ('title', 'question', 'get_total_votes', 'pk',)
    list_filter = ('active_from',)
    search_fields = ('title', 'text', 'text_results', 'question__question',)
    raw_id_fields = ('question',)


class SurveyChoiceInlineAdmin(admin.TabularInline):
    exclude = ('points', 'votes',)
    model = Choice
    extra = 5


class SurveyOptions(admin.ModelAdmin):
    form = SurveyForm
    exclude = ('quiz', 'contest', 'allow_no_choice', 'allow_multiple')
    list_display = ('__unicode__', 'get_total_votes',)
    list_filter = ('active_from', 'active_till',)
    search_fields = ('question',)
    inlines = [SurveyChoiceInlineAdmin]


admin.site.register(Poll, PollOptions)
admin.site.register(Survey, SurveyOptions)
admin.site.register(Contest, ContestOptions)
admin.site.register(Quiz, QuizOptions)
admin.site.register(Question, QuestionOptions)
admin.site.register(Choice, ChoiceOptions)
admin.site.register(Vote, VoteOptions)
admin.site.register(Contestant, ContestantOptions)
