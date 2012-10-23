#!/usr/bin/python2
# -*- coding: utf-8 -*-

import urllib,urllib2
import cookielib
import random
import time
import logging

logger = logging.getLogger(__name__)


UAs = []
UAs.append("Mozilla/5.0 (Windows; U; WinNT; de; rv:1.0.2) Gecko/20030311 Beonex/0.8.2-stable")
UAs.append("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0")
UAs.append("Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 Firefox/5.0")
UAs.append("Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6;de-De; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9")
UAs.append("Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)")
UAs.append("Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; de-DE)")
UAs.append("Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; SLCC1; .NET CLR 1.1.4322)")
UAs.append("Opera/9.80 (Windows NT 6.1; U; de-DE) Presto/2.9.181 Version/12.00")
UAs.append("Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52")
UAs.append("Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-DE) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1")
UAs.append("Mozilla/5.0 (Windows; U; Windows NT 6.1; de-DE) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27")
UAs.append("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/18.6.872.0 Safari/535.2 UNTRUSTED/1.0 3gpp-gba UNTRUSTED/1.0")
UAs.append("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11")


DELAY=3
MINDELAY=1

# You can either call fetch() or use the opener member
# calling opener.open(url) will return a file-like object,
# which can be passed to the BeautifulSoup ctor
# This is useful as simply calling read()
# on the file descriptor ourselves does not guarantee
# we get the entire content..
#

"""
The Leechi is a tasty little download helper to fetch websites
which do not want to be crawled.
It can change its UA and features random delays between fetches.
It can also handle session cookies which are required
by some sites.
""" 
class Leechi(object):

  # retry: if an error occurs during network operations, e.g. fetch() and fetchDelayed(),
  # the operation will be tried again. For both fetch() and fetchDelayed(),
  # the module will sleep a bit before retrying
  def __init__(self, cookies=True, retry=3):
    # pick user agent string. will persist for the lifetime of the object
    self.useCookies = cookies
    self._tries = retry + 1
    self.chooseRandomUA()

  """
  Choose a different, random User Agent string from the list of UA strings.
  Typically, a single random UA is chosen at object creation time automatically.
  If a different UA string is desired without having to re-create the object,
  call this method.
  """
  def chooseRandomUA(self):
    self.ua = random.choice(UAs)
    # re-create opener to propagate the new UA string
    self._createOpener()

  """
  Sets customs User Agent string.
  """
  def setCustomUA(self, UA):
    self.ua = UA
    self._createOpener()

  def getCurrentUA(self):
    return self.ua

  def fetch(self, URL):
    # I was under the impression that read() may not always return the entire
    # content of the file-like object.
    # Consulting the documentation, it turns out that this is only the case
    # in "non-blocking mode". So let's hope this file-like object is in
    # blocking mode..
    handle = self.obtainHandle(URL)
    return Leechi._handleError(lambda: handle.read(), tries=self._tries, msg="Fetching URL %s" % URL)
    
  
  """
  Fetch content of URL after waiting for a random amount of time.
  The delay will be between 0 and 3 seconds by default.
  The upper and lower bounds are configurable.
  """
  # TODO: make delay and mindelay configurable via ctor?
  def fetchDelayed(self, URL, delay=DELAY, mindelay=MINDELAY):
    Leechi._sleep()
    return self.fetch(URL)

  # Do not use the opener member. Use this method to obtain a file handle for you
  # If you absolutely must use the opener member,
  # please be aware that changing the UA will create a new opener object.
  # TODO: is the empty string equivalent to not passing params
  """
  Returns file-like object.
  """
  def obtainHandle(self, URL, params=""):
    logger.debug("URL is: %s",  URL)
    logger.debug("params is: %s", params)
    return Leechi._handleError(lambda: self.opener.open(URL, params), tries=self._tries, msg="Obtaining handle for URL %s" % URL)

  """
  Returns file-like object after sleeping for a while.
  """
  # similar to fetchDelayed(), this will block so you don't have to
  def obtainHandleDelayed(self, URL, delay=DELAY, mindelay=MINDELAY, params=""):
    Leechi._sleep(delay, mindelay)
    return self.obtainHandle(URL, params)

  def _createOpener(self):
    # TODO: do we want to lose the cookies when re-creating the opener with a different UA?
    if self.useCookies:
      # use LWPCookieJar to persist cookies to disk
      cookieJar = cookielib.LWPCookieJar("/tmp/nomnomnom")
      self.cookieJar = cookieJar
      processor = urllib2.HTTPCookieProcessor(cookieJar)
      opener = urllib2.build_opener(processor)
    else:
      # fall back to default python configuration
      opener = urllib2.build_opener()
    # Accept */* is needed for gh
    opener.addheaders = [("User-Agent", self.ua), ("Accept", "*/*")]
    self.opener = opener

  @staticmethod
  def _sleep(delay=DELAY, mindelay=MINDELAY):
    time.sleep(random.uniform(mindelay, delay))

  @staticmethod
  def _handleError(function, tries, msg="Unspecified"):
    for trial in xrange(tries):
      try:
        return function()
      except urllib2.URLError,e:
        exception=e
        Leechi._sleep()
        logger.info("Caught exception, try %s/%s. Action was: %s" % (trial,tries, msg))
        logger.exception(e)
        # for some reason, any exception in the following block gets logged
        #try:
        #  logger.info("Got HTTP status code: %s", exception.code)
        #  logger.info("Exception.reason: %s", exception.reason)
        #except:
        #  pass
    # propagate
    raise exception

