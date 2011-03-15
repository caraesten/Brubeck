# Allow the use of / operator for division to yield floats instead of integers:
# http://docs.python.org/whatsnew/2.2.html#pep-238-changing-the-division-operator
from __future__ import division

# Imports from standard libraries
import Image
import os
import shutil

# Imports from Django
from django.conf import settings

def get_filename_components(file):
    """
    Splits the file's full name into directory, base and extension.
    """
    (file_dir, file_name) = os.path.split(file.path)
    (file_base, file_ext) = os.path.splitext(file_name)
    return {
        'file_dir': file_dir,
        'file_base': file_base,
        'file_ext': file_ext
    }

def get_thumbnail_filename(image, width):
    """
    Returns a modified filename for a thumbnail of a specified width.
    """
    components = get_filename_components(image)
    return os.path.join(components['file_dir'], "".join([components['file_base'], 't', str(width), components['file_ext']]))

def get_legacy_filename(image, type):
    """
    Returns a thumbnail filename in the 2008 site's original format.
    
    type: A string that should be either 't' or 't2'. Will assume 't' if
    provided value makes no sense.
    't' thumbnails are 200 pixels wide.
    't2' thumbnails are 150 pixels high.
    """
    components = get_filename_components(image)
    if type is not 't2':
        type = 't'
    return os.path.join(components['file_dir'], "".join([components['file_base'], type, components['file_ext']]))

def is_vert(image):
    """
    Determines whether this photo is more vertical than a square.
    """
    aspect = image.width / image.height
    if aspect < 1:
        return True
    else:
        return False

def save_thumbnail(image, width=None, height=None, filename=None):
    """
    Resizes an image to a given width or height.
    
    Must specify exactly one dimension (width or height). To specify neither
    or both will raise an exception.
    Saves thumbnail to specified filename.
    """
    old_height = image.height
    old_width = image.width
    original_filename = image.path
    
    if width and height:
        raise StandardError('Specifying both width and height is prohibited')
    if width:
        new_width = width
        new_height = int(old_height * (new_width / old_width))
    elif height:
        new_height = height
        new_width = int(old_width * (new_height / old_height))
    else:
        raise StandardError('Must specify either width or height')
    
    try:
        image = Image.open(original_filename)
        image.thumbnail((new_width, new_height), Image.ANTIALIAS)
        if image.format == 'JPEG':
            image.save(filename)
        else:
            image.save(filename)
    except:
        try:
            os.symlink(original_filename, filename)
        except:
            shutil.copyfile(original_filename, filename)

def save_pdf_thumbnail(pdf, width):
    """
    Saves thumbnail images from the given PDF. Requires pdftoppm, from xpdf:
    http://www.foolabs.com/xpdf/
    """
    try:
        path_to_pdftoppm = settings.PATH_TO_PDFTOPPM
    except:
        path_to_pdftoppm = 'pdftoppm'
    try:
        file_dir = get_filename_components(pdf)['file_dir']
        file_base = get_filename_components(pdf)['file_base']
        os.system('%s -f 1 -l 1 %s %s' % (path_to_pdftoppm, pdf.path, pdf.path.replace('.pdf', '')))
        ppm_path = os.path.join(file_dir, file_base + '-000001.ppm')
        ppm = Image.open(ppm_path)
        old_width = ppm.size[0]
        old_height = ppm.size[1]
        new_width = width
        new_height = int(old_height * (new_width / old_width))
        ppm.thumbnail((new_width, new_height), Image.ANTIALIAS)
        # new_filename = "".join([file_dir, file_base, 't', str(width), '.jpg'])
        new_filename = pdf.path.replace('.pdf', 't' + str(width) + '.jpg')
        ppm.save(new_filename, 'jpeg', quality=85)
        os.remove(ppm_path)
    except:
        pass

def save_legacy_thumbnails(image):
    """
    Saves the two sizes of thumbnail originally created by the 2008 site.
    """
    save_thumbnail(image, width=200, filename=_get_legacy_filename(image, type='t'))
    save_thumbnail(image, height=150, filename=_get_legacy_filename(image, type='t2'))