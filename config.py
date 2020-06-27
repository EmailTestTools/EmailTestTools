#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from util.log import init_log

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = BASE_DIR + '/../log/'
logger = init_log(LOG_FILE)

ACCOUNTS = {
    "account": {
        "user": "test@test.com",
        "apipass": "apipass",
        "passwd": "passwd",
        "smtp_server": "mail.test.com:25",
        "imap_server": "imap.test.com:143",
        "pop3_server": "pop.test.com:110",
        "ssl_smtp_server": "mail.test.com:465",
        "ssl_imap_server": "imap.test.com:993",
        "ssl_pop3_server": "pop.test.com:995"},
}