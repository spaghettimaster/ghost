#!/usr/bin/python
"""Set Ghost email, name, URL, password

Option:
--password= unless provided, will ask interactively
--email= unless provided, will ask interactively
--addy= unless provided, will ask interactively
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

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'password=', 'email=', 'addy=', 'uname='])
    except getopt.GetoptError, e:
        usage(e)

    password = ""
    email = ""
    addy = ""
    uname = ""

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--password':
            password = val
        elif opt == '--email':
            email = val
	elif opt == '--addy':
	    addy = val
        elif opt == '--username':
            uname = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password("Ghost Password","Enter new password for the Ghost blogger account (>= 8 characters).")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email("Ghost Email","Enter email address for the Ghost blogger account.","admin@example.com")

    if not addy:
        if 'd' not in locals():
            d = Dialog('Turnkey Linux - First boot configuration')
        addy = d.get_input(
            "Ghost URL (not IP address)",
            "Enter the full URL of the Ghost Blog.",
            "http://my-ghost-blog.org")

    if not uname:
        if 'd' not in locals():
            d = Dialog('Turnkey Linux - First boot configuration')

        uname = d.get_input(
            "Ghost Account Name",
            "Enter the Ghost blogger's name (real name recommended).",
            "Blogger Unknown")

#Kept for reference
#hash = hashlib.md5(password).hexdigest()

    hash = bcrypt.hashpw(password,bcrypt.gensalt())



    dbase = "/opt/ghost/content/data/ghost.db"
    uid = "1"
    con = lite.connect(dbase)
    with con:
        cur = con.cursor()
        #cur.execute('INSERT INTO users ("id", "name", "password", "email") VALUES (1,"uname","hash","email");')
	    cur.execute('UPDATE roles_users SET user_id="4" WHERE id="1";')
        cur.execute('UPDATE users SET password=\"%s\" WHERE id="1";' % hash)
        cur.execute('UPDATE users SET name=\"%s\" WHERE id="1";' % uname)
        cur.execute('UPDATE users SET email=\"%s\" WHERE id="1";' % email)
        cur.execute('UPDATE users SET status=\"active\" WHERE id="1";')

        con.commit()

    for line in fileinput.FileInput("/opt/ghost/config.js",inplace=1):
        line = line.replace("http://my-ghost-blog.com",addy)
        print line

if __name__ == "__main__":
    main()
