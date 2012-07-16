from zope.sendmail.interfaces import IMailDelivery
from zope.component import getUtility
from config import create_emailUtilities

import logging

log = logging.getLogger('gs.email')

def send_email(sender, recipients, email, xverp=False):
    if not (isinstance(recipients, list) or isinstance(recipients, tuple)):
        recipients = [recipients]

    create_emailUtilities()
        
    mailer = getUtility(IMailDelivery, 'gs.maildelivery')
    mailer.send(sender, recipients, email)
    log.info("Sent email of length: %s to %s from %s" %
                                      (len(email), recipients, sender))
