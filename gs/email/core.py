# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import
from logging import getLogger
log = getLogger('gs.email')
from zope.sendmail.interfaces import IMailDelivery
from zope.component import getUtility
from .config import create_emailUtilities
# FIXME: config
#: The maximum number of email addresses in a batch
MAX_BATCH = 50


def send_email(sender, recipients, email):
    '''Send an email message to some recipients

:param str sender: The address of the person, or group, that is
                   responsible for sending the email message. This will
                   become the from-address on the *envelope;* it is
                   separate from the :mailheader:`From`,
                   :mailheader:`Sender`, and :mailheader:`Reply-to`
                   addresses in the email message.
:param recipients: The address of the person who should receive the email
                   message, a ``list`` of recipients, or a ``tuple``
                   containing the addresses of the recipients. This will
                   become the  to-address on the  *envelope;* it is separate
                   from the To, CC, and BCC addresses in the email message.
:type recipients: ``str``, ``tuple``, or ``list``.
:param str email: The email message, as a string. It needs to be a complete
                  message with headers and a body.
:returns: ``None``.

The :func:`send_email` function uses SMTP to send an  :param:`email` message
to the :param:`recipients` in *batches*. The batching is necessary to
prevent overwhelming the SMTP server (it makes management of the mail queue
easier).
'''
    if not (isinstance(recipients, list) or isinstance(recipients, tuple)):
        recipients = [recipients]
    # TODO: sort
    # --=mpj17-- Consider the wisdom of sorting the list of recipients
    # recipients.sort(key=lambda x: x[::-1])
    # This will put all the addresses to the same *host* closer together.
    create_emailUtilities()
    mailer = getUtility(IMailDelivery, 'gs.maildelivery')

    while recipients:
        if (MAX_BATCH == 0) or (MAX_BATCH > len(recipients)):
            batch = len(recipients)
        else:
            batch = MAX_BATCH

        try:
            mailer.send(sender, recipients[0:batch], email)
        except TypeError as te:
            m = 'Issue sending email of length {0} from {3} to {1}:\n{2}'
            msg = m.format(len(email), recipients[0:batch], te, sender)
            log.error(msg)
        else:
            m = "Sent email of length {0} from {3} to {1} (batchsize: {2})"
            msg = m.format(len(email), recipients[0:batch], batch, sender)
            log.info(msg)

        recipients = recipients[batch:]
