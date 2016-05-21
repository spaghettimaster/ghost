Ghost - A publishing platform for professional bloggers
=======================================================

`Ghost`_ is an open source publishing platform which is beautifully 
designed, easy to use, and free for everyone. Start a blog with Ghost 
today and learn to blog! Ghost is a lightning-fast Node.js 
application with an Ember.js admin client and Handlebars.js themes.

This appliance includes all the standard features in `TurnKey Core`_,
and on top of that:

- Ghost:

   - Installed from upstream source code to /opt/ghost

     **Security note**: Updates to Ghost may require supervision so
     they **ARE NOT** configured to install automatically. See below for
     updating Ghost.

   
   - Ghost process managed by `pm2`_.
   - Proxied by Nginx (webserver).

- SSL support out of the box.
- Postfix MTA (bound to localhost) to allow sending of email (e.g.,
  password recovery).
- Webmin module for configuring Postfix.

Supervised Manual Ghost Update
------------------------------

Note: Check the version you have install and ensure that upgrading to 
      the latest version is supported. Always enure that you have a 
      current backup before proceeding with software updates.

Assuming that updating the latest Ghost version is supported. update 
from the command line::

    DIR=/opt/ghost
    cd $DIR
    su -c "pm2 stop ghost" node
    rm -rf core
    curl -LOk https://ghost.org/zip/ghost-latest.zip
    unzip ghost-latest.zip -d ghost-temp
    cd ghost-temp
    cp -R core $DIR
    cp index.js *.json *.md $DIR
    # optional step - update default theme
    cp -R content/themes/casper $DIR/content/themes
    cd ..
    rm -r ghost-temp
    rm ghost-latest.zip 
    chown -R node:node $DIR
    su -c "npm install --production" node
    su -c "pm2 start ghost" node

Ghost does not have a security only newsletter so we recommend that 
you subcribe to the `Ghost Blog`_ to keep up to date.

Credentials *(passwords set at first boot)*
-------------------------------------------

-  Webmin, SSH, MySQL, Adminer: username **root**
-  Ghost: username **admin**


.. _Ghost: https://ghost.org/
.. _TurnKey Nodejs: https://www.turnkeylinux.org/nodejs
.. _pm2: http://pm2.keymetrics.io/
.. _Ghost Blog: https://blog.ghost.org/

