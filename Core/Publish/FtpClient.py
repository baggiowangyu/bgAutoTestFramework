#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ftplib
import os
import socket


class FtpClient:

    def __init__(self, ftp_host, ftp_user, ftp_pass):
        self.ftp_host = ftp_host
        self.ftp_user = ftp_user
        self.ftp_pass = ftp_pass
        # self.ftp

    def Connect(self):
        try:
            self.ftp = ftplib.FTP(self.ftp_host)
        except (socket.error, socket.gaierror) as e:
            print(e)
            return False

        try:
            self.ftp.login(self.ftp_user, self.ftp_pass)
        except ftplib.error_perm:
            print(u"FTP账号或密码错误")
            self.ftp.quit()
            return False

        return True

    def PushFile(self, filepath, ftppath):
        try:
            self.ftp.storbinary('STOR %s' % ftppath, open(filepath, 'rb'))
        except ftplib.error_perm:
            print(u"推送文件失败")
            os.unlink(filepath)
            return False

        self.ftp.quit()
        return True
