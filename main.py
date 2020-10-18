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

    def __init__(self):
        self.clear()
        self.SetTitle('One Man Builds Discord Attachment Scraper Tool')
        
        title = Fore.YELLOW+"""
                ___  _ ____ ____ ____ ____ ___     ____ ___ ___ ____ ____ _  _ _  _ ____ _  _ ___ 
                |  \ | [__  |    |  | |__/ |  \    |__|  |   |  |__| |    |__| |\/| |___ |\ |  |  
                |__/ | ___] |___ |__| |  \ |__/    |  |  |   |  |  | |___ |  | |  | |___ | \|  |  
                                                                                                
                                    ____ ____ ____ ____ ___  ____ ____                                                
                                    [__  |    |__/ |__| |__] |___ |__/                                                
                                    ___] |___ |  \ |  | |    |___ |  \                                                
                                                                                                                    
        """
        print(title)
        with open('config.json','r') as f:
            config = json.load(f)

        self.token = config['token']
        init(convert=True)
        self.download_attachments = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Would you like to download attachments [1] yes [0] no: '))
        self.bot = commands.Bot(command_prefix='$', self_bot=True)

    def Download(self,url):
        lock = Lock()
        lock.acquire()
        response = requests.get(url)
        filename = url.split('/')[-1]
        with open('Downloads/{0}'.format(filename),'wb') as f:
            f.write(response.content)
        print(Fore.GREEN+'['+Fore.WHITE+'!'+Fore.GREEN+'] '+filename)
        lock.release()

    def Start(self):
        self.clear()
        @self.bot.event
        async def on_ready():
            print(Fore.GREEN+'['+Fore.WHITE+'!'+Fore.GREEN+'] LOGGED IN AS | '+self.bot.user.name)

        @self.bot.event
        async def on_message(message):
            if message.attachments and self.bot.user != message.author:
                url = message.attachments[0].url

                with open('attachments.txt','a') as f:
                    f.write(url+'\n')
                print(Fore.GREEN+'['+Fore.WHITE+'!'+Fore.GREEN+'] ATTACHMENT | '+url)
                if self.download_attachments == 1:
                    threading = Thread(target=self.Download,args=[url]).start()
                    
        self.bot.run(self.token,bot=False)

if __name__ == '__main__':
    main = Main()
    main.Start()