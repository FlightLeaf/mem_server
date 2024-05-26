from flask import jsonify
from flask_mail import Message
from threading import Thread

from data import return_html


def send_async_email(app, msg, mail):
    with app.app_context():
        mail.send(msg)


def send_email(app, data, mail):
    user = data['email']
    code = data['code']
    msg = Message(subject='来自5:20AM的邮件',
                  sender="718856370@qq.com",
                  recipients=[user])
    msg.body = '来自5:20AM的邮件'
    msg.html = (return_html(code))
    thread = Thread(target=send_async_email, args=[app, msg, mail])
    thread.start()
    return jsonify({'status': 'success', 'message': 'Email sent successfully'}), 200
