from django import forms

from brubeck.voxpopuli.models import Poll

class PollForm(forms.Form):
    def __init__(self, data=None, poll_id=None, *args, **kwargs):
        forms.Form.__init__(self, data=data, *args, **kwargs)
        
        poll = Poll.objects.get(id=poll_id)
        choices = poll.choice_set.order_by('?')
        
        POLL_CHOICES = []
        
        for choice in choices:
            POLL_CHOICES.append((choice.id, choice.choice))
        
        self.fields['choice'] = forms.ChoiceField(choices=POLL_CHOICES, widget=forms.RadioSelect)
