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
from zope.sendmail.interfaces import IMailDelivery
from zope.component import getUtility
from .config import create_emailUtilities

import logging
log = logging.getLogger('gs.email')

max_batch = 50


def send_email(sender, recipients, email):
    if not (isinstance(recipients, list) or isinstance(recipients, tuple)):
        recipients = [recipients]

    create_emailUtilities()

    mailer = getUtility(IMailDelivery, 'gs.maildelivery')

    while recipients:
        if (max_batch == 0) or (max_batch > len(recipients)):
            batch = len(recipients)
        else:
            batch = max_batch

        mailer.send(sender, recipients[0:batch], email)
        log.info("Sent email of length: %s to %s (batchsize: %s) from %s" %
                    (len(email), recipients[0:batch], batch, sender))

        recipients = recipients[batch:]
