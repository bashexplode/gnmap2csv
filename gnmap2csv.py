#!/usr/bin/python
# Scripted by Jesse Nebling (@bashexplode)
# Works with both masscan and nmap results
import re
import csv
import argparse

parser = argparse.ArgumentParser(description='Convert GNMap file to CSV by IP address | open ports')
parser.add_argument('inputfile')
parser.add_argument('outputfile')
args = parser.parse_args()

writer = csv.writer(open(args.outputfile, 'a+', newline=''), delimiter=',') 
hostports = {}

for line in open(args.inputfile):
    try:
        if "Ports:" in line:
            host = ""
            if "Timestamp" in line:
                host = line.split('\t')[1].split()[1] 
            else:
                host = line.split('\t')[0].split()[1]
            if host not in hostports.keys():
                hostports[host] = {}
            if "Ports" not in hostports[host].keys():
                portslist = re.findall(r'(\d*)/open/',line)
                hostports[host]["Ports"] = portslist
            else:
                portslist = re.findall(r'(\d*)/open/',line)
                for port in portslist:
                    if port not in hostports[host]["Ports"]:
                        hostports[host]["Ports"].append(port)                
                
        # hostname = re.findall(r'Timestamp: [0-9]+\tHost: (.+?)\(.+\)\tPorts:', line)[0]
    except: 
        pass

for host in hostports.keys():
    ports = list(map(int, hostports[host]["Ports"]))
    ports.sort()
    ports = list(map(str, ports))
    outputlist = [host, "; ".join(ports)]
    writer.writerow(outputlist)
