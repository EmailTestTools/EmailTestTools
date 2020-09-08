# EmailTestTools

*EmailTestTools* is a test tool to help mail server administrators check whether their email servers are vulnerable to email spoofing attacks. This tool is based on our latest research on email sender spoofing.

Our research systematically analyzes the email delivery process based on the four key steps of the authentication process: sending authentication, receiving veriﬁcation, forwarding veriﬁcation and UI rendering. 

As shown in the figure below, we defined three ways of email sender spooﬁng attacks: a. Shared MTA Attack, b. Direct MTA Attack. c. Forward MTA Attack. Futhermore, we found 14 email spooﬁng attacks capable of bypassing SPF, DKIM, DMARC and user-interface protections. 

<div align=center><img src="./img/threat_model.png" width = "600" height = "380" alt="Threat Model" align=center /></div>

By combining different attacks, a spooﬁng email can completely pass all prevalent email security protocols, and no security warning will be shown on the receiver’s UI. As a result, it is very difﬁcult to identify whether such an email is forged, even for people with a technical background.

In this repo, we  summarize the main email spoofing attack methods we have discovered. Email service administrators can use this tool to simulate real email sender spoofing attacks and evaluate and improve the security of email services.

## Installation

- Download this tool

```
git clone https://github.com/EmailTestTools/EmailTestTools.git
```

- Install dependencies

```
sudo pip install -r requirements.txt
```

> Python 3

## Getting started

As mentioned earlier, all email sender spooﬁng attacks are based on three basic methods: a. Shared MTA Attack, b. Direct MTA Attack. c. Forward MTA Attack. *EmailTestTools* mainly implements the first two methods (You can also implement Forward MTA Attack based on the first two methods, at the same time some artificial work is required)

- **Shared MTA Attack**. Attackers can use the MTA of the public mailbox service to send fake emails. Since the credibility of the sender’s MTA IP is an important factor affecting the spam engine’s decision algorithm, it is easy for attackers to spoof the email and enter the victim’s inbox. This method requires the attacker to have an available email account.
- **Direct MTA Attack**. Since the communication process between the sender’s MTA and the receiver’s MTA does not have an authentication mechanism, attackers can simulate as Sender's MTA to communicate with Receiver's MTA to send spoofed emails.

*EmailTestTools* has two modules: fuzzing module and attack module, and each module supports these two basic methods for testing.

### fuzzing module

Since some malformed sender addresses may affect the verification of email security protocols, we designed a fuzz module to try to find ways to bypass the email security protocol.

1. Generate malformed From headers.

[pre_fuzz.py](./pre_fuzz.py) will automatically grab the ABNF rules in the relevant email speciﬁcations and generate test samples according to the ABNF rules. Since common mail services usually refuse to handle emails with highly deformed headers, we have speciﬁed set certain values for our empirical experiment purposes. Besides, we also  introduced the common mutation methods in the protocol fuzz , such as header repeating, inserting spaces, inserting Unicode characters, header encoding, and case variation.

Usage:

| Short Form | Long Form | Description                                                  |
| ---------- | --------- | ------------------------------------------------------------ |
| -r         | --rfc     | The RFC number of the ABNF rule to be extracted.             |
| -t         | --target  | The field to be fuzzed in ABNF rules.                        |
| -c         | --count   | The amount of ambiguity data that needs to be generated according to ABNF rules. |

Example:

```bash
python3 pre_fuzz.py -r 5322 -t from -c 255
```

Screenshots

![screenshots](img/screenshots.png)

2. Send emails with malformed sender address

[run_test.py](./run_test.py) will automatically test the target  according to the test data. We have also carefully controlled the message sending rate with intervals over 10 minutes to minimize the impact on the target email services.

Before testing, you need to configure the recipient address in `config.py`.

```python
receiveUser = "xxx@gmail.com"
```

You can choose **Shared MTA** or **Direct MTA** to send test emails. At the same time, you can also choose **MIME FROM** or **MAIL FROM** to test.

| Short Form | Long Form | Description                                       |
| ---------- | --------- | ------------------------------------------------- |
| -m         | --mode    | Attack mode ( SMTP: Shared MTA, MTA: Direct MTA). |
| -t         | --target  | The target field to test. (MIME / MAIL )          |

For example, If you want to use Direct MTA to fuzz MIME FROM, you can execute:

```bash
python3 run_test.py -m MTA -t MIME
```

By the way, if you want to use Shared MTA, you need to configure your email account in `config/account.json`.

```json
{
  "gmail.com": {
    "user": "test@test.com",
    "apipass": "apipass",
    "passwd": "passwd",
    "smtp_server": "mail.test.com:25",
    "imap_server": "imap.test.com:143",
    "pop3_server": "pop.test.com:110",
    "ssl_smtp_server": "mail.test.com:465",
    "ssl_imap_server": "imap.test.com:993",
    "ssl_pop3_server": "pop.test.com:995"}
}
```

You can configure more than one account, and designate sending account in `config.py `.

```python
target_domain = "gmail.com"
```

### attack module

We analyze and summarize the employed adversarial techniques into two scripts that make email sender spooﬁng successful in practice. These two scripts are used to verify vulnerabilities in real life.

[smtp_send.py](./smtp_send.py) simulate as user's MUA to Sender's MTA via SMTP protocol (**Shared MTA**). The role of this tool is to test the security issues of the Sender's MTA and test whether the receiver can accept abnormal email.

Usage:

The method of configuring the sending account and recipient address is the same as above. We have built-in some attack methods and encapsulated them into functions, which you can call directly. By the way, you can use `test_normal` to check if it can work as expected before attacking.

```python
if __name__ == '__main__':
  	test_normal(user, passwd, smtp_server, receiveUser,subject,content,mime_from=None,filename=filename,mime_from1=None,mime_from2=None,mail_from=None,image=image)
    # test_mail_mime_chars_attack(user, passwd, smtp_server, receiveUser,special_unicode)
    # test_multiple_mime_from1(user, passwd, smtp_server, receiveUser)
```

[mta_send.py](./mta_send.py) simulate as Sender's MTA to communicate with Receiver's MTA (**Direct MTA**). This tool can be simulated as any email sender and can test receiver's security.

Usage:

This method does not need to configure the mailing account. We have built-in some attack methods, too. It should be noted that different attacks require different parameters, such as `mail_from`, `mime_from`, `reply_to` etc. You can specify the values of these parameters as needed. If you do not specify, the default value of the corresponding attack will be used. 
```python
if __name__ == "__main__":
    mail_from = 'xxx@test.com'
    mime_from = 'xxx@test.com'
    reply_to = mime_from
    to_email = 'xxx@gmail.com'
    subject = 'This is subject'
    content = """This is content"""
    test_normal(mail_from, to_email, subject, content, mime_from=mime_from, mime_from1=None,mime_from2=None, sender=None,helo=None,filename=None)
    # test_reverse_mime_from(to_email)
    # test_mime_from_empty(mail_from,to_email)
    # test_IDN_mime_from(to_email)
    # sender = 'admin@gmail.com'
    # test_sender(mail_from,to_email,sender)
    # test_mail_mime_attack(mail_from,to_email)
    # test_mail_mime_attack_diff_domain(mail_from,to_email)
    # test_mime_from_badchar(to_email)
```

More functions await your exploration. Have fun~

