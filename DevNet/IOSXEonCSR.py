# curl -GET --insecure --anyauth --user developer:Cisco12345 https:///ios-xe-mgmt.cisco.com:9443/

import sys, xml.dom.minidom
from ncclient import manager

def netconf(host, port, username, password, params_dict):
    print("###################################################################")
    print("#                              NETCONF                            #")
    print("###################################################################")
    print("Device Parameters")
    print("Host: "+host)
    print("NetConf port: "+str(port))
    print("Username: "+username)
    print("Password: "+password)
    print("Attempting connecting to device....")


    m = manager.connect(host=host,port=netconf_port,username=username,password=password,device_params=params_dict)

    hostname_filter = '''
                          <filter>
                              <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                              </native>
                          </filter>
                          '''

    m_string = str(m.get_config("running", hostname_filter))
    print(m_string)

    xmlDom = xml.dom.minidom.parseString(m_string)
    print(xmlDom.toprettyxml(indent=" "))


def restconf(host, port, username, password)
    print("###################################################################")
    print("#                             RESTCONF                            #")
    print("###################################################################")
    print("Device Parameters")
    print("Host: "+host)
    print("NetConf port: "+str(port))
    print("Username: "+username)
    print("Password: "+password)
    print("Attempting connecting to device....")


def main():
    print("IOS XE on CSR Python Script")
    print("Device: CSR1000V")
    host = "ios-xe-mgmt.cisco.com"
    ssh_port = 8181
    netconf_port = 10000
    restconf_port = 9443
    username = "developer"
    password = "C1sco12345"
    params_dict = {"name" : "csr"}

    netconf(host, netconf_port, username, password, params_dict)

    restconf(host, restconf_port, username, password)





if __name__ == "__main__":
    main()