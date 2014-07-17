from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from django.conf import settings

import datetime
import re

from django.forms.widgets import Widget, Select
from django.utils.dates import MONTHS
from django.utils.safestring import mark_safe

class ForeignKeySearchInput(forms.HiddenInput):
    """
    A Widget for displaying ForeignKeys in an autocomplete search input 
    instead in a ``select`` box.
    """
    class Media:
        css = {
            'all': ('/media/css/jquery.autocomplete.css',)
        }
        js = (
            settings.STATIC_URL + 'js/lib/jquery.js',
            settings.STATIC_URL + 'js/lib/jquery.bgiframe.min.js',
            settings.STATIC_URL + 'js/lib/jquery.ajaxQueue.js',
            settings.STATIC_URL + 'js/jquery.autocomplete.js'
        )

    def label_for_value(self, value):
        key = self.rel.get_related_field().name
        obj = self.rel.to._default_manager.get(**{key: value})
        return Truncator(obj).words(14)

    def __init__(self, rel, search_fields, attrs=None):
        self.rel = rel
        self.search_fields = search_fields
        super(ForeignKeySearchInput, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        rendered = super(ForeignKeySearchInput, self).render(name, value, attrs)
        if value:
            label = self.label_for_value(value)
        else:
            label = u''
        return rendered + mark_safe(u'''
            <style type="text/css" media="screen">
                #lookup_%(name)s {
                    padding-right:16px;
                    background: url(
                        %(admin_media_prefix)simg/admin/selector-search.gif
                    ) no-repeat right;
                }
                #del_%(name)s {
                    display: none;
                }
            </style>
<input type="text" id="lookup_%(name)s" value="%(label)s" />
<a href="#" id="del_%(name)s">
<img src="%(admin_media_prefix)simg/admin/icon_deletelink.gif" />
</a>
<script type="text/javascript">
            if ($('#lookup_%(name)s').val()) {
                $('#del_%(name)s').show()
            }
            $('#lookup_%(name)s').autocomplete('../search/', {
                extraParams: {
                    search_fields: '%(search_fields)s',
                    app_label: '%(app_label)s',
                    model_name: '%(model_name)s',
                },
            }).result(function(event, data, formatted) {
                if (data) {
                    $('#id_%(name)s').val(data[1]);
                    $('#del_%(name)s').show();
		    filter();
                }
            });
            $('#del_%(name)s').click(function(ele, event) {
                $('#id_%(name)s').val('');
                $('#del_%(name)s').hide();
                $('#lookup_%(name)s').val('');
            });
            </script>
        ''') % {
            'search_fields': ','.join(self.search_fields),
            'admin_media_prefix': settings.STATIC_URL,
            'model_name': self.rel.to._meta.module_name,
            'app_label': self.rel.to._meta.app_label,
            'label': label,
            'name': name,
        }

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')

class MonthYearWidget(Widget):
    """
    A Widget that splits date input into two <select> boxes for month and year,
    with 'day' defaulting to the first of the month.
    
    Based on SelectDateWidget, in 
    
    django/trunk/django/forms/extras/widgets.py
    
    
    """
    none_value = (0, '---')
    month_field = '%s_month'
    year_field = '%s_year'

    def __init__(self, attrs=None, years=None, required=True):
        # years is an optional list/tuple of years to use in the "year" select box.
        self.attrs = attrs or {}
        self.required = required
        if years:
            self.years = years
        else:
            this_year = datetime.date.today().year
            self.years = range(this_year - 2, this_year+2)

    def render(self, name, value, attrs=None):
        try:
            year_val, month_val = value.year, value.month
        except AttributeError:
            year_val = month_val = None
            if isinstance(value, basestring):
                match = RE_DATE.match(value)
                if match:
                    year_val, month_val, day_val = [int(v) for v in match.groups()]

        output = []

        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name

        month_choices = MONTHS.items()
        if not (self.required and value):
            month_choices.append(self.none_value)
        month_choices.sort()
        local_attrs = self.build_attrs(id=self.month_field % id_)
        s = Select(choices=month_choices)
        select_html = s.render(self.month_field % name, month_val, local_attrs)
        output.append(select_html)

        year_choices = [(i, i) for i in self.years]
        if not (self.required and value):
            year_choices.insert(0, self.none_value)
        local_attrs['id'] = self.year_field % id_
        s = Select(choices=year_choices)
        select_html = s.render(self.year_field % name, year_val, local_attrs)
        output.append(select_html)

        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        return '%s_month' % id_
    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        if y == m == "0":
            return None
        if y and m:
            return '%s-%s-%s' % (y, m, 1)
        return data.get(name, None)