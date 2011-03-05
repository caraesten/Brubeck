import datetime
from haystack import indexes
from haystack.sites import site
from brubeck.events.models import Calendar, Event

class CalendarIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
#    name = indexes.CharField(model_attr='name')

    rendered = indexes.CharField(use_template=True, indexed=False,)

#    def prepare(self, object):
#        self.prepared_data = super(CalendarIndex, self).prepare(object)
#        return self.prepared_data

    def get_updated_field(self):
        return 'last_updated'

#    def get_queryset(self):
#        return Calendar.objects.all()

site.register (Calendar, CalendarIndex)

class EventIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
#    name = indexes.CharField(model_attr='name')
#    summary = indexes.CharField(model_attr='summary')
#    description = indexes.CharField(model_attr='description')
    start = indexes.DateTimeField(model_attr='start')
    end = indexes.DateTimeField(model_attr='start', null=True)
#    location = indexes.CharField(model_attr='location')

    rendered = indexes.CharField(use_template=True, indexed=False,)

#    def prepare(self, object):
#        self.prepared_data = super(EventIndex, self).prepare(object)
#        return self.prepared_data

    def get_updated_field(self):
        return 'last_updated'

#    def get_queryset(self):
#        return Event.objects.all()

site.register (Event, EventIndex)
