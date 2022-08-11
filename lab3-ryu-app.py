from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib import dpid as dpid_lib
from ryu.lib import stplib
from ryu.lib.packet import ethernet, arp, ipv4, ether_types
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.topology import event

#NOTE THIS APPLICATION NEED TO RUN ALONG WITH ofctl_rest.py IN RYU CONTROLLER:
#ryu-manager lab3-ryu-app.py ofctl_rest.py

class SimpleSwitch13(app_manager.RyuApp):
    # Setting open flow protocol 1.3
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
    #_CONTEXTS = {'stplib': stplib.Stp}

    def __init__(self, *args, **kwargs):
        super(SimpleSwitch13, self).__init__(*args, **kwargs)
        self.matchList = []
        self.count = 0


    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    # The controller sends a feature request to the switch upon session establishment.
    def switch_features_handler(self, ev):
        # Retrieving the Data Flow of the switch
        datapath = ev.msg.datapath
        # Retrieving the open flow protocol of the switch
        ofproto = datapath.ofproto
        # Retrieving the local variable parser of the open flow protocol of the switch
        parser = datapath.ofproto_parser
        print('\nadding new flow entry:')
        # Extracting Switch DPID
        dpid = dpid_lib.dpid_to_str(datapath.id)
        print("DPID :"+dpid[0:2]+":"+dpid[2:4]+":"+dpid[4:6]+":"+dpid[6:8]+":"+dpid[8:10]+":"+dpid[10:12]+":"+dpid[12:14]+":"+dpid[14:16])
        self.count += 1
        print('switch count = ',self.count)
        switch = int(dpid[14:16])
        print('switch = ',switch)

        #install table-miss flow entry
        #The flow entry includes: priority, match & action

        #packet_in to controller
        #add flow to controller
        #cookie=0x0, duration=6.422s, table=0, n_packets=20, n_bytes=1632, priority=0 actions=CONTROLLER:65535

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        # Switch DPID coding
        # Core11
        # 00: 00:00: 00:00: 00(core switch-->00):01(group 1): 01(1st sw)
        # Core22
        # 00: 00:00: 00:00: 00(core):02(group1): 02(switch2)
        # Agg32
        # 00: 00:00: 00:00: 03(pod3):03(location): 01（sw）
        # pod3 agg2
        # location: from left to right, from bottom to top, start from left bottom
        # for pod x：
        # left bottom = 0（edge x1）
        # right bottom = 1（edge x2）
        # upper left = 2（agg x1）
        # upper right = 3（agg x2)
        # all pod switch DPID ended with 01
        # Host IP allocation:
        # Host h23 --> 10.2.1.2
        # 10.2（pod2）.1（connect to edge x1）.2（1st host） / 8 (to connect other subnet without L3 routing)
        # pod2 host3

        # DPID of core switch [00:00:00:00:00:0:j:i]

        # in my implement if dpid[10:12] == 0 --> core switch; else indicate pod 1-4
        if switch == 1:
            ip = '10.0.0.1'
            mask = "255.255.255.255"
            match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=(ip, mask))
            action = [parser.OFPActionOutput(1)]
            print("prefix: " + ip + " output port : " + str(1))
            self.matchList.append(match)
            self.add_flow(datapath, 100, match, action)
            tcp_match = parser.OFPMatch(eth_type=0x0800,ip_proto=6)
            tcp_actions = [parser.OFPActionOutput(2)]
            self.add_flow(datapath, 2, tcp_match, tcp_actions)
            nontcp_match = parser.OFPMatch(eth_type=0x0800,)
            nontcp_actions = [parser.OFPActionOutput(3)]
            self.add_flow(datapath, 1, nontcp_match, nontcp_actions)


        elif switch == 3:
            ip = '10.0.0.2'
            mask = "255.255.255.255"
            match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=(ip, mask))
            action = [parser.OFPActionOutput(2)]
            print("prefix: " + ip + " output port : " + str(1))
            self.matchList.append(match)
            self.add_flow(datapath, 100, match, action)
            tcp_match = parser.OFPMatch(eth_type=0x0800,ip_proto=6)
            tcp_actions = [parser.OFPActionOutput(1)]
            self.add_flow(datapath, 2, tcp_match, tcp_actions)
            nontcp_match = parser.OFPMatch(eth_type=0x0800)
            nontcp_actions = [parser.OFPActionOutput(3)]
            self.add_flow(datapath, 1, nontcp_match, nontcp_actions)


        elif switch == 2:
            ip = '10.0.0.1'
            mask = "255.255.255.255"
            match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=(ip, mask))
            action = [parser.OFPActionOutput(1)]
            print("prefix: " + ip + " output port : " + str(1))
            self.matchList.append(match)
            self.add_flow(datapath, 100, match, action)
            ip = '10.0.0.2'
            mask = "255.255.255.255"
            match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=(ip, mask))
            action = [parser.OFPActionOutput(2)]
            print("prefix: " + ip + " output port : " + str(2))
            self.matchList.append(match)
            self.add_flow(datapath, 100, match, action)



        elif switch == 4:
            ip = '10.0.0.1'
            mask = "255.255.255.255"
            match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=(ip, mask))
            action = [parser.OFPActionOutput(2)]
            print("prefix: " + ip + " output port : " + str(2))
            self.matchList.append(match)
            self.add_flow(datapath, 100, match, action)
            ip = '10.0.0.2'
            mask = "255.255.255.255"
            match = parser.OFPMatch(eth_type=0x0800, ipv4_dst=(ip, mask))
            action = [parser.OFPActionOutput(1)]
            print("prefix: " + ip + " output port : " + str(1))
            self.matchList.append(match)
            self.add_flow(datapath, 100, match, action)

        #Aggregation Switch
        # DPID of agg switch [00:00:00:00:00:pod:switch:01]


    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]

        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)


