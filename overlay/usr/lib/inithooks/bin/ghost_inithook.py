#!/usr/bin/python
"""Set Ghost email, name, password, address

Option:
--password= unless provided, will ask interactively
--email= unless provided, will ask interactively
--uname= unless provided, will ask interactively
--address= unless provided, will ask interactively
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
                                       ['help', 'password=', 'email=', 'uname=', 'address='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    email = ""
    uname = ""
    address = ""

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--password':
            password = val
        elif opt == '--email':
            email = val
        elif opt == '--username':
            uname = val
        elif opt == '--address':
            address = val
    if not address:
        offer = "https://example.com"
        valid = ""
        config = "/opt/ghost/config.js"

        def check_url(addy):
            validity = validators.url(addy)
            return validity

        def address():
            addy = d.get_input("Ghost URL", "Enter the URL for the new Ghost blog (https recommended)", "https://example.com")
            return addy

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

        while not valid:
            address = address()
            valid = check_url(address)

        current_url = get_url(config)
        replace_url(current_url,address,config)




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
