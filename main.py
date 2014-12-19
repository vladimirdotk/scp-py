#!/usr/bin/env python3

# Main script for copying files to a remote host

from scp import SftpClient

# You should correctly fill in at least these variables
host = 'example.com'
username = 'login'
password = 'secret'
local_dir = '/home/scp-py/folder/'
remote_dir = '/home/example.com/folder/'

client = SftpClient(host, username, password, local_dir, remote_dir)
client.copy()