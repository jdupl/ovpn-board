import time

class Reader():

    def __init__(self, filename='/etc/openvpn/openvpn-status.log'):
        self.last_update = 0
        self.filename = filename
        self.cached_clients = {}

    def get_clients(self):
        if time.time() - self.last_update > 15:
            self.update()
        return self.cached_clients

    def update(self):
        self.last_update = time.time()
        self.cached_clients['dhcp'] = []
        self.cached_clients['servers'] = []

        for client in self.parse_file():
            net_range = client['vpn_ip'].split('.')[2]

            if int(net_range) > 127:
                self.cached_clients['dhcp'].append(client)
            else:
                self.cached_clients['servers'].append(client)


    def parse_file(self):
        CLIENT_LIST_DELIM = "Common Name,Real Address,Bytes Received,Bytes Sent,Connected Since"
        ROUTING_TABLE_DELIM = "Virtual Address,Common Name,Real Address,Last Ref"

        client_list = {}
        routing_table = {}
        clients = []

        f = open(self.filename, 'r')
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

        return clients
