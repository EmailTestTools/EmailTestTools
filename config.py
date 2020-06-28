#!/usr/bin/env python

import os, json
from util.util import init_log,banner

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = BASE_DIR + '/log/run.log'
FUZZ_PATH = BASE_DIR + '/config/fuzz.json'
RULE_PATH = BASE_DIR + '/config/rule.json'
ACCOUNT_PATH = BASE_DIR + '/config/account.json'

logger = init_log(LOG_FILE)

with open(RULE_PATH, 'r') as f:
    CONFIG_RULES = json.load(f)

with open(ACCOUNT_PATH, 'r') as f:
    ACCOUNTS = json.load(f)



# The domain name to be tested
target_domain = "target"

account = ACCOUNTS[target_domain]
user = account['user']
passwd = account['apipass']
smtp_server = account['smtp_server']

receiveUser = "xxx@gmail.com"
#Change receiveUser to what you like to test.


subject = 'This is subject'
content = """This is content"""
filename = None
image = None









