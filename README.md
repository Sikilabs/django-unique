django-unique
=============

generate unique urls associated to a user each unique url is linked to an object and a user. 
The url usage can be tracked by clicks number. Each url has an expiration date.

Thanks to Net Batchelder : http://stackoverflow.com/a/1360222

This become very handy when your models are actual files and you want to make them available for download
with a minimal level of security.

A few parameters are needed:
-  settings.py:

    `UNIQUE_URL_OBJECT` : the model class that the urls will correspond to

    `UNIQUE_EXP_DATE` : the urls expiration date
    
    `UNIQUE_MAX_CLICS` : the max clics allowed per url

-  templates:

     unique/download_error.html : the download error page