#!/usr/bin/python

#
# 02/2006 Will Holcomb <wholcomb@gmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# 03/24/14 Always force multipart even if no files are submitted
#          and respect field order (use collections.OrderedDict
#          for this)
# 7/26/07 Slightly modified by Brian Schneider
# in order to support unicode files ( multipart_encode function )
"""
Usage:
  Enables the use of multipart/form-data for posting forms

Inspirations:
  Upload files in python:
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/146306
  urllib2_file:
    Fabien Seisen: <fabien@seisen.org>

Example:
  import MultipartPostHandler, urllib2, cookielib

  cookies = cookielib.CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies),
                                MultipartPostHandler.MultipartPostHandler)
  params = { "username" : "bob", "password" : "riviera",
             "file" : open("filename", "rb") }
  opener.open("http://wwww.bobsite.com/upload/", params)

Further Example:
  The main function of this file is a sample which downloads a page and
  then uploads it to the W3C validator.
"""

import urllib2
import mimetools
import mimetypes
import os
from cStringIO import StringIO
import logging

logger = logging.getLogger(__name__)


class Callable:

    def __init__(self, anycallable):
        self.__call__ = anycallable

# Controls how sequences are uncoded.
# If true, elements may be given multiple values by
# assigning a sequence.
doseq = 1


class MultipartPostHandler(urllib2.BaseHandler):
    handler_order = urllib2.HTTPHandler.handler_order - \
        10  # needs to run first

    def http_request(self, request):
        data = request.get_data()
        if data is not None and type(data) != str:
            boundary, data = self.multipart_encode(data)
            contenttype = 'multipart/form-data; boundary=%s' % boundary
            if request.has_header('Content-Type'):
                ct_header = request.get_header('Content-Type')
                if ct_header.find('multipart/form-data') != 0:
                    logger.warn("Replacing %s with %s",
                                request.get_header('content-type'),
                                'multipart/form-data')
            request.add_unredirected_header('Content-Type',
                                            contenttype)
            request.add_data(data)
        return request

    def multipart_encode(data):
        boundary = mimetools.choose_boundary()
        buf = StringIO()
        for(key, value) in data.iteritems():
            if isinstance(value, file):
                filename = value.name.split('/')[-1]
                contenttype = mimetypes.guess_type(
                    filename)[0] or 'text/plain' #'application/octet-stream'
                buf.write('--%s\r\n' % boundary)
                # note the trailing space here!
                buf.write('Content-Disposition: form-data; ')
                buf.write('name="%s"; filename="%s"\r\n' % (key, filename))
                buf.write('Content-Type: %s\r\n' % contenttype)
                value.seek(0)
                buf.write('\r\n' + value.read() + '\r\n')
            else:
                buf.write('--%s\r\n' % boundary)
                # note the trailing space here!
                buf.write('Content-Disposition: form-data; ')
                buf.write('name="%s"' % key)
                buf.write('\r\n\r\n' + value + '\r\n')
        buf.write('--' + boundary + '--\r\n\r\n')
        buf = buf.getvalue()
        return boundary, buf
    multipart_encode = Callable(multipart_encode)

    https_request = http_request


def main():
    import tempfile
    import sys

    validatorURL = "http://validator.w3.org/check"
    opener = urllib2.build_opener(MultipartPostHandler)

    def validateFile(url):
        temp = tempfile.mkstemp(suffix=".html")
        os.write(temp[0], opener.open(url).read())
        fh = open(temp[1], "rb")
        params = {"ss": "0",
                  "doctype": "Inline",
                  "uploaded_file": fh}
        print opener.open(validatorURL, params).read()
        fh.close()
        os.remove(temp[1])

    if len(sys.argv[1:]) > 0:
        for arg in sys.argv[1:]:
            validateFile(arg)
    else:
        validateFile("http://www.google.com")

if __name__ == "__main__":
    main()
