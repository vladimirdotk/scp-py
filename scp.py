#!/usr/bin/env python3

# This script is for copying files from local folder to remote
# You will need a paramiko library.

import os
import paramiko
import sys


class SftpClient():

    """ Client for copying files """

    def __init__(self, host, user, password, local_dir, remote_dir, port=22, logs=True, debug=True, logfile='scp.log',):
        self.host = host
        self.local_dir = local_dir
        self.remote_dir = remote_dir
        self.port = port
        self.username = user
        self.password = password
        self.logfile = logfile
        self.logs = logs
        self.debug = debug

    def __logging(self, message, details=None, critical=True):
        """ Logs errors and info messages

        :param string message:
        :param string details:
        :param bool critical:
        """
        if self.logs:
            import logging
            if self.debug:
                log_level = logging.DEBUG
            else:
                log_level = logging.INFO
            logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S',
                                level=log_level, filename=self.logfile)
            if critical:
                logging.critical(message)
            else:
                logging.info(message)
            if details:
                logging.critical(details)

    def __filelist(self, folder):
        """Gets files list

        :param string folder:
        :return list:
        """
        try:
            dirlist = os.listdir(folder)
            if dirlist:
                return dirlist
            else:
                self.__logging('Seems like folder '+folder+' is empty! Nothing to copy.')
                return None
        except Exception as e:
            self.__logging('Failed to get file\'s list!', e)

    def __connection(self):
        """Connects to a remote host

        :return object:
        """
        try:
            transport = paramiko.Transport((self.host, self.port))
            transport.connect(username=self.username, password=self.password)
            return transport
        except Exception as e:
            self.__logging('Connection failed!', e)
            return None

    def __client(self, transport):
        """Initializes an SFTP client

        :param object transport:
        :return object:
        """
        try:
            return paramiko.SFTPClient.from_transport(transport)
        except Exception as e:
            self.__logging('SFTP client error!', e)
            return None

    def __put(self, client, local_path, remote_path):
        """Copies file to a remote host

        :param object client:
        :param stirng local_path:
        :param string remote_path:
        """
        try:
            client.put(local_path, remote_path)
            self.__logging('Copied '+local_path, critical=False)
        except Exception as e:
            self.__logging('Failed to copy '+local_path, e)

    def __pathcorrector(self, path):
        """Checks and corrects path for self needs

        :param string path:
        :return string:
        """
        if path[-1] != '/':
            return path+'/'
        else:
            return path

    def copy(self):
        """Copies files from local folder to remote"""
        local_folder = self.__pathcorrector(self.local_dir)
        remote_folder = self.__pathcorrector(self.remote_dir)
        files_list = self.__filelist(local_folder)
        if files_list:
            transport = self.__connection()
        else:
            sys.exit('Listing fles error')
        if transport:
            sftp = self.__client(transport)
        else:
            sys.exit('Connection error')
        if sftp:
            for item in files_list:
                self.__put(sftp, local_folder+item, remote_folder+item)
            sftp.close()
            transport.close()
        else:
            sys.exit('SFTP client error')