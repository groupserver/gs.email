# -*- coding: utf-8 -*-
##############################################################################
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
##############################################################################
from __future__ import absolute_import
from logging import getLogger
log = getLogger('gs.email')
from zope.sendmail.interfaces import IMailDelivery
from zope.component import getUtility
from .config import create_emailUtilities

max_batch = 50


def send_email(sender, recipients, email):
    if not (isinstance(recipients, list) or isinstance(recipients, tuple)):
        recipients = [recipients]
    # TODO: sort
    # --=mpj17-- Consider the wisdom of sorting the list of recipients
    # recipients.sort(key=lambda x: x[::-1])
    # This will put all the addresses to the same *host* closer together.
    create_emailUtilities()
    mailer = getUtility(IMailDelivery, 'gs.maildelivery')

    while recipients:
        if (max_batch == 0) or (max_batch > len(recipients)):
            batch = len(recipients)
        else:
            batch = max_batch

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
