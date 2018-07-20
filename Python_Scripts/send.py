##############################################################################
#!/usr/bin/env python
#Author: Ky Ho, Jose Duron
#Date:7/18/19
# Main ETHERNET Module to Send and Recieve UDP DATAGRAMS to MICROZED
#
#This module uses a fixed IP address and port number that must match the
#IP address of the MICROZED. This module restricts the sent packages to be
#predefined commands: ping, read, rite, send, and exit.
# ############################################################################
import sys
import socket
import optparse

#define the IP and port for the zynq
UDP_IP = "192.168.1.10"
UDP_PORT = 7

delimiter = '/'

#Creates the socket
def setup_connection():
    #Display
    print "UDP target IP:", UDP_IP
    print "UDP target port:", UDP_PORT
    sock = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    return sock

#Template for commands
def setup_commands():
    parser = optparse.OptionParser()
    parser.add_option('-c', '--command', dest='command', help='Commands are "ping, read, rite, exit, send')
    parser.add_option('-m', '--message', dest='message', help='Your message')
    return parser;

def get_commands(parser):
    all_commands = ''
    packet_length = 0
    send_flag = 0

    while send_flag != -1:

        (options, args) = parser.parse_args()

        #Check if there is a command
        if options.command is None:
            options.command = raw_input('Enter a command: ')
            options.command = options.command.strip()

        #Exit - Terminate session
        if options.command == "exit":
            sock.close()
            sys.exit()

        #Send - Send current stream of commands
        elif options.command == "send":
            options.message = ''
            send_flag = -1;

        #Ping - Pings device
        elif options.command == "ping":
            options.message = ''
	    all_commands = all_commands + options.command + delimiter
            packet_length += 2;

        #Read or Rite
        elif options.command == "read" or options.command == "rite":
            options.message = raw_input('Enter a message to send: ');
            packet_length += 3;
            options.message = options.message.strip()
	    all_commands = all_commands + options.command + delimiter + options.message + delimiter

        #Invalid command
        else:
            print "Not a valid command"
            set_payload_flag = -1

        all_commands = all_commands.strip()

    #include the packet length and return back to main
    payload = str(packet_length) + delimiter + all_commands  + 'end'
    print payload;
    return payload;

def main():
    sock = setup_connection()
    parser = setup_commands()
    length_and_commands = get_commands(parser)

    #Send over the udp packet
    sock.sendto(length_and_commands, (UDP_IP, UDP_PORT))

    # recv_flag = 0;
    # while (recv_flag != -1):
    data, server = sock.recvfrom(8192)
    print >>sys.stderr, 'recieved "%s"' % data

main()
