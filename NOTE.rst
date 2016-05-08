

======================================
Ghost appliance for use with TklDev
======================================

Summary
=========


* Create a dedicated Ghost (http://tryghost.org) (blog) appliance using TklDev from Turnkey GNU/Linux (http://turnkeylinux.org). Intended to be a turnkey solution that provides a ready-to-run blogging platform upon receiving answers to a few brief, clear prompts.

* derived from TKL's Nodejs Appliance at https://github.com/turnkeylinux-apps/nodejs.

* Relies on Node 0.10.40 (recommended by Ghost documentation) (http://support.ghost.org/supported-node-versions/)

* to be used with with TklDev (https://www.turnkeylinux.org/tkldev) to generate bootable install ISO based on `TKL Core <https://www.turnkeylinux.org/core>`_, which in turn is based on Debian "Jessie" 8.

* Installs ghost latest-stable. Confirmed to work on 0.7.8 and 0.7.9

* Based on Nodejs appliance; relies on sqlite3 for db

Details
=======

* Relies on `pm2 <http://pm2.keymetrics.io/>`_ for daemonization (init.d/ghost)

* during build: python in conf.d/ configures email for sendmail.

* admin interface at <ghost_url>/ghost: auto redirected to secure http (https)

* https enabled

* In addition to packages installed by Nodjs appliance, installs *python-bcrypt* and *python-pysqlite2* (plan/main)

* Installs *Ghost 0.7.9* from zip (conf.d/ghost): configured to install latest stable.

* Additional inithook prompts for initial Ghost blogger password and email address (credentials) as well as the URL of the Ghost instance. With that information (which is validated), it prepares the sqlite3 database and ghost config. file (overlay/usr/lib/inithooks)

* Configured for production environment rather than default dev env. Installs with npm install --production

* daemonized with pm2 with node user. Found that unless very careful, pm2 will not start after reboot. Important check.

* Configured in /opt/ghost, owned by "node" user (su node)

Recommended User Configuration actions
========================================

1. Change slug for account created at first boot (from ghost-owner) using the admin interface (user profile). This can't be done with sql from inithook without breaking links.

3. In preparation for first boot, have a domain secured and directed at the Ghost instance

4. After any changes to /opt/ghost/config.js::

    su node

    pm2 restart ghost

    exit

5. See markdown syntax `reference <https://daringfireball.net/projects/markdown/syntax>`_.



To Do
======

1. Make full contents of .art/; make compliant to specifications
2. Confirm email setting work as they should (I haven't been able to confirm)
4. Revise based on feedback (round 2)
5. Revise README, finally

For consideration
==================

* Rely on MySQL to run database

* Default Branch is "mail"; this branch has the most recent changes from rgoldman
