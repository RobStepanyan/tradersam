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

current_url = get_current_site(request)
mail_subject = 'Traders.am Email Confirmation'
message = render_to_string(
    'users_app/sign_up_activation.html',
    {
        'user': user,
        'request': request,
        'domain': current_url.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user) 
    }
)
to_email= form.cleaned_data['email']
with SMTP_SSL('smtp.yandex.ru', 465) as server:
    msg = MIMEText(message, 'html')
    msg['Subject'] = mail_subject
    msg['From'] = "Traders.am <noreply@traders.am>"
    
    server.login('noreply@traders.am', '2p%84=DUu#W4WT7*')
    server.sendmail(from_addr='noreply@traders.am', to_addrs=to_email, msg=msg.as_string())

to_email = to_email[0] + '*' * len(to_email[1:to_email.index('@')-2]) + to_email[to_email.index('@')-2:] 