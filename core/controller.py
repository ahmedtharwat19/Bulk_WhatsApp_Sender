import threading
import time

class AppController:
    def __init__(self, browser, sender, countdown, antiban):
        self.browser = browser
        self.sender = sender
        self.countdown = countdown
        self.antiban = antiban
        self.running = False

    def start(self):
        self.running = True

        self.browser.ensure_ready()
        self.countdown.run()

        for target in self.sender.targets():
            if not self.running:
                break

            self.antiban.before_send()
            self.sender.send(target)
            self.antiban.after_send()

    def stop(self):
        self.running = False
