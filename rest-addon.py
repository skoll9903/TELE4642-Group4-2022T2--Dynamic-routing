import requests
import json
import re
import ast
import sys
ipadd = "192.168.153.21"
port = "8080"
def get_switch_id():
    url = 'http://' + ipadd + ':' + port + '/stats/switches'
    re_switch_id = requests.get(url=url).json()
    switch_id_hex = []
    for i in re_switch_id:
        switch_id_hex.append(hex(i))
    return switch_id_hex
# 通过get()和获取的dpid得到每一个交换机的流表项
def get_flow_table():
    url = 'http://' + ipadd + ':' + port + '/stats/flow/%d'
    list_switch = get_switch_id()
    all_flow = []
    for switch in list_switch:
        new_url = format(url % int(switch, 16))
        re_switch_flow = requests.get(url=new_url).json()
        all_flow.append(re_switch_flow)
    return all_flow
def post_clear_flow(dpid):
    url = 'http://' + ipadd + ':' + port + '/stats/flowentry/clear/' + str(dpid)
    response = requests.delete(url=url)
    if response.status_code == 200:
        print('Successfully Clear!')
    else:
        print('Fail!')
def post_add_flow(dpid, priority, output_port,ip_protocol=0,ipv4_dest="0.0.0.0/0",eth_type=2048,cookie=0):
    url = 'http://' + ipadd + ':' + port + '/stats/flowentry/add'
    if ip_protocol == 0:
        data = {
            "dpid": dpid,
            "cookie": cookie,
            "cookie_mask": 0,
            "table_id": 0,
            "priority": priority,
            "flags": 0,
            "match": {
                "eth_type":eth_type,
                "ipv4_dst":ipv4_dest
            },
            "actions": [
                {
                    "type": "OUTPUT",
                    "port": output_port
                }
            ]
        }
    elif ip_protocol == 6:
        data = {
            "dpid": dpid,
            "cookie": cookie,
            "cookie_mask": 0,
            "table_id": 0,
            "priority": priority,
            "flags": 0,
            "match": {
                "eth_type": eth_type,
                "ip_proto": ip_protocol
            },
            "actions": [
                {
                    "type": "OUTPUT",
                    "port": output_port
                }
            ]
        }
    else:
        data = "0"
    response = requests.post(url=url, json=data)
    if response.status_code == 200:
        print('Successfully Add!')
    else:
        print('Fail!')
# post_clear_flow(1)
# post_add_flow(1, 50, 1, 6)
def TCP_UDP():
    post_clear_flow(1)
    post_clear_flow(3)
    post_add_flow(1, 100, 1, 0,"10.0.0.1/255.255.255.255")
    post_add_flow(1, 50, 2, 6)
    post_add_flow(1, 30, 3, 0)
    post_add_flow(3, 100, 2, 0,"10.0.0.2/255.255.255.255")
    post_add_flow(3, 50, 1, 6)
    post_add_flow(3, 30, 3, 0)
def UDP_TCP():
    post_clear_flow(1)
    post_clear_flow(3)
    post_add_flow(1, 100, 1, 0, "10.0.0.1/255.255.255.255")
    post_add_flow(1, 50, 3, 6)
    post_add_flow(1, 30, 2, 0)
    post_add_flow(3, 100, 2, 0, "10.0.0.2/255.255.255.255")
    post_add_flow(3, 50, 3, 6)
    post_add_flow(3, 30, 1, 0)
def show_status(flow_table):
    TCP_ports = []
    for i in flow_table:
        switch_code  = list(i.keys())
        if switch_code == ['1']:
            for j in i['1']:
                if 'nw_proto' in j['match'].keys():
                    outport = j['actions'][0]
                    TCP_ports.append((1,outport[-1]))
        elif switch_code == ['3']:
            for j in i['3']:
                if 'nw_proto' in j['match'].keys():
                    outport = j['actions'][0]
                    TCP_ports.append((3,outport[-1]))
    return TCP_ports

print("help: input different strings for different functions")
# print("show_flow_table = show flow table of all 4 switches in the network")
print("show_status = show TCP and UDP current flow status")
print("[example: TCP = Upper, UDP = bottom (Default setting)]")
print("reverse = switch role of the 2 lines")
order = input('please input your order')


allocation = show_status(get_flow_table())
status = str()
if allocation == [(1,'2'),(3,'1')]:
    status = 'TCP traffic through upper link, UDP traffic through bottom link'
elif allocation == [(1,'3'),(3,'3')]:
    status = 'UDP traffic through upper link, TCP traffic through bottom link'
else:
    print('system error, please reboot network')
    sys.exit()
print('current line allocation is:', status)

if order == 'reverse':
    if allocation == [(1,'2'),(3,'1')]:
        UDP_TCP()
    else:
        TCP_UDP()
    allocation = show_status(get_flow_table())
    status = str()
    if allocation == [(1,'2'),(3,'1')]:
        status = 'TCP traffic through upper link, UDP traffic through bottom link'
    elif allocation == [(1,'3'),(3,'3')]:
        status = 'UDP traffic through upper link, TCP traffic through bottom link'
    else:
        print('system error, please reboot network')
        sys.exit()
    print('current line allocation is:', status)


