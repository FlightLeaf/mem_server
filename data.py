def return_html(code):
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>验证码邮件</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 20px;
            }
            .container {
                background-color: #fff;
                border-radius: 10px;
                padding: 20px;
                max-width: 600px;
                margin: auto;
            }
            h2 {
                color: #333;
            }
            .verification-code {
                font-size: 24px;
                font-weight: bold;
                color: #e74c3c;
                margin: 20px 0;
                display: inline-block;
                padding: 10px;
                background-color: #f1c40f;
                border-radius: 5px;
            }
            p {
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>感谢您的使用</h2>
            <p>您的验证码是：</p>
            <div class="verification-code">'''+code+'''
            </div>
            <p>请将此验证码输入到相应的输入框中，以完成验证。</p>
        </div>
    </body>
    </html>
    '''