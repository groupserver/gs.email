============
``gs.email``
============
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sending email from GroupServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-03-19
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

This is the core product for *sending* email from GroupServer_
via SMTP [#receiving]_. It is used by the groups to send email to
the group members [#sending]_, and the user-profile system to
send notifications [#notifications]_.

The configuration for sending email is done through the standard
configuration system [#config]_.

From the code, the ``send_email`` function is used by most of the
GroupServer system to send the messages. Depending on the
options, those email messages may be sent using the XVERP mailer
that is also defined in this product.


Resources
=========

- Code repository: https://github.com/groupserver/gs.email/
- Documentation:
  http://groupserver.readthedocs.org/projects/gsemail/
- Questions and comments to
  http://groupserver.org/groups/development/
- Report bugs at https://redmine.iopen.net/projects/groupserver/

.. [#receiving] *Receiving* email is supported by the
   ``gs.group.messages.add.base`` product
   <https://github.com/groupserver/gs.group.messages.add.base>

.. [#notifications] Notifications are sent by the
                    ``gs.profile.notify`` product
                    <https://github.com/groupserver/gs.profile.notify/>

.. [#sending] *Sending* email from groups is handled by the
              ``gs.group.list.sender`` product
              <https://github.com/groupserver/gs.group.list.sender>

.. [#config] See the ``gs.config`` product for more information
             <https://github.com/groupserver/gs.config>


.. _GroupServer.org: http://groupserver.org/
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _onlinegroups.net: https://onlinegroups.net/
.. _GroupServer: http://groupserver.org/

..  LocalWords:  TLS SMTP XVERP BCC
