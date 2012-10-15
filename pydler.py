# checkdir.py Copyright (C) 2012 Mark Wingerd
#
# This program comes with ABSOLUTELY NO WARRANTY;
# This is free software, and you are welcome to redistribute it
# under certain conditions; Please see the file LICENSE for detail.
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urlparse
import httplib

import checkdir

def get_file(src, dest, block_size=16384, console_info=False):
    """ Download files and saves them.

    src: File source.
    dest: Destination of the file.
    block_size: Optional. Amount of bytes downloaded at a time. Defaults
                to 16384.
    console_info: Optional. Displays download status to the console.
                  Default is False.
    """
    # Initialize download information.
    src = _getsrcfile(src)
    f = urllib2.urlopen(src)
    f_total = int(f.info().getheaders("Content-Length")[0])
    f_down = 0

    # Initialize local file information.
    out = open(dest, 'wb')

    # Download in block_sizes and output if requested.
    _output(f_down, f_total, console_info=True)
    while f_down < f_total:
        buffer = f.read(block_size)
        f_down += len(buffer)
        out.write(buffer)
        _output(f_down, f_total, console_info=True)
    out.close()



def _output(current, file_size, console_info=False):
    """ Will display downloading information and file status to console.

    current: Current data downloaded.
    total: Total amount of data to be downloaded.
    console_info: Optonal. If true, will display messages to console.
    """
    # Handle initial, progress, and completion messages based on current.
    if console_info:
        if current == 0:
            print "Downloading %s Bytes" % file_size
        if 0 < current < file_size:
            status = r"%10d  [%3.2f%%]" % (current, current * 100. / file_size)
            print status
        if current == file_size:
            print "Download Complete. %s Bytes" % current



def _getsrcfile(src):
    """ Verifies that the source path is valid. """

    # Adds http:// if none exsist in the url.
    urlparts = urlparse.urlparse(src)
    if not urlparts[0]:
        src = 'http://' + src
        urlparts = urlparse.urlparse(src)

    # Check if link has content
    connection = httplib.HTTPConnection(urlparts[1]) 
    connection.request('HEAD', urlparts[2]) 
    response = connection.getresponse() 
    if response.status == 200:
        print "Resource exists: %s" % response.status 
    else:
        print "Resource not found: %s" % response.status

    return src





### This is just to test how the functions work. ###
# Proper use.
get_file('http://www.strangelyeverafter.com/image/mainImage000.jpg', 
         './img001.jpg', console_info=True)
get_file('www.strangelyeverafter.com/img/mainImage001.jpg', 
         './img002.jpg', console_info=True)
get_file('strangelyeverafter.com/image/mainImage002.jpg', 
         './img003.jpg', console_info=True)
# Error in src.
#get_file('image/mainImage000.jpg', './img.jpg', console_info=True)
# Error in dest.
#get_file('http://www.strangelyeverafter.com/image/mainImage000.jpg', 
#         '.notafolder/img.jpg', console_info=True)
# Invalid link.
#get_file('http://www.strangelyeverafter.com/image/mainImage100.jpg', 
#         './img.jpg', console_info=True)