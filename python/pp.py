import os
from github import Github
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
    laas_excel = "Junk/LaaS/Device_pool_updated.xlsx"
    final_fname = "P0_Lead_Report.csv"
    p0_tag = pd.read_csv('P0_Tagging.csv')
    ucs_info = pd.read_excel(laas_excel, sheet_name="UCS")
    router_info = pd.read_excel(laas_excel, sheet_name="Router")
    rack_numbers = ['PP17','PP18','PP19','PP20','PP22','PP23','PP24','PP25','PP26','PP27','PP28']
    rack_numbers = ['PP25']

    for rack_number in rack_numbers:
        rack_info = pd.read_excel(laas_excel, sheet_name=rack_number)
        routers = [0,8,16,24,32]
        for router in routers:
            try:
                with open('Junk/LaaS/dev_ENG-BGL-POOL-C8500-12X-08_1.yaml', 'r') as file:
                    demo_yaml = yaml.safe_load(file)
                print("Router number is {}".format(router))
                peer = rack_info['Peer'][router]
                router_details = router_info[router_info['Hostname']==peer]
  
                family = peer.split('-')[0]
                print(family)
                pid = '-'.join(peer.split('-')[:-1])
                print(pid)
                name = 'DEVICE-POOL/{}/{}/{}-L1SW/ENG-BGL-POOL-{}'.format(family,pid,pid,peer)
                location = 'BGL11/3/{}/{}'.format(rack_number[0]+rack_number[1],rack_number[2]+rack_number[3])
                email = 'eng-bgl-laas-admin@cisco.com'
                             
                mgmt_ip = router_details['Mgmt IP'].iloc[0].strip()
               
                netmask = 24
                gateway = '10.105.59.1'
                console_ip = router_details['Terminal Server IP'].iloc[0].strip()
              
                console_port = int(router_details['Port'].iloc[0])
   
                tags = [family,pid]
                power_ip = router_details['PDU IP'].iloc[0].strip()
                power_name = "Rack " + router_details['Rack#'].iloc[0].strip() + " PDU-A"
                power_port = str(int(router_details['Outlet'].iloc[0]))
      
                power_username = 'user'
                power_password = 'Bgl11lab@123'
                power_rack = router_details['Rack#'].iloc[0]
                router_yaml = demo_yaml
                
                router_yaml['name'] = name
                print(name)
                router_yaml['location'] = location
                router_yaml['owner']['email'] = email
                router_yaml['management']['ip-address'] = mgmt_ip
                router_yaml['management']['gateway'] = gateway 
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

                router_yaml['misc'] = ''
                router_yaml['tftp'] = ''
                router_yaml['connections'][0]['TenGigabitEthernet 0/0/0']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][0+router]
                router_yaml['connections'][1]['TenGigabitEthernet 0/0/1']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][1+router]
                router_yaml['connections'][2]['TenGigabitEthernet 0/0/2']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][2+router]
                router_yaml['connections'][3]['TenGigabitEthernet 0/0/3']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][3+router]
                router_yaml['connections'][4]['TenGigabitEthernet 0/0/4']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][4+router]
                router_yaml['connections'][5]['TenGigabitEthernet 0/0/5']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][5+router]
                router_yaml['connections'][6]['TenGigabitEthernet 0/0/6']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][6+router]
                router_yaml['connections'][7]['TenGigabitEthernet 0/0/7']['eng-blr-aci-spine1'] = rack_info[' Leaf Node# and Intf'][7+router]

                yaml_filename = "Junk/LaaS/Outfiles/dev_ENG-BGL-POOL-{}.yaml".format(peer)
                with open(yaml_filename, 'w') as file:
                    yaml.dump(router_yaml, file,sort_keys=False)
            except:
                print("Router not found")