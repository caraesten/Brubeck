# Imports from Django
from django import forms

# Imports from maneater
from brubeck.core.emailing.recaptcha import RecaptchaFieldPlaceholder, RecaptchaForm, RecaptchaWidget

# class LetterToTheEditorForm(forms.Form):
class LetterToTheEditorForm(RecaptchaForm):
    name = forms.CharField(help_text="Required for us to print your letter.")
    self_email = forms.CharField(label="E-mail address", help_text="Required for us to print your letter.")
    cc_self = forms.BooleanField(label="Send yourself a copy of this e-mail (optional)", required=False)
    phone_number = forms.CharField(required=False)
    body = forms.CharField(widget=forms.Textarea, help_text="Please keep your letter under 200 words, particularly if you'd like for us to print it.")
    captcha = RecaptchaFieldPlaceholder(widget=RecaptchaWidget(theme='white'), label='Spam filter')

class PhotoRequestForm(forms.Form):
# class PhotoRequestForm(RecaptchaForm):
    slug = forms.CharField()
    writer_name = forms.CharField(required=False)
    writer_phone = forms.CharField(required=False)
    writer_email = forms.EmailField(required=False)
    editor_name = forms.CharField()
    event = forms.CharField()
    event_when = forms.CharField(label="Event date/time", required=False)
    event_location = forms.CharField(required=False)
    deadline = forms.CharField(required=False)
    comments = forms.CharField(label="Additional comments/requests/warnings", widget=forms.Textarea, required=False)
    # captcha = RecaptchaFieldPlaceholder(widget=RecaptchaWidget(theme='white'), label='Spam filter')

# class SubmissionForm(forms.Form):
class SubmissionForm(RecaptchaForm):
    name = forms.CharField()
    self_email = forms.EmailField(label="E-mail address")
    about = forms.CharField(label="Tell us about yourself (optional)", widget=forms.Textarea, required=False)
    cc_self = forms.BooleanField(label="Send yourself a copy of this e-mail (optional)", required=False)
    submission = forms.CharField(label="What's on your mind?", widget=forms.Textarea)
    captcha = RecaptchaFieldPlaceholder(widget=RecaptchaWidget(theme='white'), label='Spam filter')

class SystemTestForm(RecaptchaForm):
    name = forms.CharField()
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'wide'}))
    website = forms.URLField(widget=forms.TextInput(attrs={'class': 'wide'}), label='Web site (optional)', required=False)
    captcha = RecaptchaFieldPlaceholder(widget=RecaptchaWidget(theme='white'), label='Are you a human?')

class WorkForUsForm(RecaptchaForm):

    INTEREST_CHOICES = (
    ('News', 'News'), # traviscornejo@gmail.com, kaylen.ralph@gmail.com, steve.dickherber@gmail.com aliciastice@gmail.com
    ('Arts', 'Arts'), # asussell@gmail.com
    ('Sports', 'Sports'), # zachmink12@gmail.com
    ('Opinion', 'Opinion'), # ryanschuessler@gmail.com
    ('MOVE Magazine', 'MOVE Magazine'), # ecwg33@mail.mizzou.edu
    ('Photography', 'Photography'), # agro.nicholas@gmail.com
    ('Design', 'Design'), # esdundon@gmail.com
    ('Broadcast/Multimedia', 'Broadcast/Multimedia'), # nataliexcheng@gmail.com
    ('Web Development', 'Web Development'), # aimeeml@gmail.com
    ('Marketing/Promotions', 'Marketing/Promotions'), # piercecourchaine@gmail.com
    ('Strategic Communications/Advertising', 'Strategic Communications/Advertising'), # molly.paskal@gmail.com

    )   
    name = forms.CharField()
    class_title = forms.CharField(max_length=100)
    self_email = forms.EmailField(label="E-mail address")
    area_of_interest = forms.ChoiceField(choices=INTEREST_CHOICES, label="Select your area of interest.")
    previous_experience = forms.CharField(widget=forms.Textarea, required=False, help_text="Optional: List previous journalism experience.")
    cc_self = forms.BooleanField(label="Send yourself a copy of this e-mail (optional)", required=False)
    captcha = RecaptchaFieldPlaceholder(widget=RecaptchaWidget(theme='white'), label='Are you a human?')

class ContentEmailForm(forms.Form):
    """
    Shows a form with which users can e-mail links to our content.
    """
    sender_name = forms.CharField(required=False, label="Your name (optional)")
    sender_email = forms.EmailField(label="Your e-mail address")
    recipient_name = forms.CharField(required=False, label="Recipient's name (optional)")
    recipient_email = forms.EmailField(label="Recipient's e-mail address")
    note = forms.CharField(required=False, widget=forms.Textarea, label="Add a note (optional)")
    content_type = forms.CharField(widget=forms.HiddenInput, label="Type of content to send")
    content_id = forms.CharField(widget=forms.HiddenInput, label="ID of content to send")

