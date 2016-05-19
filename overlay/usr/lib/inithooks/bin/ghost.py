#!/usr/bin/python
"""Set Ghost admin password, email, name and domain

Option:
    --password=     unless provided, will ask interactively
    --email=        unless provided, will ask interactively
    --uname=        unless provided, will ask interactively
    --domain=       unless provided, will ask interactively
"""

import sys
import getopt
import bcrypt
import sqlite3
from dialog_wrapper import Dialog
import re

DEFAULT_UNAME = 'Blogger Unknown'

def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email=',
                                        'uname=', 'domain='])
    except getopt.GetoptError, e:
        usage(e)

    password = ''
    email = ''
    uname = ''
    domain = ''

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val
        elif opt == '--uname':
            uname = val
        elif opt == '--domain':
            domain = val

    if not password:
        d = Dialog('Turnkey Linux - First boot configuration')
        password = d.get_password(
            "Ghost Password",
            "Enter a new password for the Ghost blogger account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('Turnkey Linux - First boot configuration')

        email = d.get_email(
            "Ghost Email",
            "Please enter email address for the Ghost blogger account.",
            "admin@example.com")

    if not uname:
        if 'd' not in locals():
	    d = Dialog('Turnkey Linux - First boot configuration')

	uname = d.get_input(
		"Ghost Account Name",
		"Enter the Ghost blogger's name (real name recommended).",
		DEFAULT_UNAME)

    if uname == "DEFAULT":
        uname = DEFAULT_UNAME

    if not domain:
        if 'd' not in locals():
            d = Dialog('Turnkey Linux - First boot configuration')

        domain = d.get_input(
            "Ghost Domain",
            "Enter the domain to serve Ghost, include http(s) protocol, defaults to https.",
            "https://www.example.com")

        if not domain.startswith('https://') and not domain.startswith('http://'):
			domain = 'https://'+domain

	with open('/opt/ghost/config.js', 'r') as fob:
		all_config = fob.read()

	current_url = re.findall(r'(https?://\S+)', all_config)[2] # third occurance in file
	current_url = current_url.translate(None, "',")
	all_config = all_config.replace(current_url, domain)

	with open('/opt/ghost/config.js', 'w') as fob:
		fob.write(all_config)


	hashed_pw = bcrypt.hashpw(password, bcrypt.gensalt())

	dbase = '/opt/ghost/content/data/ghost.db'
	con = sqlite3.connect(dbase)
	with con:
		cur = con.cursor()

        cur.execute('UPDATE users SET password=\"%s\" WHERE id="1";' % hashed_pw)
        cur.execute('UPDATE users SET name=\"%s\" WHERE id="1";' % uname)
        cur.execute('UPDATE users SET email=\"%s\" WHERE id="1";' % email)
        cur.execute('UPDATE users SET status=\"active\" WHERE id="1";')
        con.commit()	

if __name__ == '__main__':
	main()
