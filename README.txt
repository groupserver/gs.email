Introduction
============

This is the core product for *sending* email from GroupServer_ via SMTP
[#receiving]_. It is used by the groups (``Products.XWFMailingListManager``) 
to send email to the group members, and the user-profile system 
(``gs.profile.notify``) to send notifications.

The configuration_ for sending email is done through the standard
configuration system. Known solutions to problems are discussed in the
Troubleshooting_ section below.

From the code, the `send_email`_ function is used by most of the
GroupServer system to send the messages. Depending on the options, those
email messages may be sent using the XVERP mailer_ that is also defined
in this product.

Configuration
=============

The configuration options_ sets up how the mailer_ connects to the SMTP
server [#config]_. Delivery of email messages can be can be to a local
server, a remote server, or turned off entirely as shown in the
`configuration examples`_ below.

Options
-------

``hostname`` (required):
  The name of the SMTP server (``localhost`` if the SMTP server is running
  on the same machine as GroupServer).

``port`` (required):
  The port that the SMTP server runs on (usually ``25``).

``username`` (optional):
  The name of the user that logs into the SMTP server to send the
  message. (Defaults to ``None``.)

``password`` (optional):
  The password used to log into the SMTP server. (Defaults to ``None``.)

``no_tls`` and ``force_tls`` (both optional):
  Transport Layer Security (TLS) is the replacement to the Secure Sockets
  Layer (SSL). It can be used to encrypt the communication between
  GroupServer and the SMTP server. Normally the `mailer`_ will use TLS if
  it is available.

  Setting the ``no_tls`` option to ``False`` will force the GroupServer to
  connect to the SMTP server *en clear*, even if encryption is
  available. This may be useful if the SMTP server only accepts connections
  from ``localhost`` and it is running on the same machine as GroupServer.

  Setting the ``force_tls`` to ``True`` forces GroupServer to use
  encryption to connect to the SMTP server. If TLS is not available then a
  ``RuntimeError`` is raised.

``queuepath`` (optional):
  The path to the ``Maildir`` folder that stores all the messages before
  processing by the SMTP server. Defaults to ``/tmp/mailqueue``.

``processorthread`` (optional):
  If ``True`` (the default) then a separate thread will be started to
  handle the queue and pass the email messages on to the SMTP server. If
  ``False`` the email messages will just be written to the file in
  ``queuepath`` and not be processed (which is **very** useful for
  testing).

``xverp`` (optional):
  If ``True`` then XVERP will be used to send the email messages.

.. _configuration examples:

Examples
--------

Setting up delivery to the local SMTP server, from the GroupServer instance
called ``main``::

  [smtp-main]
  hostname = localhost
  port = 25
  no_tls = True
  queuepath = /tmp/main-mail-queue
  xverp = True

Setting up delivery to a remote SMTP server, from the GroupServer instance
called ``production``::

  [smtp-production]
  hostname = remote.host.name
  port = 2525
  username = user_on_the_remote_server
  password = password_on_the_remote_server
  force_tls = True
  queuepath = /tmp/production-mail-queue
  processorthread = True
  xverp = True

Setting up a Test system to not send out email::

  [smtp-test]
  hostname = localhost
  port = 25
  queuepath = /tmp/test-mail-queue
  processorthread = False

Troubleshooting
===============

Mail is trapped in ``queuedir/new``: look to see if ``.sending_*`` or
``.rejected_*`` files have been created in the same directory. If so,
delete them and the mail should be processed.

``send_email``
==============

The main function used to send email is ``gs.email.send_email``.

Synopsis
--------

::

   send_email(sender, recipients, email, xverp=False)

Arguments
---------

``sender``: 
  The address [#addr-spec]_ of the person, or group, that is responsible
  for sending the email message. This will become the ``From`` address on
  the *envelope;* it is separate from the From, Sender, and Reply-to
  addresses in the email message.

``recipients``:
  The address of the person who should receive the email message, a *list*
  of recipients, or a *tuple* containing the addresses of the
  recipients. This will become the ``To`` address on the *envelope,* and is
  separate from the To, CC, and BCC addresses in the email message.

``email``:
  The email message. It needs to be a complete message with the headers and
  the body.

``xverp``
  If set to ``True`` then XVERP information will be sent with the email
  message [#xverp]_.

Returns
-------

``None``.

Examples
--------

Send an email from the support-address of the site to all the addresses of
a GroupServer user::

  eu = gs.profile.email.base.EmailUser(context, userInfo)
  send_email(siteInfo.get_support_email(), eu.get_addresses(), emailMessage)

The ``gs.profile.notify.NotifyUser`` class demonstrates how to send an
email message. The ``gs.profile.notify.MessageSender`` demonstrates how an
email message is constructed using the standard Python ``email`` module
[#email]_.

Mailer
======

The mailer ``gs.email.mailer.XVERPSMTPMailer`` is a subclass of
``zope.sendmail.mailer.SMTPMailer``. It differs in the implementation of
the ``send`` method, which turns on the ``XVERP`` mail-option when it sends
the email message to Postfix [#xverp]_. 

The ``XVERPSMTPMailer`` is loaded when the `configuration`_ option
``xverp`` is set to ``True``.

.. [#config] Configuration is handled by the ``gs.email.config`` module.
   It uses the ``gs.config`` module to read the configuration information.
.. [#receiving] *Receiving* email is supported by the
   ``gs.group.messages.add.base`` product and the
   ``gs.group.messages.add.smtp2gs`` product. *Displaying* the messages is
   handled by the other ``gs.group.messages`` products.
.. [#xverp] For more information about XVERP see `The Postfix VERP Howto
   <http://www.postfix.org/VERP_README.html>`_.
.. [#addr-spec] Technically it is the ``addr-spec`` portion of the email
   address, as defined by `RFC 5322 <http://tools.ietf.org/html/rfc5322>`_.
.. [#email] See <http://docs.python.org/library/email.html>.
.. _GroupServer: http://groupserver.org/

..  LocalWords:  TLS SMTP XVERP BCC
