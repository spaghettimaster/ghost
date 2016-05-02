#!/usr/bin/python
"""Set Ghost email, name, password

Option:
--password= unless provided, will ask interactively
--email= unless provided, will ask interactively
--uname= unless provided, will ask interactively

"""

import sys
import getopt
import subprocess
import hashlib
import bcrypt
import sqlite3 as lite
import locale
import dialog
import fileinput
from dialog_wrapper import Dialog
import re
import validators

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'password=', 'email=', 'uname=', 'addy='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    email = ""
    uname = ""
    addy = ""

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--password':
            password = val
        elif opt == '--email':
            email = val
        elif opt == '--username':
            uname = val

    if not addy:
        offer = "https://example.com"
        isvalid = ""
        config = "/opt/ghost/config.js"

        def check_url(addy):
            validity = validators.url(addy)
            return validity

        d = Dialog('Turnkey Linux - First boot configuration')

        def address():
            addy = d.get_input("Ghost URL", "Enter the URL for the new Ghost blog (https recommended)", "https://example.com")
            return addy

        addy = address()

        valid = check_url(addy)

        while not valid:
            addy = address()
            check_url(addy)

        def get_url(filein):
            f = open(filein, 'r')
            f = f.read()
            urls = re.findall(r'(http[s]?://[^\s]+)', f)
            current_url = urls[2]
            current_url = current_url.translate(None, "',")
            return current_url

        def replace_url(old,new,fileout):
            config = None
            with open(fileout,'r') as file :
                config = file.read()
            config = config.replace(old,new)
            with open(fileout, 'w') as file:
                file.write(config)
            return 0
        current_url = get_url(config)
        replace_url(current_url,addy,config)




    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password("Ghost Password","Enter new password for the Ghost blogger account (>= 8 characters).")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email("Ghost Email","Enter email address for the Ghost blogger account.","admin@example.com")

    if not uname:
        if 'd' not in locals():
            d = Dialog('Turnkey Linux - First boot configuration')

        uname = d.get_input(
            "Ghost Account Name",
            "Enter the Ghost blogger's name (real name recommended).",
            "Blogger Unknown")


        #slug = uname.replace(" ", "-")


    hash = bcrypt.hashpw(password,bcrypt.gensalt())



    dbase = "/opt/ghost/content/data/ghost.db"
    con = lite.connect(dbase)
    with con:
        cur = con.cursor()

        cur.execute('UPDATE users SET password=\"%s\" WHERE id="1";' % hash)
        cur.execute('UPDATE users SET name=\"%s\" WHERE id="1";' % uname)
        cur.execute('UPDATE users SET email=\"%s\" WHERE id="1";' % email)
        cur.execute('UPDATE users SET status=\"active\" WHERE id="1";')
        #cur.execute('UPDATE users SET slug=\"%s\" WHERE id="1";' % slug)
        con.commit()

if __name__ == "__main__":
    main()
