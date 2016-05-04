#! /usr/bin/python

import fileinput
import re

config = "/opt/ghost/config.js"
old = "mail: {},"
new = """
        mail: {
            transport: 'SMTP',
            options: {
                service: 'sendmail',
            }
        },
"""

for line in fileinput.input(config,inplace=1):
    line = line.replace(old,new)
    print line,
