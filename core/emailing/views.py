"""
Provides an assortment of functions to help with general e-mail forms.
There are only two form fields with special meanings, and both are optional:
    'self_email' should always be the sender's own e-mail address.
    'cc_self' is a BooleanField asking whether or not the person wants to be
    sent a copy of the e-mail being generated.
"""

# Imports from standard libraries
import mimetools

# Imports from Django
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import redirect_to_login
# from django.core.mail import send_mail
from django.core.mail import EmailMessage, SMTPConnection
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, loader, RequestContext

# Imports from maneater
from maneater.core.decorators import is_editor
from maneater.emailing.forms import *

def render_email_and_send(context=None, message_template='', subject='', recipients=None, sender=None):
    """
    Sends an e-mail based on the given parameters.
    
    Takes a context (as a dictionary), a template path (as a string), a subject
    (as a string) and recipients (as a list or tuple). E-mail templates SHOULD
    (see RFC 2119 for the meaning of SHOULD) be plain text. (I have no idea
    what will happen if you pass HTML.)
    """
    t = loader.get_template(message_template)
    c = Context(context)
    message = t.render(c)
    
    # Not sure why, but there's a random bug somewhere that causes e-mail
    # socket errors. It's puzzled some other people, but this line seems to
    # more or less fix it:
    # http://mail.python.org/pipermail/python-list/2006-December/420357.html
    mimetools._prefix = 'x'
    
    if not sender:
        sender = settings.SERVER_EMAIL
    
    # send_mail(subject, message, sender, recipients)
    
    connection = SMTPConnection(fail_silently=True)
    email_to_send = EmailMessage(
        subject = subject,
        body = message,
        from_email = sender,
        to = recipients,
        connection = connection
    )
    email_to_send.send(fail_silently=True)
    connection.close()

def handle_form_and_email(request, form=None, form_template='', message_template='', subject='', recipients=None, redirect_to='/thanks/', sender=None, uses_captcha=True, *args, **kwargs):
    """
    Abstracts the rendering and processing of e-mail forms.
    """
    if uses_captcha:
        remote_ip = request.META['REMOTE_ADDR']
    if request.method == 'POST':
        if uses_captcha:
            form = form(remote_ip, request.POST)
        else:
            form = form(request.POST)
        
        if form.is_valid():
            # Handle special field names and possibly set sender address.
            try:
                if form.cleaned_data['cc_self']:
                    recipients.append(form.cleaned_data['self_email'])
                if sender == 'self':
                    sender = form.cleaned_data['self_email']
            except:
                pass
            # Send the e-mail.
            render_email_and_send(message_template=message_template, context=form.cleaned_data, subject=subject, recipients=recipients, sender=sender)
            return HttpResponseRedirect('/thanks/')
    else:
        if uses_captcha:
            form = form(remote_ip)
        else:
            form = form()
    
    page = {
        'form': form
    }
    
    return render_to_response(form_template, page, context_instance=RequestContext(request))

def captcha_form_and_email(request, form=None, form_template='', message_template='', subject='', recipients=None, redirect_to='/thanks/', sender=None, *args, **kwargs):
    """
    Abstracts the rendering and processing of e-mail forms.
    """
    remote_ip = request.META['REMOTE_ADDR']
    if request.method == 'POST':
        form = form(remote_ip, request.POST)
        if form.is_valid():
            # Handle special field names and possibly set sender address.
            try:
                if form.cleaned_data['cc_self']:
                    recipients.append(form.cleaned_data['self_email'])
                if sender == 'self':
                    sender = form.cleaned_data['self_email']
            except:
                pass
            # Send the e-mail.
            render_email_and_send(message_template=message_template, context=form.cleaned_data, subject=subject, recipients=recipients, sender=sender)
            return HttpResponseRedirect('/thanks/')
    else:
        form = form(remote_ip)
    
    page = {
        'form': form
    }
    
    return render_to_response(form_template, page, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def restricted_email(request, form=None, form_template='', message_template='', subject='', recipients=None, redirect_to='/thanks/', uses_captcha=False, editor_required=False):
    """
    Wraps handle_form_and_email() to require users to be staff members (or
    editors, if you'd prefer).
    """
    if is_editor(request.user) or not editor_required:
        return handle_form_and_email(request, form=form, form_template=form_template, message_template=message_template, subject=subject, recipients=recipients, redirect_to=redirect_to, uses_captcha=uses_captcha)
    else:
        # Make the user log in first.
        redirect_to_login(next=request.META['PATH_INFO'])
