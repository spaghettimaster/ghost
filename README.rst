:author: Rik Goldman

:title: Ghost for TKLDEV readme

:date: April 4, 2016

======================================
Ghost appliance for use with TklDev
======================================

Summary
=========

*Create a dedicated `Ghost <http://tryghost.org>`_ (blog) appliance using TklDev from `Turnkey GNU/Linux <http://turnkeylinux.org>`_. Intended to be a turnkey solution that provides a ready-to-run blogging platform upon receiving answers to a few brief, clear prompts.*

* derived from TKL's Nodejs Appliance at https://github.com/turnkeylinux-apps/nodejs.

* to be used with with TklDev (https://www.turnkeylinux.org/tkldev) to generate bootable install ISO based on `TKL Core <https://www.turnkeylinux.org/core>`_, which in turn is based on Debian "Jessie" 8.

Details
=======

* Relies on `pm2 <http://pm2.keymetrics.io/>`_ for daemonization

* In addition to packages installed by Nodjs appliance, installs *python-bcrypt* and *python-pysqlite2* (plan/main)

* Installs *Ghost 0.7.8* from zip (conf.d/ghost)

* Additional inithook prompts for initial Ghost blogger password and email address (credentials) as well as the URL of the Ghost instance. With that information, it prepares the sqlite3 database and ghost config. file (overlay/usr/lib/inithooks)

* Configured for production environment rather than default dev env. Installs with npm install --production

* Configured in /opt/ghost, owned by "node" user (su node)
