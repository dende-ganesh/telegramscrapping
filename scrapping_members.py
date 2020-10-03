from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
print("libraries  imported  sucessfully")


api=input("enter my telegram details in order \n 1.api\n 2.hash\n 3.phone with country code\n").split()
api_id=int(api[0])
api_hash=api[1]
phone=api[2]

client = TelegramClient('session_name', api_id, api_hash)
client.connect()


if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)


for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
print('Choose a group to scrape members')



for i,g in zip(range(len(groups)),groups):
    print(str(i) + '- ' + g.title)


group_index = input("Enter a Number: ")
group=groups[int(group_index)]

all_participants = []
all_participants = client.get_participants(group)


print('======================Adding Members to file==================')

members_file=open("members.txt",'a')

user_count=0
for user in all_participants:
    if user.username==None:
        continue
    members_file.write(user.username)
    user_count+=1
    members_file.write("\n")
members_file.close()


print('{} Members scraped successfully.'.format(user_count))
