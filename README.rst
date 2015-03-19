============
``gs.email``
============
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sending email from GroupServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-10-24
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

Introduction
============

This is the core product for *sending* email from GroupServer_
via SMTP [#receiving]_. It is used by the groups to send email to
the group members [#sending]_, and the user-profile system to
send notifications [#notifications]_.

The configuration for sending email is done through the standard
configuration system. Known solutions to problems are discussed
in the Troubleshooting_ section below.

From the code, the `send_email`_ function is used by most of the
GroupServer system to send the messages. Depending on the
options, those email messages may be sent using the XVERP mailer_
that is also defined in this product [#xverp]_.


Troubleshooting
===============

Mail is trapped in ``queuedir/new``: look to see if
``.sending_*`` or ``.rejected_*`` files have been created in the
same directory. If so, delete them and the mail should be
processed.

``send_email``
==============

The main function used to send email is ``gs.email.send_email``.

Synopsis
--------

::

   send_email(sender, recipients, email)

Arguments
---------

``sender``: 
  The address [#addr-spec]_ of the person, or group, that is
  responsible for sending the email message. This will become the
  ``From`` address on the *envelope;* it is separate from the
  From, Sender, and Reply-to addresses in the email message.

``recipients``:
  The address of the person who should receive the email message,
  a *list* of recipients, or a *tuple* containing the addresses
  of the recipients. This will become the ``To`` address on the
  *envelope;* it is separate from the To, CC, and BCC addresses
  in the email message.

``email``:
  The email message. It needs to be a complete message with the
  headers and the body.

Returns
-------

``None``.

Examples
--------

Send an email from the support-address of the site to all the
addresses of a GroupServer user:

.. code-block:: python

  eu = gs.profile.email.base.EmailUser(context, userInfo)
  send_email(siteInfo.get_support_email(), eu.get_addresses(), emailMessage)

The ``gs.profile.notify.NotifyUser`` class demonstrates how to
send an email message. The ``gs.profile.notify.MessageSender``
demonstrates how an email message is constructed using the
standard Python ``email`` module [#email]_.

Mailer
======

The mailer ``gs.email.mailer.XVERPSMTPMailer`` is a subclass of
``zope.sendmail.mailer.SMTPMailer``. It differs in the
implementation of the ``send`` method, which turns on the
``XVERP`` mail-option when it sends the email message to Postfix
[#xverp]_.

The ``XVERPSMTPMailer`` is loaded when the configuration option
``xverp`` is set to ``True``.

Resources
=========

- Code repository: https://github.com/groupserver/gs.email/
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

.. [#xverp] For more information about XVERP see *The Postfix
            VERP Howto* <http://www.postfix.org/VERP_README.html>

.. [#addr-spec] Technically it is the ``addr-spec`` portion of the email
   address, as defined by `RFC 5322 <http://tools.ietf.org/html/rfc5322>`_.
.. [#email] See <http://docs.python.org/library/email.html>.
..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/
.. _GroupServer.org: http://groupserver.org/
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _onlinegroups.net: https://onlinegroups.net/
.. _GroupServer: http://groupserver.org/

..  LocalWords:  TLS SMTP XVERP BCC
