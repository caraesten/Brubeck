# Imports from standard libraries
import random

# Imports from Django
from django import template
from django.contrib.sites.models import Site

# Imports from brubeck
from brubeck.advertising.models import BannerAd

register = template.Library()

@register.simple_tag
def render_adsense(type):
    """
    Renders a Google Adsense block in the same sizes as the BannerAd model.
    """
    if type == 'banner':
        code = """
            <script type="text/javascript"><!--
            google_ad_client = "pub-5361914556213729";
            google_ad_slot = "1625200313";
            google_ad_width = 468;
            google_ad_height = 60;
            //-->
            </script>
            <script type="text/javascript"
            src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
            </script>
        """
    elif type == 'shortvert':
        code = """
            <script type="text/javascript"><!--
            google_ad_client = "pub-5361914556213729";
            google_ad_slot = "8697309618";
            google_ad_width = 120;
            google_ad_height = 240;
            //-->
            </script>
            <script type="text/javascript"
            src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
            </script>
        """
    elif type == 'vertical':
        code = """
            <script type="text/javascript"><!--
            google_ad_client = "pub-5361914556213729";
            google_ad_slot = "9446223050";
            google_ad_width = 120;
            google_ad_height = 600;
            //-->
            </script>
            <script type="text/javascript"
            src="http://pagead2.googlesyndication.com/pagead/show_ads.js">
            </script>
        """
    else:
        return ''
    
    return '<div class="ad ad_%s">%s</div>' % (type, code)

@register.simple_tag
def render_cube_ad():
    """
    Renders a BannerAd instance of the desired size, 'cube'. Defaults to None if
    no such ad exists for a given site.
    """
    site = Site.objects.get_current()
            
    try:
        ads = BannerAd.current.filter(site=site).filter(ad_type='cube').filter(special_section__isnull=True)
        if not ads:
            ad = None
        else:
            ad = random.choice(ads)
    except Advertisement.DoesNotExist:
        ad = None
    if not ad:
        return ''
            
    code = ''
    if not ad.code:
        code = '<img src="%s" alt="%s" />' % (ad.image.url, ad.name)
        if ad.url:   
            code = ''.join(['<a href="%s">' % ad.url, code, '</a>'])
    else:
        code = ad.code
    code = ''.join(['<div class="ad ad_cube">', code, '</div>'])
            
    return code

@register.simple_tag 
def render_eyebrow_ad():
    """
    Renders a BannerAd instance of the desired size, 'eyebrow'. Defaults to None if
    no such ad exists for a given site.
    """
    site = Site.objects.get_current()

    try:
        ads = BannerAd.current.filter(site=site).filter(ad_type='eyebrow').filter(special_section__isnull=True)
        if not ads:
            ad = None
        else:
            ad = random.choice(ads)
    except Advertisement.DoesNotExist:
        ad = None
    if not ad:
        return ''
        
    code = ''
    if not ad.code:
        code = '<img src="%s" alt="%s" />' % (ad.image.url, ad.name)
        if ad.url:
            code = ''.join(['<a href="%s">' % ad.url, code, '</a>'])
    else:
        code = ad.code
    code = ''.join(['<div class="ad ad_eyebrow">', code, '</div>'])
            
    return code

@register.simple_tag
def render_banner_ad(type, fallback='True'):
    """
    Renders a BannerAd instance of the desired size. If fallback is 'True',
    the site will display an AdSense ad if there is no current BannerAd of the 
    specified type.
    """
    site = Site.objects.get_current()
    
    # If we ask for a vertical ad, this means we'll have room for either a
    # vertical ad or a shortvert. Let's mix things up a bit.
    if type == 'vertical':
        type = random.choice(['vertical', 'shortvert'])
    
    if type in ['vertical', 'shortvert', 'banner']:
        try:
            ads = BannerAd.current.filter(site=site).filter(ad_type=type).filter(special_section__isnull=True)
            if not ads:
                ad = None
            else:
                ad = random.choice(ads)
        except Advertisement.DoesNotExist:
            ad = None
        if not ad:
            if fallback == 'True':
                return render_adsense(type)
            else:
                return ''
    
    code = ''
    if not ad.code:
        code = '<img src="%s" alt="%s" />' % (ad.image.url, ad.name)
        if ad.url:
            code = ''.join(['<a href="%s">' % ad.url, code, '</a>'])
    else:
        code = ad.code
    code = ''.join(['<div class="ad ad_%s">' % type, code, '</div>'])
    
    return code

@register.simple_tag
def render_special_banner_ad(type, section_id, fallback='True'):
    """
    Renders a BannerAd instance of the desired size. If fallback is 'True',
    the site will display an AdSense ad if there is no current BannerAd of the
    specified type.
    """
    site = Site.objects.get_current()

    try:
        section_id = int(section_id)
    except:
        section_id = 0

    # If we ask for a vertical ad, this means we'll have room for either a
    # vertical ad or a shortvert. Let's mix things up a bit.
    if type == 'vertical':
        type = random.choice(['vertical', 'shortvert'])
                                                                                     
    if type in ['vertical', 'shortvert', 'banner']:
        try:
            ads = BannerAd.current.filter(site=site).filter(ad_type=type).filter(special_section__id=section_id)
            if not ads:
                ad = None
            else:
                ad = random.choice(ads)
        except Advertisement.DoesNotExist:
            ad = None
        if not ad:
            if fallback == 'True':
                return render_adsense(type)
            else:
                return ''

    code = ''
    if not ad.code:
        code = '<img src="%s" alt="%s" />' % (ad.image.url, ad.name)
        if ad.url:
            code = ''.join(['<a href="%s">' % ad.url, code, '</a>'])
    else:
        code = ad.code
    code = ''.join(['<div class="ad ad_%s">' % type, code, '</div>'])

    return code

@register.simple_tag
def render_ad_by_id(ad_id, fallback='True'):
    """
    Renders the requested BannerAd instance. If fallback is 'True', the site will
    display an AdSense ad if there is no current BannerAd with the specified ID and
    of the specified type.
    """
    try:
        ad_id = int(ad_id)
    except:
	ad_id = 0

    try:
        ad = BannerAd.current.get(id=ad_id)
    except BannerAd.DoesNotExist:
        ad = None

    if not ad:
        ad = None
        if fallback == 'True':
            return render_adsense(type)
        else:
            return ''
    
    code = ''
    if not ad.code:
        code = '<img src="%s" alt="%s" />' % (ad.image.url, ad.name)
        if ad.url:
            code = ''.join(['<a href="%s">' % ad.url, code, '</a>'])
    else:   
        code = ad.code
    code = ''.join(['<div class="ad ad_%s">' % ad.ad_type, code, '</div>'])
                
    return code
