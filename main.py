import time
import imaplib
import email
import os
import json
from threading import Thread


class SiriControl(Thread):
    def __init__(self, callback, username, password):
        Thread.__init__(self)
        self.callback = callback
        try:
            self.last_checked = -1
            self.mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
            self.mail.login(username, password)
            self.mail.list()
            self.mail.select("Notes")

            result, uidlist = self.mail.search(None, "ALL")
            try:
                self.last_checked = uidlist[0].split()[-1]
            except IndexError:
                pass

        except imaplib.IMAP4.error as e:
            print("[ERROR] ", e)

    def fetch_command(self):
        self.mail.list()
        self.mail.select("Notes")
        result, uidlist = self.mail.search(None, "ALL")
        try:
            latest_email_id = uidlist[0].split()[-1]
        except IndexError:
            return

        if latest_email_id == self.last_checked:
            return

        self.last_checked = latest_email_id
        result, data = self.mail.fetch(latest_email_id, "(RFC822)")
        voice_command = email.message_from_string(data[0][1].decode('utf-8'))
        return str(voice_command.get_payload()).lower().strip()

    def run(self):
        print("Starting up...")
        print("\n")
        while True:
            try:
                spokenText = self.fetch_command()
                if spokenText:
                    self.callback(spokenText.lower())
            except TypeError:
                pass
            except Exception as exc:
                print("[ERROR] {exc}".format(
                    **locals()))
                print("Restarting...")
            time.sleep(1)
