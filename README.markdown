Awesome's mail checker application
==================================


Introduction
------------

Awesome deserved a distraction free notification system (no blinking text, no
popup window, etc.) to let you know about your new unread mails over you
multiple mail servers. I looked for an application that does just that, but
that was in vain. So, I decided to code mine. After almost two years of use,
I'm satisfied with its functionning of the code, so I'm releasing it.

If you want to check how it looks like before you jump to the installation,
check out the screenshot section.

Dependencies
------------

* Python 3
* that pretty much all you need, because Python is "battery included"

Install
-------

You can run the script directly from the source directory (`python3
checkmail.py`). May you need to install the script system wide, I believe it
would be as simple as:

	python3 setup.py install

Setup
-----

Within your rc.lua file (which should by default be in the
$HOME/.config/awesome directory), you need to perform the following steps:

* create a news "mymailbox" widget (the name can be changed, but the mail.cfg
  file must be modified accordingly) by adding the following lines in your
  rc.lua

````-- used as a notification system for the checkmail.py script
	mymailbox = widget({ type = "textbox", name = "mymailbox", align = "left" })
	mymailbox.text = ""
````

* register the widget by adding the following line after the
  `mywibox[s].widgets = {}` line (in order to register the widget):

````
	mymailbox,
````

Screenshot (because one picture is worth thousand words and I don't intend to write as much)
--------------------------------------------------------------------------------------------

![For an awesome looking screenshot, have a look at the screenshot.png file in the repo](screenshot.png)

TODO
----

As I am currently the only user of checkmail.py, I do not intend to write any
of this extension, unless someone asks for it:

* graphical password typing (currently using the getpass module)
* connect to IMAP servers (that is withouh SSL support)
* improve the setup part so that only small interactions are required by the
  user (that is YOU!)

