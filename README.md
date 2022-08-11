# Basic-Mininet-Ryu-Routing-topo-Ryu-REST-API-usecase
This project created a basic Mininet topo that apply special routing rule -- separate TCP and other traffic into 2 paths.
Implementation of Project - dynamic routing
Auto static ARP is enabled in this topo to simplify the network traffic.
Feature
This Demo application have following features so far:
a)	Separate TCP and UDP traffic into different path for transmission;
b)	Exchange the roles of the two paths on the fly, using REST API provided by RYU controller.

How to execute the demo:
 
#lab3-mininet-topo.py
#Mininet topo file, it should run on Mininet host.
#sudo python3 lab3-mininet-topo.py

#Lab3-ryu-app.py
#ryu application, insert initial flow table to switches, 
#note that it should run along with ofctl_rest.py on Mininet host.
#ryu-manager lab3-ryu-app.py ofctl_rest.py

#rest-addon.py: 
#run on a host that could reach ryu controller, which could change the flow table on the fly.
#python3 rest-addon.py
