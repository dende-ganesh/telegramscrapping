
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import traceback
import time



api=input("enter my telegram details in order \n 1.api\n 2.hash\n 3.phone with country code\n").split()
api_id=int(api[0])
api_hash=api[1]
phone=api[2]


client = TelegramClient(phone, api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))


input_file = sys.argv[1]

users = []
members_file=open('members.txt')
for member in members_file:
    users.append(member)


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
        groups.append(chat)


print('Choose a group to add members:')
for i,g in zip(range(len(groups)),groups):
    print(str(i) + '-' + g.title)


t_group=groups[int(input("enter group id u to add members"))]
t_group_input = InputPeerChannel(t_group.id,t_group.access_hash)


for user in users:
        try:
            print ("Adding "+user)
            client(InviteToChannelRequest(t_group_input,[user]))
            print("user added, "+user)
            print("..............Waiting for 10 Seconds.....................")
            time.sleep(10)
        except PeerFloodError:
                    print("flood error from telegram program is stopping............................")
                    break
        except UserPrivacyRestrictedError:
                print("user cannot be added because of privacy")
        except:
            traceback.print_exc()
            print("Unexpected Error")
            continue
