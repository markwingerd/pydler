# checkdir.py Copyright (C) 2012 Mark Wingerd
#
# This program comes with ABSOLUTELY NO WARRANTY;
# This is free software, and you are welcome to redistribute it
# under certain conditions; Please see the file LICENSE for detail.
#
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import urlparse, httplib
import sys, os

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
    try: 
        f = _getsrcfile(src)
    except: 
        print 'ERROR: Source file is inaccessable.'
        return 'ERROR: Source file is inaccessable.'
    f_total = int(f.info().getheaders("Content-Length")[0])
    f_down = 0

    # Initialize local file information.
    try:
        dest = _verifydest(dest)
    except:
        print 'ERROR: No filename provided or other misc error.'
        return 'ERROR: No filename provided or other misc error.'
    out = open(dest, 'wb')

    # Download in block_sizes and output if requested.
    _output(f_down, f_total, console_info=True)
    while f_down < f_total:
        buffer = f.read(block_size)
        f_down += len(buffer)
        out.write(buffer)
        _output(f_down, f_total, console_info=True)
    out.close()

    return



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
    """ Checks if a URL is valid and returns a urllib2 to the URL.
    src: URL of the file needed to be downloaded.
    returns: A urllib2 link to the src. """

    # Adds http:// if none exsist in the url.
    urlparts = urlparse.urlparse(src)
    if not urlparts[0]:
        src = 'http://' + src
        urlparts = urlparse.urlparse(src)

    # Check if link has content
    connection = httplib.HTTPConnection(urlparts[1]) 
    connection.request('HEAD', urlparts[2]) 
    response = connection.getresponse() 
    if response.status != 200:
        raise

    # Get the source file and return it.
    return urllib2.urlopen(src)

def _verifydest(dest):
    """ Uses the checkdir library to verify that the dest is valid
        and create any additional directories needed. 
    dest: A string containing a path and filename for our file.
    returns: dest variable which may have changes.
    """

    # Verify the path and filename is valid.
    if 'linux' in sys.platform: 
        dest = checkdir.validate_string_unix(dest)
    else:
        raise 'OS not supported'

    # Splits the path into a path and filename. Tests if there is a filename
    splitPath = os.path.split(dest)
    if splitPath[1] == '': 
        raise 'No file name provided'

    # Check if there is a path and it exists. Create if it does not.
    if splitPath[0] and (not os.path.exists(splitPath[0])):
        os.makedirs(splitPath[0])

    return dest


def test():
    ### This is just to test how the functions work. ###
    # Proper use.
    """
    get_file('http://www.strangelyeverafter.com/image/mainImage000.jpg', 
             './img001.jpg', console_info=True)
    get_file('www.strangelyeverafter.com/image/mainImage001.jpg', 
             './img002.jpg', console_info=True)
    get_file('strangelyeverafter.com/image/mainImage002.jpg', 
             './img003.jpg', console_info=True)
    get_file('http://www.strangelyeverafter.com/image/mainImage003.jpg', 
             'img.jpg', console_info=True)
    # Additional feature could include the lack of a dest variable. The program
    # would take the filename from the source and apply it to the dest variable.
    """
    # Error in src.
    print 'The following will fail.'
    get_file('image/mainImage000.jpg', './img.jpg', console_info=True) #Raises Error
    get_file('http://www.strangelyeverafter.com/img/mainImage000.jpg', 
            './img001.jpg', console_info=True) #Raises Error
    get_file('http://www.strangelyeverafter.com/image/mainImage000.jpg', 
            './notafolder/', console_info=True) #Raises Error

    print 'The following will succeed.'
    # The directory notafolder should be created.
    get_file('http://www.strangelyeverafter.com/image/mainImage000.jpg', 
            './notafolder/img000.jpg', console_info=True) #Creates Folder
    # Invalid link.
    #get_file('http://www.strangelyeverafter.com/image/mainImage100.jpg', 
    #         './img.jpg', console_info=True)