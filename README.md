# CVSender
Automate sending your resume to recruiters

# AUTHOR 
```
    [+] AUTHOR:       Yasser Janah
    [+] GITHUB:       https://github.com/yasserjanah
    [+] TWITTER:      https://twitter.com/th3x0ne
    [+] FACEBOOK:     https://fb.com/yasser.janah0
```

# Screenshots
<strong align="center">Linux OS</strong>

<p align="center">
    <img src="https://i.ibb.co/YjmnzFz/Screenshot-select-area-20210706130025.png">
</p>

<strong align="center">Windows OS</strong>

<p align="center">
    <img src="https://i.ibb.co/4tD14MR/Screenshot-select-area-20210706120917.png">
</p>

# Installation
```
git clone https://github.com/yasserjanah/CVSender
cd CVSender/
pip3 install -r requirements.txt
```

# Usage

1. edit <code>conf/config.ini</code> file.
<p align="center">
    <img src="https://i.ibb.co/nRZbszG/Screenshot-select-area-20210706125503.png">
</p>

- change <strong>SMTP_SERVER</strong> value to your mail server (if you will be using your Gmail account don't change the value).
- change <strong>SMTP_PORT</strong> value to your mail server port (if you will be using your Gmail account don't change the value).
- change <strong>SMTP_EMAIL</strong> value to your own e-mail.
- change <strong>SMTP_PASS</strong> value to your own e-mail password. (if you will be using your Gmail account, please create new App Password from <a href="https://myaccount.google.com/apppasswords">Here</a>.
- change <strong>SENDER_NAME</strong> to your full name.
- change <strong>MAIL_SUBJECT</strong>.
- change <strong>CV_PATH</strong> value to your resume path.
- change <strong>TEMPLATE</strong> value to your email template (or let it in default template, but you should make changes to example.html).

2. create a file that contains emails (each one in a different line).
3. run the script.
```
    python CVSender.py --emails list_of_emails.txt
```

# Result
<p align="center">
    <img src="https://i.ibb.co/YTJdY5n/Screenshot-select-area-20210706144431.png">
</p>
