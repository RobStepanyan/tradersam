from smtplib import SMTP_SSL
from email.mime.text import MIMEText

with SMTP_SSL('smtp.yandex.ru', 465) as server:
    # server.docmd('AUTH', 'XOAUTH2' + 'QWdBRUE3cWpPTl8tQUFZX2xmcmpvTGw2alU5aGpaaDU0S2VnYVdV')
    # server.set_debuglevel(True)
    message = 'This message is sent from Python.'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Subject'
    msg['From'] = "Traders.am <noreply@traders.am>"
    
    server.login('noreply@traders.am', '2p%84=DUu#W4WT7*')
    
    server.sendmail(from_addr='noreply@traders.am', to_addrs='robert1stepanyan@gmail.com', msg=msg.as_string())