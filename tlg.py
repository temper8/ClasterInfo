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



async def get_channels(bot):
    channels = {}
    res = await bot.get_updates()
    #print(res)
    for r in res:
        tmp = r.my_chat_member
        if type(tmp) is telegram._chatmemberupdated.ChatMemberUpdated:
            if tmp.chat.type == 'channel':
                #print(tmp.chat)
                channels[tmp.chat.title] = tmp.chat.id
    print(channels)                
    return channels

async def send_msg(channel, message):
    bot = telegram.Bot(token= get_bot_token('site.json'))
    try:
        await bot.initialize()
        # code
        print('bot initialize')
        channels = await get_channels(bot)

        if channel in channels:        
            await bot.send_message(chat_id= channels[channel], text= message)
            print(f'{channel} : {message}')
        else:
            print(f"can't find channel {channel} ")
    finally:
        await bot.shutdown()

def send_message(channel, message):
    asyncio.run(send_msg(channel, message))

if __name__ == "__main__":
    print('test tlg')
    send_message('Claster Info', 'Hello')

