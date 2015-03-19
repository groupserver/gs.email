:mod:`gs.email` API Reference
=============================

.. currentmodule:: gs.email

The main function used by external code in the :func:`send_email`
function. Internally it uses the mailer_ to send messages.

``send_email``
--------------

.. autofunction:: send_email
.. autodata:: gs.email.core.MAX_BATCH

Examples
~~~~~~~~

Send an email from the support-address of the site to all the
addresses of a GroupServer user:

.. code-block:: python

  eu = gs.profile.email.base.EmailUser(context, userInfo)
  send_email(siteInfo.get_support_email(), eu.get_addresses(), emailMessage)

The :class:`gs.profile.notify.NotifyUser` class demonstrates how
to send an email message using :func:`send_email`. The
:class:`gs.profile.notify.MessageSender` class demonstrates how
an email message is constructed using the standard Python
:mod:`email` module.

Mailer
------

The :class:`gs.email.mailer.XVERPSMTPMailer` is loaded when the
configuration option ``xverp`` is set to ``True`` (see
:doc:`configuration`). As its name implies, it turns on XVERP, so
the groups can be informed when an address bounces [#xverp]_.


.. autoclass:: gs.email.mailer.XVERPSMTPMailer
   :members:

.. [#xverp] For more information about XVERP see *The Postfix
            VERP Howto* <http://www.postfix.org/VERP_README.html>

..  LocalWords:  XVERP
