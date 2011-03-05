# Imports from Django
from django import forms

# Imports from brubeck
from brubeck.emailing.recaptcha import RecaptchaFieldPlaceholder, RecaptchaForm, RecaptchaWidget

class RequestForm(RecaptchaForm):
# class RequestForm(forms.Form):
    """
    Allows potential advertisers to submit their contact information to the
    business staff.
    """
    mail_media_kit = forms.BooleanField(required=False, label="Mail me a printed copy of the rate card with a media kit")
    mail_sample_copy = forms.BooleanField(required=False, label="Mail me a sample copy of The brubeck")
    company_name = forms.CharField()
    contact_name = forms.CharField(label="Your name")
    phone_number = forms.CharField()
    address = forms.CharField(widget=forms.Textarea)
    comments = forms.CharField(required=False, label="Additional comments?", widget=forms.Textarea)
    captcha = RecaptchaFieldPlaceholder(widget=RecaptchaWidget(theme='white'), label='Spam filter')

