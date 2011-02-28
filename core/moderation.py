# Akismet spam filtering: http://sciyoshi.com/blog/2009/jul/17/prevent-django-newcomments-spam-akismet-reloaded/

from django.contrib.comments.moderation import CommentModerator, moderator, AlreadyModerated
from django.contrib.sites.models import Site
from django.conf import settings

class AkismetModerator(CommentModerator):
    email_notification = True
    
    def check_spam(self, request, comment, key, blog_url=None, base_url=None):
        try:
            from akismet import Akismet
        except:
            return False
        
        if blog_url is None:
            blog_url = 'http://%s/' % Site.objects.get_current().domain
        
        ak = Akismet(key=key, blog_url=blog_url)
        
        if base_url is not None:
            ak.baseurl = base_url
        
        if ak.verify_key():
            data = {
                'user_ip': request.META.get('HTTP_X_FORWARDED_FOR', '127.0.0.1'),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'referrer': request.META.get('HTTP_REFERER', ''),
                'comment_type': 'comment',
                'comment_author': comment.user_name.encode('utf-8')
            }
            
            if ak.comment_check(comment.comment.encode('utf-8'), data=data, build_data=True):
                return True
        
        return False
    
    def allow(self, comment, content_object, request):
        allow = super(AkismetModerator, self).allow(comment, content_object, request)
        spam = self.check_spam(request, comment, key=settings.AKISMET_API_KEY)
        
        return not spam and allow
        
# try:
#     moderator.register(Entry, EntryModerator)
# except AlreadyModerated:
#     moderator.unregister(Entry)
#     moderator.register(Entry, EntryModerator)