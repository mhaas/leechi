#!/usr/bin/env python
# -*- coding: utf-8-*-

from distutils.core import setup

setup(name='Leechi',
      version='0.2',
      description='Website crawler utility',
      author='Michael Haas',
      author_email='haas@computerlinguist.org',
      url='https://github.com/mhaas/leechi',
      py_modules=['leechi'],
      classifiers = [ 'Development Status :: 4 - Beta',
                      'Intended Audience :: Developers',
                      'License :: OSI Approved :: GNU General Public License (GPL)',
                      'Operating System :: OS Independent',
                      'Programming Language :: Python :: 2',
                      'Topic :: Internet :: WWW/HTTP',
                      'Topic :: Software Development :: Libraries'
                    ],
      long_description = """\
Website crawling utility
----------------------------

Leechi is a robust and sneaky wrapper for urllib2.

It is sneaky because it introduces
random delays between requests
and because it changes its User Agent string.

It is robust because it will automatically retry failed requests.

Additionally, it will handle cookies to make session handling
easier or even automatic.

See website for usage information.

Leechi development was sponsored by the Forschungsdaten Service Center
of Universität Mannheim, Germany <http://service.informatik.uni-mannheim.de/>.
"""
     )
