Within your rc.lua file:

-- used as a notification system for the check_mail.py script
mymailbox = widget({ type = "textbox", name = "mymailbox", align = "left" })
mymailbox.text = ""

and add the following line to mywibox[s].widgets = {} (in order to register
the widget):
            mymailbox,


