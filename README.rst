Ghost - A publishing platform for professional bloggers
=======================================================

`Ghost`_ is an open source publishing platform which is beautifully 
designed, easy to use, and free for everyone. Start a blog with Ghost 
today and learn to blog! Ghost is a lightning-fast Node.js 
application with an Ember.js admin client and Handlebars.js themes.

This appliance includes all the standard features in `TurnKey Nodejs`_,
(less tklweb-cp & node examples) and on top of that:

- Ghost:

   - Installed from upstream source code to /opt/ghost

- SSL support out of the box.
- Postfix MTA (bound to localhost) to allow sending of email (e.g.,
  password recovery).
- Webmin modules for configuring Apache2 and Postfix.

Credentials *(passwords set at first boot)*
-------------------------------------------

-  Webmin, SSH, MySQL, Adminer: username **root**
-  Ghost: username **admin**


.. _Ghost: https://ghost.org/
.. _TurnKey Nodejs: https://www.turnkeylinux.org/nodejs

