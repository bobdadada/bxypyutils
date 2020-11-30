from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

__all__ = ['notify_self']

def notify_self(server, emailbox, msg, subject=None):
    """
    Send an email to ourself

    :param server: (host, port) gives the hostname and port of smtp service.
    :param emailbox: (addr, passwd) gives the address and password of one's mailbox.
    :param msg: message.
    :param subject: subject of the message. default: None.

    >>>notify_self(('localhost', 25), ('name@domain', 'passwd'), 'A test email', 'Test')
    """
    if len(emailbox) != 2:
        raise ValueError('Please enter the correct email address and password with format (addr, passwd)')
    addr, password = emailbox

    if isinstance(server, six.string_types):
        host, port = server, 25
    elif isinstance(server, (tuple, list)):
        if len(server) == 1:
            host, port = server[0], 25
        elif len(server) == 2:
            host, port = server
        else:
            raise ValueError('Please enter the host and port of the SMTP service with format (host, port)')
    else:
        raise ValueError('Please enter the host and port of the SMTP service with format (host, port)')

    # Create a plain message
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header(formataddr(('Me', addr)), 'utf-8')   # Sender
    message['To'] =  Header(formataddr(('Me', addr)), 'utf-8')    # Receiver
    message['Subject'] = Header(str(subject), 'utf-8')

    with smtplib.SMTP() as smtpObj:
        smtpObj.connect(host, port)
        smtpObj.login(addr, password)
        smtpObj.sendmail(addr, [addr], message.as_string())
