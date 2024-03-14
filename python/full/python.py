# int1=10
# int2=6
# if int != int2:
#     int2=++int1
#     print(int1-int2)

import os
import requests
from pprint import pprint
import json
import re
import pandas as pd
import pdb
import yaml
import plotly.express as px
from datetime import datetime, date, timedelta
from ast import literal_eval
import PyPDF2


def laas_yaml():
    laas_excel = "Device_pool_updated.xlsx"
    final_fname = "P0_Lead_Report.csv"
    p0_tag = pd.read_csv('P0_Tagging.csv')
    ucs_info = pd.read_excel(laas_excel, sheet_name="UCS")
    router_info = pd.read_excel(laas_excel, sheet_name="Router")
    rack_numbers = ['PP17','PP18','PP19','PP20','PP22','PP23','PP24','PP25','PP26','PP27','PP28']
    rack_numbers = ['PP27']

    for rack_number in rack_numbers:
        rack_info = pd.read_excel(laas_excel, sheet_name=rack_number)
        routers = [50,58]
        for router in routers:
            try:
                with open('dev_ENG-RTP-VTST-52_2345(3)', 'r') as file:
                    demo_yaml = yaml.safe_load(file)
                    
                print("Router number is {}".format(router))
                ucs_peer = rack_info['Peer'][router]
                ucs_details = ucs_info[ucs_info['Hostname']==ucs_peer]
                print(ucs_details)
                
                
                cor=ucs_info('Cores')[router]
                print(core)
                
                memory=ucs_info('Memory')[router]
                print(memory)
                
  
               family = peer.split('-')[0]
                print(family)
                pid = '-'.join(peer.split('-')[:-1])
                print(pid)
                name = 'DEVICE-POOL/{}/{}/{}-L1SW/ENG-BGL-POOL-{}'.format(family,pid,pid,peer)
                location = 'BGL11/3/{}/{}'.format(rack_number[0]+rack_number[1],rack_number[2]+rack_number[3])
                email = 'eng-bgl-laas-admin@cisco.com'
                             
                host_ip = ucs_info['Host IP'].iloc[0].strip()
               
                netmask = 22
                gateway = '10.104.33.1'
                tags=[core,memory]
                console_ip = router_details['Terminal Server IP'].iloc[0].strip()
              
                console_port = int(router_details['Port'].iloc[0])
   
                tags = [family,pid]
                power_ip = router_details['PDU IP'].iloc[0].strip()
                power_name = "Rack " + router_details['Rack#'].iloc[0].strip() + " PDU-A"
                power_port = str(int(router_details['Outlet'].iloc[0]))
      
                power_username = 'user'
                power_password = 'Bgl11lab@123'
                power_rack = router_details['Rack#'].iloc[0]
                ucs_yaml = demo_yaml
                
                ucs_yaml['name'] = name
#                 print(name)
                ucs_yaml['location'] = location
                ucs_yaml['owner']['email'] = email
#                 router_yaml['management']['ip-address'] = mgmt_ip
                ucs_yaml['management']['gateway'] = gateway 
                router_yaml['access'][0]['ip-address'] = console_ip
                router_yaml['access'][0]['port'] = console_port
                router_yaml['access'][0]['name'] = console_ip
                router_yaml['access'][0]['username'] = 'admin'
                router_yaml['access'][0]['password'] = 'admin'
                router_yaml['tags'][1]['tag'] = tags[0] 
                router_yaml['tags'][2]['tag'] = tags[1]

                router_yaml['power'][0]['port'] = power_port 
                router_yaml['power'][0]['power-switch']['username'] = power_username
                router_yaml['power'][0]['power-switch']['password'] = power_password
                router_yaml['power'][0]['power-switch']['ip-address'] = power_ip
                router_yaml['power'][0]['power-switch']['name'] = "{}".format(power_rack)

                ucs_yaml['misc'] = ''
                ucs_yaml['tftp'] = ''
                ucs_yaml['connections'][0]['TenGigabitEthernet 0/0/0']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][0+router]
                ucs_yaml['connections'][1]['TenGigabitEthernet 0/0/1']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][1+router]
                ucs_yaml['connections'][2]['TenGigabitEthernet 0/0/2']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][2+router]
                ucs_yaml['connections'][3]['TenGigabitEthernet 0/0/3']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][3+router]
                ucs_yaml['connections'][4]['TenGigabitEthernet 0/0/4']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][4+router]
                ucs_yaml['connections'][5]['TenGigabitEthernet 0/0/5']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][5+router]
                ucs_yaml['connections'][6]['TenGigabitEthernet 0/0/6']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][6+router]
                ucs_yaml['connections'][7]['TenGigabitEthernet 0/0/7']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][7+router]

                yaml_filename = "Junk/LaaS/Outfiles/dev_ENG-BGL-POOL-{}.yaml".format(ucs_peer)
                with open(yaml_filename, 'w') as file:
                    yaml.dump(ucs_yaml, file,default_flow_style=False)
                    print("yaml file generated",yaml_filename)
            except:
        print("Router not found")