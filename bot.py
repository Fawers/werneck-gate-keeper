import traceback
import subprocess

import telepot
from decouple import config

from arduino import serial


# Users who can trigger the commands

AUTHORIZED_USERNAMES = config('AUTHORIZED_USERNAMES').split(',')


# Arduino serial constants

ACTIVATE_GATE = b'1'

RESET_SERVO = b'0'


class Bot(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = self.getMe()['username']

    def reset_messages(self):
        updates = self.getUpdates(timeout=1)

        if updates:
            self.getUpdates(timeout=1, offset=updates[-1]['update_id']+1)

    def handle_message(self, msg):
        if 'text' not in msg:
            return

        if msg['text'].startswith('/'):
            self.handle_command(msg)

    def handle_command(self, msg):
        # Run not if username is not authorized
        if msg['from'].get('username') not in AUTHORIZED_USERNAMES:
            self.sendMessage(msg['chat']['id'], '401')
            return

        command = msg['text'].replace('@' + self.username, '').split(' ', 1)[0]
        method = 'handle_' + command[1:]

        if hasattr(self, method):
            getattr(self, method)(msg)

    def handle_ativar_portao(self, msg):
        self.handle_bateria(msg, True)

    def handle_bateria(self, msg, send_only_if_discharging=False):
        battery_name = subprocess.getoutput('upower -e | grep -E BAT')
        battery_status = subprocess.getoutput(
            "upower -i %s | grep -E '(state|percentage)'" % battery_name)
        battery_info = battery_status.split('\n')

        response = '```\n%s\n%s```' % (
            battery_info[0].strip(), battery_info[1].strip()
        )

        if not send_only_if_discharging or \
           send_only_if_discharging and 'discharging' in response:
            self.sendMessage(msg['chat']['id'], response, parse_mode='markdown')

    def handle_resetar_servo(self, msg):
        serial.write(RESET_SERVO)
        response = serial.readline()

        if not response:
            response = 'No response received'
        else:
            response = 'arduino: ' + response.decode('utf-8')

        self.sendMessage(msg['chat']['id'], response)

    def run(self, reset_messages=True):
        if reset_messages:
            self.reset_messages()

        last_offset = 0

        while True:
            try:
                updates = self.getUpdates(timeout=60, offset=last_offset)

                if updates:
                    for u in updates:
                        self.handle_message(u['message'])

                    last_offset = updates[-1]['update_id'] + 1

            except KeyboardInterrupt:
                break
            except:
                traceback.print_exc()

bot = Bot(config('TELEGRAM_BOT_TOKEN'))
