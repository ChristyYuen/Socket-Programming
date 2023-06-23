# Lab3 Skeleton
#
# Hints/Reminders from Lab 3:
#
# To check the source and destination of an IP packet, you can use
# the header information... For example:
#
# ip_header = packet.find('ipv4')
#
# if ip_header.srcip == "1.1.1.1":
#   print "Packet is from 1.1.1.1"
#
# Important Note: the "is" comparison DOES NOT work for IP address
# comparisons in this way. You must use ==.
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)

#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core

# You can check if IP is in subnet with 
# IPAddress("192.168.0.1") in IPNetwork("192.168.0.0/24")
# install with:
# sudo apt install python-netaddr
from netaddr import IPNetwork, IPAddress

import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Routing (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_routing (self, packet, packet_in, port_on_switch, switch_id):
    # port_on_swtich - the port on which this packet was received
    # switch_id - the switch which received this packet

    # Your code here

    msg = of.ofp_flow_mod()
    msg.match = of.ofp_match.from_packet(packet)
    msg.data = packet_in

    tcp = packet.find('tcp')

    icmp = packet.find('icmp')


    if switch_id == 1:
      if ip.dstip == "20.1.1.0/24" or ip.dstip == "10.0.1.0/24" and ip.srcip == "10.0.1.0/24" or ip.srcip == "20.1.1.0/24" and icmp:
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        self.connection.send(msg)
    elif switch_id == 2:
      if ip.dstip == "10.0.1.0/24" or ip.dstip == "30.0.1.0/24" and ip.srcip == "10.0.1.0/24" or ip.srcip == "30.0.1.0/24" and tcp:
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        self.connection.send(msg)
    else:
      pass




    pass

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_routing(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Routing(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
