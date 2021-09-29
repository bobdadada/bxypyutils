from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

__all__ = ['notify_self', 'send_email']


def notify_self(server, emailbox, msg, subject=None):
    """
    Send an email to ourself

    :param server: (host, port, needssl) gives the hostname and port of smtp service, and will build a 
        TLS-encrypted connection if needssl is True.
    :param emailbox: (addr, passwd) gives the address and password of one's mailbox.
    :param msg: message.
    :param subject: subject of the message. default: None.

    >>>notify_self(('localhost', 25), ('name@domain', 'passwd'), 'A test email', 'Test')
    >>>notify_self(('localhost', 465, True), ('name@domain', 'passwd'), 'A test email', 'Test')
    """
    if len(emailbox) != 2:
        raise ValueError(
            'Please enter the correct email address and password with format (addr, passwd)')
    addr, _ = emailbox

    send_email(server, emailbox, [addr], msg, subject)


def send_email(server, emailbox, toaddrs, msg, subject=None):
    """
    Send an email to multiple receivers.

    :param server: (host, port, needssl) gives the hostname and port of smtp service, and will build a 
        TLS-encrypted connection if needssl is True.
    :param fromemailbox: (addr, passwd) gives the address and password of one's mailbox.
    :param toaddrs: [addr, addr, ...] list of email addresses that need to be sent 
    :param msg: message.
    :param subject: subject of the message. default: None.

    >>>send_email(('localhost', 25), ('name@domain', 'passwd'), ['toname@domain',], 'A test email', 'Test')
    >>>send_email(('localhost', 465, True), ('name@domain', 'passwd'), ['toname@domain',], 'A test email', 'Test')
    """
    if len(emailbox) != 2:
        raise ValueError(
            'Please enter the correct email address and password with format (addr, passwd)')
    addr, password = emailbox

    if isinstance(server, six.string_types):
        host, port, needssl = server, 25, False
    elif isinstance(server, (tuple, list)):
        if len(server) == 1:
            host, port, needssl = server[0], 25, False
        elif len(server) == 2:
            host, port = server
            needssl = False
        elif len(server) == 3:
            host, port, needssl = server
        else:
            raise ValueError(
                'Please enter the host and port of the SMTP service with format (host, port)')
    else:
        raise ValueError(
            'Please enter the host and port of the SMTP service with format (host, port)')

    if needssl:
        smtpObj = smtplib.SMTP_SSL(host, port)
    else:
        smtpObj = smtplib.SMTP(host, port)

    smtpObj.login(addr, password)

    for toaddr in toaddrs:
        # Create a plain message
        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = Header(formataddr((False, addr)), 'utf-8')   # Sender
        message['To'] = Header(formataddr(
            (False, toaddr)), 'utf-8')    # Receiver
        message['Subject'] = Header(str(subject), 'utf-8')

        smtpObj.sendmail(addr, [toaddr], message.as_string())

    smtpObj.close()
