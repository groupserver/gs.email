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
import socket
from zope.sendmail.mailer import SMTPMailer, have_ssl


class XVERPSMTPMailer(SMTPMailer):
    def send(self, fromaddr, toaddrs, message):
        """ This is effectively the same method as in SMTPMailer, only
            we also want to support mail_options to pass XVERP.

        """
        connection = self.smtp(self.hostname, str(self.port))

        # send EHLO
        code, response = connection.ehlo()
        if code < 200 or code >= 300:
            code, response = connection.helo()
            if code < 200 or code >= 300:
                m = 'Error sending HELO to the SMTP server '\
                    '(code=%s, response=%s)' % (code, response)
                raise RuntimeError(m)

        # encryption support
        have_tls = connection.has_extn('starttls')
        if not have_tls and self.force_tls:
            raise RuntimeError('TLS is not available but TLS is required')

        if have_tls and have_ssl and not self.no_tls:
            connection.starttls()
            connection.ehlo()

        if connection.does_esmtp:
            if self.username is not None and self.password is not None:
                username, password = self.username, self.password
                if isinstance(username, unicode):
                    username = username.encode('utf-8')
                if isinstance(password, unicode):
                    password = password.encode('utf-8')
                connection.login(username, password)
        elif self.username:
            m = 'Mailhost does not support ESMTP but a username is '\
                'configured'
            raise RuntimeError(m)

        connection.sendmail(fromaddr, toaddrs, message,
                            mail_options=["XVERP"])
        try:
            connection.quit()
        except socket.sslerror:
            #something weird happened while quiting
            connection.close()
