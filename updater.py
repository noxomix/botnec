import json
import os
import random
import time

import discord


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=" -> Ruhemodus"))
        if "/" in message.content:
            print('Message from {0.author}: {0.content}'.format(message))
            s = message.content.lstrip().split(' ')
            command = s[0] or ''
            value = s[1] or 'none'
            msg2 = ''
            if len(s) > 2:
                msg2 = s[2]
            with open('conf.json', 'r') as conf:
                config = json.load(conf)
            if command == '/git' and str(message.author) in config['roles']['admin']['members']:
                await self.change_presence(status=discord.Status.online)
                time.sleep(3)
                with open('private.json', 'r') as f:
                    d = json.load(f)
                if (value == "UP-" + d['name'] or value in ['*', '-']) and msg2 == '-u':
                    await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Updating..."))
                    time.sleep(1)
                    os.popen('git stash')
                    time.sleep(2)
                    os.popen('git pull')
                    time.sleep(2)
                    await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=" -> Ruhemodus"))
                    # await message.channel.send(f'```\nDer Updater "UP-{d["name"]}" wird erneut gestartet.\n```')
                    exit()
                elif value == d['name'] or value == "*":
                    await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Updating..."))
                    time.sleep(1)
                    os.popen('git stash')
                    time.sleep(4)
                    os.popen('git pull')
                    time.sleep(5)
                    os.popen('screen -S Botnec -dm python3 main.py')
                    await message.channel.send(f'```\n[UP-{d["name"]}] Der Node "{d["name"]}" wird erneut gestartet.\n```')
                    time.sleep(random.randrange(12, 25))
                    await message.channel.send(f'/check {d["name"]}')
                    await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=" -> Ruhemodus"))
                    time.sleep(3)
            elif command == '/check' and str(message.author) in config['roles']['admin']['members']:
                await self.change_presence(status=discord.Status.online)
                await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Updating..."))
                with open('private.json', 'r') as f:
                    d = json.load(f)
                if (s[1] == ("UP-" + d['name'])) or s[1] in ['*', '-']:
                    await message.channel.send(f'```\n[✅] Updater "UP-{d["name"]}" is running.\n```')
                    await message.delete()
                    await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=" -> Ruhemodus"))
                    time.sleep(10)
                    await self.change_presence(status=discord.Status.offline)
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=" -> Ruhemodus"))
        await self.change_presence(status=discord.Status.offline)


client = MyClient()

with open('private.json', 'r') as file:
    data = json.load(file)
client.run(data['utoken'])
