# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014, 2015 OnlineGroups.net and Contributors.
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
from zope.component import getUtility, queryUtility
from zope.component import getGlobalSiteManager
from zope.sendmail.interfaces import IMailer, IMailDelivery
from zope.sendmail.mailer import SMTPMailer
from zope.sendmail.delivery import QueuedMailDelivery
from zope.sendmail.queue import QueueProcessorThread
from gs.config import Config, getInstanceId
from gs.config.config import bool_
from .mailer import XVERPSMTPMailer

import logging
log = logging.getLogger('gs.email')


def create_emailUtilities(instance_id=None):
    '''Create the utilities to send the email messages

:param str instance_id: The indentifier for the GroupServer instance
:returns: ``None``

The :func:`create_emailUtilities` function loads the ``smtp`` section of the
configuration of the instance specified by ``instance_id``. If no instance
is specified then :func:`gs.config.getInstanceId` is used to determine the
current instance. It then loads the following configuration options:

* ``hostname``
* ``port``
* ``username``
* ``password``
* ``no_tls``
* ``force_tls``
* ``queuepath``
* ``processorthread``
* ``xverp``

If the XVERP option is ``True`` then
:class:`gs.email.mailer.XVERPSMTPMailer` is registered as the utility used
to connect to the SMTP host; otherwise
:class:`zope.sendmail.mailer.SMTPMailer` is used. In either case the mailer
is configured with the options in the config file.'''
    if not instance_id:
        instance_id = getInstanceId()

    config = Config(instance_id)
    config.set_schema('smtp', {'hostname': str, 'port': int,
                               'username': str, 'password': str,
                               'no_tls': bool_, 'force_tls': bool_,
                               'queuepath': str, 'processorthread': bool_,
                               'xverp': bool_})
    smtpconfig = config.get('smtp', strict=False)
    name = ''
    for key in ('hostname', 'port', 'username', 'password', 'no_tls',
                'force_tls'):
        name += '+%s+' % smtpconfig.get(key, None)

    gsm = getGlobalSiteManager()
    if not queryUtility(IMailer, 'gs.mailer.%s' % name):
        if smtpconfig.get('xverp', False):
            Mailer = XVERPSMTPMailer
        else:
            Mailer = SMTPMailer

        gsm.registerUtility(
            Mailer(
                hostname=smtpconfig.get('hostname', None),
                port=smtpconfig.get('port', None),
                username=smtpconfig.get('username', None),
                password=smtpconfig.get('password', None),
                no_tls=smtpconfig.get('no_tls', None),
                force_tls=smtpconfig.get('force_tls', None)),
            IMailer, name='gs.mailer.%s' % name)
    queuePath = smtpconfig.get('queuepath', '/tmp/mailqueue')
    if not queryUtility(IMailDelivery, name='gs.maildelivery'):
        delivery = QueuedMailDelivery(queuePath)
        gsm.registerUtility(delivery, IMailDelivery, name='gs.maildelivery')
        if smtpconfig.get('processorthread', True):
            mailerObject = getUtility(IMailer, 'gs.mailer.%s' % name)
            thread = QueueProcessorThread()
            thread.setMailer(mailerObject)
            thread.setQueuePath(queuePath)
            thread.start()
