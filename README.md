Website crawling utility
======

Leechi is a robust and sneaky wrapper for urllib2.

It is sneaky because it introduces
random delays between requests
and because it changes its User Agent string.

It is robust because it will automatically retry failed requests.

Additionally, it will handle cookies to make session handling
easier or even automatic.

Leechi development was sponsored by the Forschungsdaten Service Center
of Universität Mannheim, Germany <http://service.informatik.uni-mannheim.de/>.


Usage
======


  In [1]: import leechi
  In [2]: l = leechi.Leechi(cookies=False)
  In [3]: l.fetch("http://www.informatik.uni-mannheim.de/robots.txt")
  Out[3]: 'User-agent: *\nDisallow: /fileadmin/\nDisallow: /uploads/\n\n'
  # sleep a random delay
  In [4]: l.fetchDelayed("http://www.informatik.uni-mannheim.de/robots.txt")
  Out[4]: 'User-agent: *\nDisallow: /fileadmin/\nDisallow: /uploads/\n\n'

  In [5]: import BeautifulSoup
  In [6]: soup = BeautifulSoup.BeautifulSoup(l.obtainHandle("http://www.informatik.uni-mannheim.de/"))

  In [7]: soup.title
  Out[7]: <title>Institut für Informatik und Wirtschaftsinformatik - Fakultät für Wirtschaftsinformatik und Wirtschaftsmathematik</title>

  In [8]: soup = BeautifulSoup.BeautifulSoup(l.obtainHandleDelayed("http://www.informatik.uni-mannheim.de/"))
  In [9]: soup.title
  Out[9]: <title>Institut für Informatik und Wirtschaftsinformatik - Fakultät für Wirtschaftsinformatik und Wirtschaftsmathematik</title>

  In [12]: l.getCurrentUA()
  Out[12]: 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52'
  In [13]: l.chooseRandomUA()
  In [14]: l.getCurrentUA()
  Out[14]: 'Mozilla/5.0 (X11; Linux x86_64; rv:5.0) Gecko/20100101 Firefox/5.0 Firefox/5.0'


