# Imports from Django
from django.db import models

# Imports from brubeck
from brubeck.blogs.widgets import ColorPickerWidget

class ColorField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorPickerWidget
        return super(ColorField, self).formfield(**kwargs)
        
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^brubeck\.blogs\.fields\.ColorField"])