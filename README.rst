

======================================
Ghost appliance for use with TklDev
======================================

Summary
=========

* Create a dedicated Ghost (http://tryghost.org) (blog) appliance using TklDev from Turnkey GNU/Linux (http://turnkeylinux.org). Intended to be a turnkey solution that provides a ready-to-run blogging platform upon receiving answers to a few brief, clear prompts.

* derived from TKL's Nodejs Appliance at https://github.com/turnkeylinux-apps/nodejs.

* Relies on Node 0.10.40 (http://support.ghost.org/supported-node-versions/)

* to be used with with TklDev (https://www.turnkeylinux.org/tkldev) to generate bootable install ISO based on TKL Core <https://www.turnkeylinux.org/core>, which in turn is based on Debian "Jessie" 8.

Details
=======

* Relies on `pm2 <http://pm2.keymetrics.io/>`_ for daemonization

* In addition to packages installed by Nodjs appliance, installs *python-bcrypt* and *python-pysqlite2* (plan/main)

* Installs *Ghost 0.7.8* from zip (conf.d/ghost)

* Additional inithook prompts for initial Ghost blogger password and email address (credentials) as well as the URL of the Ghost instance. With that information, it prepares the sqlite3 database and ghost config. file (overlay/usr/lib/inithooks)

* Configured for production environment rather than default dev env. Installs with npm install --production

* Configured in /opt/ghost, owned by "node" user (su node)

To Do
======

1. Transfer useable art from another repo (previous attempt)
2. Clean up for initial sniff based on previous feedback
3. Revise based on checklist
4. Revise based on feedback (round 2)
5. Revise README to include more detail and reflect changes made in revision process
6. Revise so appliance doesn't rely on db file in overlay **DONE**
