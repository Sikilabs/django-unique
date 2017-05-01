__author__ = 'ibrahim (at) sikilabs (dot) com'
__licence__ = 'MIT'

from django.shortcuts import RequestContext
from django.template import loader
from django.http import HttpResponse
from django.conf import settings
import datetime
import os

from main.unique.models import UniqueUrl

# import unique url object
modlist = settings.UNIQUE_URL_OBJECT.split(".")
_module = ".".join(modlist[:len(modlist) - 1])
_class = modlist[-1]
module_to_import_from = __import__(_module, fromlist=[_class])
class_to_import = getattr(module_to_import_from, _class)


def get_file(request, unique_url):
    """
    get file or redirect to error page
    """

    my_unique = UniqueUrl.objects.get(url=unique_url)
    if my_unique.clics < settings.UNIQUE_MAX_CLICS:
        if datetime.date.today() < my_unique.expiration_date:
            my_object_id = my_unique.decode_url(my_unique.url_hash,
                my_unique.url)[2]
            my_object = class_to_import.objects.get(id=my_object_id)
            myfile = open(settings.MEDIA_ROOT + my_object.path, 'r')
            fname, extension = os.path.splitext(my_object.path)
            response = HttpResponse(myfile,
                content_type='application/' + extension)
            response['Content-Disposition'] = "attachment; filename=" + my_object.original_filename
            my_unique.clics += 1
            my_unique.save()
            return response
        else:
            t = loader.get_template('unique/download_error.html')
            c = RequestContext(request, {'status': 1})  # expiration passed
            return HttpResponse(t.render(c))
    else:
        t = loader.get_template('unique/download_error.html')
        c = RequestContext(request, {'status': 2})  # max download reached
        return HttpResponse(t.render(c))


def generate_url(request, object_id):
    """
    generate unique url from object id
    """

    unique_object = class_to_import.objects.get(id=object_id)
    try:
        my_unique = UniqueUrl.objects.get(user=request.user,
            ref_object=unique_object)
    except UniqueUrl.DoesNotExist:
        my_unique = UniqueUrl.objects.create(user=request.user,
            expiration_date=settings.UNIQUE_EXP_DATE,
            ref_object=unique_object, clics=0)
        my_unique.encode_url()
