

def as_widget_dj_compat(bound_field, widget=None, attrs=None, only_initial=False):
        """
        Same as as_widget method of BoundField class from module
        django.forms.forms.py but does not use force_text
        for widget render method. This behavior is same as in django < 1.7
        """
        if not widget:
            widget = bound_field.field.widget

        if bound_field.field.localize:
            widget.is_localized = True

        attrs = attrs or {}
        auto_id = bound_field.auto_id
        if auto_id and 'id' not in attrs and 'id' not in widget.attrs:
            if not only_initial:
                attrs['id'] = auto_id
            else:
                attrs['id'] = bound_field.html_initial_id

        if not only_initial:
            name = bound_field.html_name
        else:
            name = bound_field.html_initial_name
        return widget.render(name, bound_field.value(), attrs=attrs)
