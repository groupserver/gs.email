Configuration
=============

The configuration for sending email is controlled by the
``gsconfig.ini`` file. The configuration options_ set up how the
system connects to the SMTP server [#config]_. Delivery of email
messages can be can be to a local server, a remote server, or
turned off entirely as shown in the `configuration examples`_
below.

Options
-------

``hostname`` (required):
  The name of the SMTP server (``localhost`` if the SMTP server
  is running on the same machine as GroupServer).

``port`` (required):
  The port that the SMTP server runs on (usually ``25``).

``username`` (optional):
  The name of the user that logs into the SMTP server to send the
  message. (Defaults to ``None``.)

``password`` (optional):
  The password used to log into the SMTP server. (Defaults to
  ``None``.)

``no_tls`` and ``force_tls`` (both optional):
  Transport Layer Security (TLS) is the replacement to the Secure
  Sockets Layer (SSL). It can be used to encrypt the
  communication between GroupServer and the SMTP server. Normally
  the system will use TLS if it is available.

  Setting the ``no_tls`` option to ``False`` will force the
  GroupServer to connect to the SMTP server *en clear*, even if
  encryption is available. This may be useful if the SMTP server
  only accepts connections from ``localhost`` and it is running
  on the same machine as GroupServer.

  Setting the ``force_tls`` to ``True`` forces GroupServer to use
  encryption to connect to the SMTP server. If TLS is not
  available then a ``RuntimeError`` is raised.

``queuepath`` (optional):
  The path to the ``Maildir`` folder that stores all the messages
  before processing by the SMTP server. Defaults to
  ``/tmp/mailqueue``.

``processorthread`` (optional):
  If ``True`` (the default) then a separate thread will be
  started to handle the queue and pass the email messages on to
  the SMTP server. If ``False`` the email messages will just be
  written to the file in ``queuepath`` and not be processed
  (which is **very** useful for testing).

``xverp`` (optional):
  If ``True`` then XVERP will be used when the email messages are
  sent [#xverp]_.

.. _configuration examples:

Examples
--------

Setting up delivery to the local SMTP server, from the
GroupServer instance called ``main``:

.. code-block:: ini

  [config-main]
  smtp = local

  [smtp-local]
  hostname = localhost
  port = 25
  no_tls = True
  queuepath = /tmp/main-mail-queue
  xverp = True

:Note: There will be more than the ``smtp`` option for the
       configuration of the ``main`` GroupServer
       instance. However, the other options have been left out
       for clarity.

Setting up delivery to a remote SMTP server, from the GroupServer
instance called ``production``:

.. code-block:: ini

  [config-production]
  smtp = remote

  [smtp-remote]
  hostname = remote.host.name
  port = 2525
  username = user_on_the_remote_server
  password = password_on_the_remote_server
  force_tls = True
  queuepath = /tmp/production-mail-queue
  processorthread = True
  xverp = True

Setting up a test system to not send out email:

.. code-block:: ini

  [config-test]
  smtp = none

  [smtp-none]
  hostname = localhost
  port = 25
  queuepath = /tmp/test-mail-queue
  processorthread = False

.. [#config] Configuration is handled by the ``gs.email.config``
             module.  It uses the ``gs.config`` module to read
             the configuration information
             <https://github.com/groupserver/gs.config>


.. [#xverp] For more information about XVERP see `The Postfix
            VERP Howto
            <http://www.postfix.org/VERP_README.html>`_.
