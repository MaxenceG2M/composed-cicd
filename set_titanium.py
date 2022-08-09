import sys
import os
from ipaddress import ip_address
from typing import Dict
import socket

import requests

def print_help() -> None:
    print('Set Titanium DNS configuration')
    print()
    print('Titanium is used if you, like me, run this stack on a remote host.')
    print('This script will record a DNS entry to redirect call on the hostname to this IP')
    print()
    print('usage: ')
    print(f'    $ python3 {os.path.basename(__file__)} <hostname> <ip_address>')

def do_requests(payload: Dict, verbe: str) -> Dict:
    req = requests.get(f'http://localhost:5380/api/{verbe}', params=payload)
    return req.json()

def get_login() -> str:
    payload = {'user': 'admin', 'pass': 'admin'}
    req = do_requests(payload, 'login')

    if req['status'] != 'ok':
        raise ValueError('Failed to retrieve login token', req)

    return req['token']

def create_zone(hostname, token) -> None:
    payload = {'token': token,
               'zone': hostname,
               'type': 'Primary'}
    req = do_requests(payload, 'zone/create')

def add_record_type_a(hostname: str, dest_ip: str, token: str) -> None:
    payload = {'token': token,
               'zone': hostname,
               'domain': hostname,
               'type': 'A',
               'ipAddress': dest_ip}

    req = do_requests(payload, 'zone/addRecord')
    print(req)

def add_record_type_cname(hostname: str, token: str) -> None:
    payload = {'token': token,
               'zone': hostname,
               'domain': '*.' + hostname,
               'cname': hostname,
               'type': 'CNAME'}

    req = do_requests(payload, 'zone/addRecord')
    print(req)

def test_resolution(hostname, dest_address) -> None:
    # Thanks to https://stackoverflow.com/a/19949007/1346391
    ip_list = []
    ais = socket.getaddrinfo(f'tatayoyo.{hostname}',0)
    for result in ais:
        ip_list.append(result[-1][0])
    ip_list = list(set(ip_list))

    if len(ip_list) > 1:
        return False

    if ip_list[0] != dest_address:
        return False
    return True

if __name__ == "__main__":
    args = sys.argv[1:]
    if 'help' in args or '-h' in args or '--help' in args:
        print_help()

    hostname = sys.argv[1]
    dest_address = sys.argv[2]

    print(f'Set Titanium entry with {hostname} --> {dest_address}')

    loged_token = get_login()
    create_zone(hostname, loged_token)
    add_record_type_a(hostname, dest_address, loged_token)
    add_record_type_cname(hostname, loged_token)

    print('')
    if test_resolution(hostname, dest_address):
        print('DNS correctly setted')
    else:
        print('DNS resolution fail. Have you added 127.0.0.1 in /etc/resolv.conf')
