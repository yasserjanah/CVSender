#!/usr/bin/env python3

"""
    Automate sending your resume to recruiters
    
    Author : Yasser JANAH (th3x0ne - contact@yasser-janah.com)
"""

try:
    from email_validator import validate_email, EmailNotValidError
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email.mime.text import MIMEText
    from colorama import init, Fore
    init()
    from os.path import exists, join
    from pathlib import Path, PureWindowsPath, PurePosixPath
    from multiprocessing import Process
    from configparser import RawConfigParser
    from argparse import ArgumentParser
    from time import ctime, sleep, perf_counter
    from email import encoders
    from re import search
    from sys import platform
    import smtplib
    import sys
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
except ModuleNotFoundError as err:
    exit(err)


class CVSender(object):
    def __init__(self, to_list: list):
        self.CONFIG_FILE = join("conf", "config.ini")
        self.SMTP_SERVER = self.read_config(cfg="SMTP_SERVER")
        self.SMTP_PORT = self.read_config(cfg="SMTP_PORT")
        self.SMTP_EMAIL = self.read_config(cfg="SMTP_EMAIL")
        self.SMTP_PASS = self.read_config(cfg="SMTP_PASS")
        self.SENDER_NAME = self.read_config(cfg="SENDER_NAME")
        self.CV_PATH = self._path(self.read_config(
            section="ATTACHMENTS", cfg="CV_PATH"))
        self.TEMPLATE = self._path(self.read_config(
            section="ATTACHMENTS", cfg="TEMPLATE"))

        if (not exists(self.CV_PATH)):
            exit(f"{Fore.RED}[{Fore.WHITE}+{Fore.RED}]{Fore.WHITE} CV is {Fore.RED}not exists{Fore.WHITE} at path :{Fore.YELLOW} '{Fore.CYAN}{self.CV_PATH}{Fore.YELLOW}'.")

        if (not exists(self.TEMPLATE)):
            exit(f"{Fore.RED}[{Fore.WHITE}+{Fore.RED}]{Fore.WHITE} TEMPLATE is {Fore.RED}not exists{Fore.WHITE} at path :{Fore.YELLOW} '{Fore.CYAN}{self.TEMPLATE}{Fore.YELLOW}'.")

        self.MESSAGE = ""
        self.TO_LIST: list = to_list
        self.SUBJECT: str = self.read_config(cfg="MAIL_SUBJECT")
        self.TO: str = ""

    def is_valid_email(self, email: str) -> bool:
        """
            check the validaty of an email
        """
        if(search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email.strip())):
            try:
                return validate_email(email)
            except EmailNotValidError:
                pass

        return False

    def read_config(self, section: str = "SENDER_CONFIG", cfg: str = "") -> str:
        """ 
            read config.ini file 
        """
        config = RawConfigParser()
        config.read(self.CONFIG_FILE)
        if (config.has_section(section)):
            return config.get(section, cfg)

    def _path(self, path: str) -> object:
        """
            handle paths in windows and linux
        """
        return PureWindowsPath(path) if (platform == "wind32") else PurePosixPath(path)

    def print_success(self, email: str, index: int, count: int) -> None:
        print(
            f"{Fore.CYAN}({Fore.WHITE}{index}{Fore.YELLOW}/{Fore.GREEN}{count}{Fore.CYAN}) ", end="")
        print(f"{Fore.WHITE}{email}... {Fore.GREEN}sent.{Fore.RESET}")

    def print_error(self, email: str, index: int, count: int, error_msg: str) -> None:
        print(
            f"{Fore.CYAN}({Fore.WHITE}{index}{Fore.YELLOW}/{Fore.GREEN}{count}{Fore.CYAN}) ", end="")
        print(f"{Fore.WHITE}{email}... {Fore.RED}failed {Fore.YELLOW}({Fore.RED}{error_msg}{Fore.YELLOW}).{Fore.RESET}")

    def _send(self, email, index, count) -> None:
        """
            send using SMTP - TODO: support IMAP
        """
        server = smtplib.SMTP(self.SMTP_SERVER, int(self.SMTP_PORT))
        server.ehlo()
        server.starttls()
        try:
            server.login(self.SMTP_EMAIL, self.SMTP_PASS)
        except smtplib.SMTPAuthenticationError as err:
            exit(err)

        try:
            server.sendmail(self.SMTP_EMAIL, email, self.MESSAGE.as_string())
            self.print_success(email, index, count)
        except Exception as error_msg:
            self.print_error(email, index, count, error_msg)
            exit(error_msg)

        server.quit()

    def send(self, email, index, count) -> None:
        """
            prepare and send the mail
        """

        self.MESSAGE = MIMEMultipart('alternative')
        self.MESSAGE['from'] = self.SENDER_NAME
        self.MESSAGE['to'] = email
        self.MESSAGE['subject'] = self.SUBJECT

        self.MESSAGE.attach(
            MIMEText(open(self.TEMPLATE, mode="r").read(), "html"))

        attach = MIMEBase('application', 'octet-stream')
        attach.set_payload(open(self.CV_PATH, mode="rb").read())
        encoders.encode_base64(attach)
        attach.add_header('Content-Disposition',
                          f'attachment; filename = {self.CV_PATH}')
        self.MESSAGE.attach(attach)

        self._send(email, index, count)

    def run(self) -> None:
        with open(self.TO_LIST, mode='r') as emails_list_f:
            emails_list = emails_list_f.readlines()
            count = len(emails_list)
            emails_list_f.close()

        processes: list = []

        print(
            f"{Fore.BLUE}[{Fore.WHITE}*{Fore.BLUE}]{Fore.WHITE} Preparing messages.{Fore.RESET}", end="")

        for index, email in enumerate(emails_list):

            email = email.strip().lower()

            if (email == ""):
                continue

            if (not self.is_valid_email(email)):
                self.print_error(email, index + 1, count,
                                 "might this email is not valid")
                continue

            p = Process(target=self.send, args=(email, index + 1, count,))
            p.daemon = True
            p.start()
            sleep(0.0101010)
            processes.append(p)

        print(
            f"\n{Fore.BLUE}[{Fore.WHITE}*{Fore.BLUE}]{Fore.WHITE} Sending...\n{Fore.RESET}")

        for p in processes:
            p.join()


def main():

    print(f"""\n\t\t{Fore.CYAN}
  ▄▄█▀▀▀▄█ ▀██▀  ▀█▀  ▄█▀▀▀▄█                       ▀██                  
▄█▀     ▀   ▀█▄  ▄▀   ██▄▄  ▀    ▄▄▄▄  ▄▄ ▄▄▄     ▄▄ ██    ▄▄▄▄  ▄▄▄ ▄▄  
██           ██  █     ▀▀███▄  ▄█▄▄▄██  ██  ██  ▄▀  ▀██  ▄█▄▄▄██  ██▀ ▀▀ 
▀█▄      ▄    ███    ▄     ▀██ ██       ██  ██  █▄   ██  ██       ██     
 ▀▀█▄▄▄▄▀      █     █▀▄▄▄▄█▀   ▀█▄▄▄▀ ▄██▄ ██▄ ▀█▄▄▀██▄  ▀█▄▄▄▀ ▄██▄    
    """)
    print(f"\t\t{Fore.RESET}made with {Fore.RED}<3{Fore.RESET} by : {Fore.GREEN}Yasser JANAH {Fore.YELLOW}({Fore.WHITE}th3x0ne{Fore.YELLOW}){Fore.RESET}\n")
    print(
        f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}]{Fore.WHITE} Started at {Fore.YELLOW}{ctime()}.{Fore.RESET}\n")

    parser = ArgumentParser()
    parser.add_argument('--emails', help="Emails list", required=True)
    args = parser.parse_args()

    start: float = perf_counter()

    if (not exists(args.emails)):
        print(f"{Fore.RED}[{Fore.WHITE}+{Fore.RED}]{Fore.WHITE} Email List is {Fore.RED}not exists{Fore.WHITE} at path :{Fore.YELLOW} '{Fore.CYAN}{args.emails}{Fore.YELLOW}'.")

    else:
        Sender = CVSender(args.emails)
        Sender.run()

    end: float = perf_counter() - start
    print(
        f"\n{Fore.GREEN}[{Fore.WHITE}+{Fore.GREEN}]{Fore.WHITE} Total elapsed time {Fore.YELLOW}{end:.4f} {Fore.WHITE}second(s).{Fore.RESET}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(
            f"\n{Fore.RED}[{Fore.WHITE}+{Fore.RED}]{Fore.WHITE} Ctrl+C {Fore.YELLOW}detected! ... {Fore.RED}shutting down.{Fore.RESET}\n")
    except Exception as err:
        raise err
