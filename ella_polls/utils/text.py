"""
truncate_words function is ported from django 1.5 and was removed in django 1.6
Here is for backward compatibility with django 1.3
"""
try:
    from django.utils.text import truncate_words
except ImportError:
    from django.utils import six
    from django.utils.text import Truncator
    from django.utils.functional import allow_lazy

    def truncate_words(s, num, end_text='...'):
        truncate = end_text and ' %s' % end_text or ''
        return Truncator(s).words(num, truncate=truncate)
    truncate_words = allow_lazy(truncate_words, six.text_type)
