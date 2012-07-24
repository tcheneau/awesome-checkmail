#!/bin/env python3
# -*- coding : utf8 -*-
import socket, ssl, getpass, imaplib, time, os, argparse, sys
from subprocess import *
from functools import partial

import configparser

# delays between 2 checks
checkdelay = 60

debug = False

DEFAULT_CFG = "~/.config/awesome/mail.cfg"

def print_debug(string):
    global debug
    if debug:
        print(string)

class awesome:
    p=None
    _widget = ""
    def __init__(self, widget_name):
        self._widget = widget_name
    def write_message(self,message):
        # may need exception handling
        self.p = Popen("awesome-client",  stdin=PIPE)
        text = self._widget + "=\"" + message + "\"\n"
        self.p.stdin.write(text.encode("utf8"))
        self.p.communicate()
        # awesome-client call should have terminated by now

class MailServer:
        _server_name=""
        _port=993
        _name=""
        _login=""
        _password=None
        _color="blue"
        _directories=[]
        # connexion to the IMAP server
        _connexion=None
        # indicates the status: "logued" or "not logued"
        _status="not logued"

        def __init__(self,
                     server_name,
                     port,
                     login,
                     password,
                     directories,
                     color,
                     printed_name):
                self._server_name=server_name
                self._login= login
                self._port = port
                self._password=password
                self._directories=directories
                self._name=printed_name
                self._color=color

                self.connect()
                self.login()
        
        def connect(self):
            """function to connecting to the mail server"""
            try:
                    print_debug("login on: %s" % self._name) 
                    self._connexion = imaplib.IMAP4_SSL(self._server_name, self._port)
            except (imaplib.IMAP4.abort, socket.gaierror, socket.error) as err:
                    print("unable to connect to ", self._name, "(", self._port, "):", err)
                    self._connexion=None
        def login(self):
            """function to log in the mail server"""
            try:
                if self._password:
                    self._connexion.login(bytes(self._login, encoding='utf8').decode("utf8"), bytes(self._password, encoding='utf8').decode("utf8"))
                # or prompt the password to the user
                else:
                    print("Please enter password for user ", self._login, " on ", self._name)
                    self._connexion.login(self._login, getpass.getpass())
                self._status="logued"
            except (imaplib.IMAP4.error, AttributeError) as err:
                print("unable to login on: ", self._name, ":", err)
            else: 
                print_debug("Successfully logued in %s as %s" % (self._name, self._login))

        def list_mailbox(self):
            if self._connexion==None or self._status=="not logued":
                self.connect()
                self.login()
                # might be modified in the future
                return ""
            else:
                localstring = ""
                try:
                        for mailbox in self._directories:
                            (status,message) = self._connexion.select(mailbox,readonly=1)
                            if status=="NO":
                                print("the mailbox %s doesn't exist on %s" % (mailbox, self._server_name))
                                continue
                            (status,message)= self._connexion.search(None,'UNSEEN')
                            if message!=[b'']:
                                localstring += " " + mailbox + '(' + str(len(message[0].decode("utf8").split(" "))) + ')' 
                except (imaplib.IMAP4.error,socket.gaierror,ssl.SSLError,socket.error) as err:
                    print("unable to fetch data from ", self._server_name, ":", err)
                    # resetting connexion
                    self._connexion=None
                return localstring


        def __str__(self):
            local_string=self.list_mailbox()
            if self._connexion==None or self._status=="not logued":
                return "<span color=\'%(_color)s\'>Not connect/logued on %(_server_name)s</span>" % self.__dict__
            else:
                #we have no mail on this server
                if local_string=="":
                    return ""
                else:
                    return '<span color=\''+  self._color + '\'> [' \
                                 +  self._name \
                                 +  local_string \
                                 + ']</span>'

def parser_server_config(cfg_obj):
    servers = []
    for server in cfg_obj.sections():
        getelm = partial(cfg_obj.get, server)
        servers.append(MailServer(server_name = server,
                                  port = getelm("Port"),
                                  login = getelm("Username"),
                                  password = getelm("Password"),
                                  directories = eval(getelm("Folders")),
                                  color = getelm("Color"),
                                  printed_name= getelm("Name")))

    return servers


if __name__ == "__main__":


    # read the configuration file
    config = configparser.ConfigParser()

    parser = argparse.ArgumentParser(description="Print unread mail nicely in Awesome")

    parser.add_argument("--path", default="~/.config/awesome/mail.cfg")


    args = parser.parse_args()




    # try to load the default path
    configfile = os.path.expanduser(args.path)
    if os.path.isfile(configfile):
        print_debug("reading configuration file {}".format(configfile))
        config.read(configfile)
    else:
        # no default configuration file is present, user needs to create a new one
        print("no configure file is present, please copy a sample configuration from \
               /usr/share/doc/awesome-checkmail/example/ to {}".format(DEFAULT_CFG))

        # TODO:
        # create the directory if needed (os.mkdir)
        # copy the file

        sys.exit(-1)




    debug = config.getboolean("global","debug")
    widget = config.get("global","widget_name")
    checkdelay = config.getint("global", "check_delay")

    config.remove_section("global")

    server_list= parser_server_config(config)

    client = awesome(widget)
    while True:
        new_mail=[]
        for server in server_list:
            new_mail.append(str(server))

        client.write_message("".join(new_mail))
        print_debug(client._widget + "=\"" +"".join(new_mail) + "\"\n")
        time.sleep(checkdelay)

