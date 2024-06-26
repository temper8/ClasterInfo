import sys
import json
import asyncio
import telegram

def get_bot_token(fname:str):
    try:
        f = open(fname, 'rb')
    except OSError:
        print("Could not open/read file:", fname)
        sys.exit()
    with f:
        data = json.load(f)
    return data['bot_token']

def read_channels(fname:str):
    try:
        f = open(fname, 'r')
    except OSError:
        return {}
    with f:
        data = json.load(f)
    return data

def write_channels(fname:str, data):
    with open(fname, 'w') as f:
        json.dump(data, f, indent = 2)

async def get_channels(bot):
    channels = read_channels('channels.json')
    res = await bot.get_updates()
    #print(res)
    for r in res:
        tmp = r.my_chat_member
        #print(tmp)
        if type(tmp) is telegram._chatmemberupdated.ChatMemberUpdated:
            if tmp.chat.type == 'channel':
                #print(tmp.chat)
                channels[tmp.chat.title] = tmp.chat.id
    #print(channels)      
    write_channels('channels.json', channels)          
    return channels

async def send_msg(channel, message):
    bot = telegram.Bot(token= get_bot_token('config.json'))
    try:
        await bot.initialize()
        # code
        print('bot initialize')
        channels = await get_channels(bot)

        if channel in channels:        
            await bot.send_message(chat_id= channels[channel], text= message)
            print(f'{channel} :')
            print(message)
        else:
            print(f"can't find channel {channel} ")
    finally:
        await bot.shutdown()

def send_message(channel, message):
    asyncio.run(send_msg(channel, message))

if __name__ == "__main__":
    print('test tlg')
    send_message('Head1 Info', 'Hello')

