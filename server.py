#!/usr/bin/python
from __future__ import print_function
from pyrad import dictionary, packet, server
import logging
import dateutil.parser
import pytz
from datetime import *
import pymysql

#DB info
db_host = '127.0.0.1'
db_user = 'vpn-test-read'
db_password = 'somepassword'
db_name = 'vpn-test'

#Creating the read only user
#CREATE USER 'vpn-test-read'@'%' IDENTIFIED BY 'somepassword';
#GRANT SELECT ON `vpn-test`.* TO 'vpn-test-read'@'%';


def check_date(expiration):
    try:
        EXPIRE = dateutil.parser.parse(expiration)
        NOW = datetime.utcnow().replace(tzinfo=pytz.UTC)
        if NOW > EXPIRE:
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False

def query(query, params=False, commit=False):
    global db_host, db_user, db_password, db_name
    try:
        connection = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        with connection.cursor() as cursor:
            if commit:
                if not bool(params):
                    cursor.execute(query)
                else:
                    cursor.execute(query, params)
                connection.commit()
                connection.close()
                return
            else:
                if not bool(params):
                    cursor.execute(query)
                else:
                    cursor.execute(query, params)
                result = cursor.fetchall()
                connection.close()
                return result
    except Exception as e:
        print(str(e))
        try:
            connection.close()
        except:
            pass
        return

logging.basicConfig(filename="pyrad.log", level="DEBUG",
                    format="%(asctime)s [%(levelname)-8s] %(message)s")

class pfsense_radius(server.Server):

    def HandleAuthPacket(self, pkt):
        print("")
        print("Received an authentication request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        pwd = pkt.PwDecrypt(pkt['User-Password'][0])
        print('User: %s Pass: %s'  % (pkt['User-Name'], pwd))
        
        reply = self.CreateReplyPacket(pkt, **{
            "Service-Type": "Framed-User",
            #"Framed-IP-Address": "10.9.9.2",                       #If you want to manually set ip, otherwise pfsense handles
            #"Framed-IPv6-Prefix": ipv6                             #Manuall set ipv6
        })
        reply.code = packet.AccessReject
        try:
            result = query('SELECT * FROM users WHERE username = %s and password = %s', params=(pkt['User-Name'][0],pwd,))[0]
            if check_date(result['date']):
                reply.code = packet.AccessAccept
        except:
            pass
        self.SendReplyPacket(pkt.fd, reply)

    def HandleAcctPacket(self, pkt):

        print("Received an accounting request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        self.SendReplyPacket(pkt.fd, reply)

    def HandleCoaPacket(self, pkt):

        print("Received an coa request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        self.SendReplyPacket(pkt.fd, reply)

    def HandleDisconnectPacket(self, pkt):

        print("Received an disconnect request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        # COA NAK
        reply.code = 45
        self.SendReplyPacket(pkt.fd, reply)

if __name__ == '__main__':

    # create server and read dictionary
    srv = pfsense_radius(dict=dictionary.Dictionary("dictionary"))

    #Accept from any client but has to have the secret. Cant add specific host right now without modifying back server.py in pyrad
    srv.hosts["0.0.0.0/0"] = server.RemoteHost("0.0.0.0/0", b"somesecretvalue", "0.0.0.0/0")
    srv.BindToAddress("")

    # start server
    srv.Run()
