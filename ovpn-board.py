#!/usr/bin/env python3

CLIENT_LIST_DELIM = "Common Name,Real Address,Bytes Received,Bytes Sent,Connected Since"
ROUTING_TABLE_DELIM = "Virtual Address,Common Name,Real Address,Last Ref"

client_list = {}
routing_table = {}
clients = []

f = open('fakedata.csv', 'r')
data = f.read()
f.close()

for s in data.splitlines():
    if len(s.split(',')) == 5 and s != CLIENT_LIST_DELIM:
        obj = s.split(',')
        client_list[obj[1]] = obj
    elif len(s.split(',')) == 4 and s != ROUTING_TABLE_DELIM:
        obj = s.split(',')
        routing_table[obj[2]] = obj

if len(routing_table) != len(client_list):
    print('invalid file!')
    exit(1)

for k, client in client_list.items():
    clients.append({
        'name': client[0],
        'real_ip': client[1].split(':')[0],
        'vpn_ip': routing_table[k][0],
        'received': client[2],
        'sent': client[3],
        'since': client[4],
    })

for client in clients:
    print(client)
