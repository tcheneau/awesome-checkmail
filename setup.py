from setuptools import setup
from glob import glob

setup(
    name = "awesome-checkmail",
    version = "0.1",
    author = "Tony Cheneau",
    author_email = "tony.cheneau@amnesiak.org",
    description = "A program for the Awesome window manager to indicate the unread email status\
            inside a widget. Works on IMAPS servers.",
    licence = "BSD",
    keywords = "awesome imap unread-email status-indication",
    
    scripts = [ 'checkmail.py'],

    data_files = [ ('share/doc/awesome-checkmail',
                    glob('*.txt') ) ,
                    ('share/doc/awesome-checkmail/example',
                    glob('example/*.*') ) ],

)

