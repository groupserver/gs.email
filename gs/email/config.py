# coding=utf-8
from gs.config import Config, getInstanceId
from gs.config.config import bool_
from mailer import XVERPSMTPMailer
from zope.component import getUtility, queryUtility
from zope.component import getGlobalSiteManager
from zope.sendmail.interfaces import IMailer, IMailDelivery
from zope.sendmail.mailer import SMTPMailer
from zope.sendmail.delivery import QueuedMailDelivery
from zope.sendmail.queue import QueueProcessorThread
import logging
import time

log = logging.getLogger('gs.email')

def create_emailUtilities(instance_id=None):
    if not instance_id:
        instance_id = getInstanceId()

    config = Config(instance_id)
    config.set_schema('smtp', {'hostname': str, 'port': int,
                               'username': str, 'password': str,
                               'no_tls': bool_, 'force_tls': bool_,
                               'queuepath': str, 'processorthread': bool_,
                               'xverp': bool_})
    smtpconfig = config.get('smtp')
    name = ''
    for key in ('hostname','port','username','password','no_tls','force_tls'):
        name += '+%s+' % smtpconfig.get(key, None)

    gsm = getGlobalSiteManager()
    if not queryUtility(IMailer, 'gs.mailer.%s' % name):
        if smtpconfig.get('xverp', False):
            Mailer = XVERPSMTPMailer
        else:
            Mailer = SMTPMailer

        gsm.registerUtility(Mailer(
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

