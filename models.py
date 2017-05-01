__author__ = 'ibrahim (at) sikilabs (dot) com'
__licence__ = 'MIT'

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import hashlib
import zlib
import urllib
import cPickle as pickle

# import unique url object
modlist = settings.UNIQUE_URL_OBJECT.split(".")
_module = ".".join(modlist[:len(modlist) - 1])
_class = modlist[-1]
module_to_import_from = __import__(_module, fromlist=[_class])
class_to_import = getattr(module_to_import_from, _class)


class UniqueUrl(models.Model):
    """
    class to describe a temporary unique download url per user
    please use the set_url function to create an instance
    """

    url = models.CharField(max_length=1000)
    user = models.ForeignKey(User)
    expiration_date = models.DateField()
    ref_object = models.ForeignKey(class_to_import)
    url_hash = models.CharField(max_length=200)
    clics = models.IntegerField()

    def encode_url(self):
        """
        Turn `data` into a hash and an encoded string, suitable for use
        with `decode_data`.
        data = [user, exp_date, ref_obj, file_name]
        """

        data = [str(self.user.username),
                str(self.expiration_date),
                str(self.ref_object.id)]
        my_url = zlib.compress(pickle.dumps(data,
            0)).encode('base64').replace('\n', '')
        my_hash = hashlib.md5(settings.UNIQUE_HASH_CODE +
            my_url).hexdigest()[:12]
        self.url = my_url
        self.url_hash = my_hash
        self.save()
        return my_hash, my_url

    def decode_url(self, my_hash, url):
        """
        The inverse of 'encode_url'
        """

        my_url = urllib.unquote(url)
        m = hashlib.md5(settings.UNIQUE_HASH_CODE + my_url).hexdigest()[:12]
        if m != my_hash:
            raise Exception("Wrong hash, please try again!")
        data = pickle.loads(zlib.decompress(my_url.decode('base64')))
        return data
