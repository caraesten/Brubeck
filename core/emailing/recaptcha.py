# CREDIT: http://smileychris.tactful.co.nz/ramblings/recaptcha/

from django.forms import *
from django.conf import settings
import httplib, urllib

class RecaptchaWidget(Widget):
    def __init__(self, theme=None, tabindex=None):
        '''
	From http://recaptcha.net/apidocs/captcha/#look-n-feel:

        theme:      'red' | 'white' | 'blackglass'

            Defines which theme to use for reCAPTCHA.

        tabindex:   any integer

            Sets a tabindex for the reCAPTCHA text box. If other elements in
            the form use a tabindex, this should be set so that navigation is
            easier for the user.
        '''
	options = {}
        if theme:
            options['theme'] = theme
        if tabindex:
            options['tabindex'] = tabindex
        self.options = options
        super(RecaptchaWidget, self).__init__()

    def render(self, name, value, attrs=None):
        args = dict(public_key=settings.RECAPTCHA_PUBLIC_KEY)
        if self.options:
            args['options'] = '''<script type="text/javascript">
   var RecaptchaOptions = %r;
</script>
''' % self.options
        return '''%(options)s<script type="text/javascript"
   src="http://api.recaptcha.net/challenge?k=%(public_key)s">
</script>

<noscript>
   <iframe src="http://api.recaptcha.net/noscript?k=%(public_key)s"
       height="300" width="500" frameborder="0"></iframe><br>  
   <textarea name="recaptcha_challenge_field" rows="3" cols="40">
   </textarea>
   <input type="hidden" name="recaptcha_response_field"
       value="manual_challenge">
</noscript>''' % args
        
    def value_from_datadict(self, data, files, name):
        challenge = data.get('recaptcha_challenge_field')
        response = data.get('recaptcha_response_field')
        return (challenge, response)

    def id_for_label(self, id_):
        return None


class RecaptchaField(Field):
    widget = RecaptchaWidget

    def __init__(self, remote_ip, *args, **kwargs):
        self.remote_ip = remote_ip
        super(RecaptchaField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(RecaptchaField, self).clean(value)
        challenge, response = value
        if not challenge:
            raise ValidationError(u'An error occured with the CAPTCHA service. Please try again.')
        if not response:
            raise ValidationError(u'Please enter the CAPTCHA solution.')
        value = validate_recaptcha(self.remote_ip, challenge, response)
        if not value.get('result'):
            raise ValidationError(u'An incorrect CAPTCHA solution was entered.')
        return value
   
   
class RecaptchaFieldPlaceholder(Field):
    '''
    Placeholder field for use with RecaptchaBaseForm which gets replaced with
    RecaptchaField (which is passed the remote_ip) when RecaptchaBaseForm is
    initialised.
    '''
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
    
        
class RecaptchaBaseForm(BaseForm):
    def __init__(self, remote_ip, *args, **kwargs):
        for key, field in self.base_fields.items():
            if isinstance(field, RecaptchaFieldPlaceholder): 
                self.base_fields[key] = RecaptchaField(remote_ip, *field.args, **field.kwargs)
        super(RecaptchaBaseForm, self).__init__(*args, **kwargs)
        
        
class RecaptchaForm(RecaptchaBaseForm, Form):
    pass


def validate_recaptcha(remote_ip, challenge, response):
    # Request validation from recaptcha.net
    if challenge:
        params = urllib.urlencode(dict(privatekey=settings.RECAPTCHA_PRIVATE_KEY,
                                       remoteip=remote_ip,
                                       challenge=challenge,
                                       response=response))
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection("api-verify.recaptcha.net")
        conn.request("POST", "/verify", params, headers)
        response = conn.getresponse()  
        if response.status == 200:
            data = response.read()
        else:
            data = ''
        conn.close()
    # Validate based on response data   
    result = data.startswith('true')
    error_code = ''
    if not result:
        bits = data.split('\n', 2)
        if len(bits) > 1:
            error_code = bits[1]
    # Return dictionary
    return dict(result=result,
                error_code=error_code)
