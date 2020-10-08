import requests
import json
import discord
import sys
import os
from discord_webhook import DiscordWebhook
from discord import Webhook,RequestsWebhookAdapter
from discord.ext import commands
from colorama import init,Fore
from threading import Thread, Lock

class Main:
    def clear(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name in ('ce', 'nt', 'dos'):
            os.system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title_name:str):
        os.system("title {0}".format(title_name))

    def PrintText(self,info_name,text,info_color:Fore,text_color:Fore):
        lock = Lock()
        lock.acquire()
        sys.stdout.flush()
        text = text.encode('ascii','replace').decode()
        sys.stdout.write(f'[{info_color+info_name+Fore.RESET}] '+text_color+f'{text}\n')
        lock.release()

    def __init__(self):
        self.clear()
        self.SetTitle('One Man Builds Discord Attachment Scraper Tool')

        with open('config.json','r') as f:
            config = json.load(f)

        self.token = config['token']
        init()
        self.download_attachments = int(input('[QUESTION] Would you like to download attachments [1] yes [0] no: '))
        self.bot = commands.Bot(command_prefix='$', self_bot=True)

    def Download(self,url):
        lock = Lock()
        lock.acquire()
        response = requests.get(url)
        filename = url.split('/')[-1]
        with open('Downloads/{0}'.format(filename),'wb') as f:
            f.write(response.content)
        self.PrintText('DOWNLOADED',filename,Fore.GREEN,Fore.WHITE)
        lock.release()

    def Start(self):
        self.clear()
        @self.bot.event
        async def on_ready():
            self.PrintText('LOGGED IN AS',self.bot.user.name,Fore.GREEN,Fore.WHITE)

        @self.bot.event
        async def on_message(message):
            if message.attachments and self.bot.user != message.author:
                url = message.attachments[0].url

                with open('attachments.txt','a') as f:
                    f.write(url+'\n')

                self.PrintText('ATTACHMENT',url,Fore.GREEN,Fore.WHITE)
                if self.download_attachments == 1:
                    threading = Thread(target=self.Download,args=[url]).start()
                    
        self.bot.run(self.token,bot=False)

if __name__ == '__main__':
    main = Main()
    main.Start()