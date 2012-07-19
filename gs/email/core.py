from zope.sendmail.interfaces import IMailDelivery
from zope.component import getUtility
from config import create_emailUtilities

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
            batch = batchsize
        
        mailer.send(sender, recipients[0:batch], email)
        log.info("Sent email of length: %s to %s (batchsize: %s) from %s" %
                           (len(email), recipients[0:batch], batch, sender))
        
        recipients = recipients[batch:]
