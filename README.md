# Basic-Mininet-Ryu-Routing-topo-Ryu-REST-API-usecase
This project created a basic Mininet topo that apply special routing rule -- separate TCP and other traffic into 2 paths.
Implementation of Project - dynamic routing
1.	Topology
Here is our test topology in this project:
 
	Auto static ARP is enabled in this topo to simplify the network traffic.
2.	Feature
This Demo application have following features so far:
a)	Separate TCP and UDP traffic into different path for transmission;
b)	Exchange the roles of the two paths on the fly, using REST API provided by RYU controller.
3.	Current Progress – Inserting initiating route
To demonstrate out Proof of Concept model, Mininet (network simulator) and Ryu (SDN controller) are needed. 
First, run lab3.py and ofctl_rest.py using Ryu controller:
# ryu-manager lab3.py ofctl_rest.py
Then, run lab3_topo.py to create test topology.
# sudo python3 lab3_topo.py
Here we could see a initiating route (flow table) is inserted into all switches.
 
And with Wireshark, we could see on only TCP packets are captured on the port of switch 2, and all other packets including UDP and ICMP will be captured on port of switch 4.
 
 
4.	Current Progress – Flow table on-the-fly modification with REST API
With REST API provided by Ryu controller, we could modify the flow table with POST request easily.
To proof this concept, we implemented an application by python, and this program could Exchange the roles of the two paths on the fly.
Remember that in last part, all TCP traffic is redirected to switch2 (upper path), and all other packets are sent to switch4 (bottom path), right? Using this application, simply type in the word “reverse”, the 2 paths will exchange their role on the fly, and now, all TCP traffic is redirected to switch4 (bottom path), and all other packets are sent to switch2(upper path).
This is achieved by sending multiple POST request to insert another set of flow table into switch 1 and switch 3.
 
Python Application 
 
Reversed Packet tracking:
5.	Future Development
Our program is not powerful enough so far, but I think this proof-of-concept could indicate large potential. 
In practice, streaming service provider are taking more and more network bandwidth with the improvement of digital video resolution – 1080P is obsolete, 2K is present, and 4K is the future, and 4K video streaming could take 5 times of the network bandwidth compare to 1080P. Users are not downloading films to local disk anymore (of course, no purchasing the Blue Ray disks anymore), they purchase a VIP service and enjoy the movies on the “cloud”.
It is reasonable that one day ISP might need to separate streaming traffic and all other network traffic to make sure streaming will not take all the bandwidth so that no one could even make a single skype call. 
I believe by using more specific match field, this protocol could separate network traffic properly, and give them different transmission route, or apply proper QoS limitation to help the network working properly.
 
How to execute the demo:
 
lab3-mininet-topo.py: Mininet topo file, it should run on Mininet host.
#sudo python3 lab3-mininet-topo.py
Lab3-ryu-app.py: ryu application, insert initial flow table to switches, 
note that it should run along with ofctl_rest.py on Mininet host.
#ryu-manager lab3-ryu-app.py ofctl_rest.py
rest-addon.py: run on a host that could reach ryu controller, which could change the flow table on the fly.
	#python3 rest-addon.py
