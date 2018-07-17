#!/usr/bin/env python
import sys
import socket
import optparse

#define the IP and port for the zynq
UDP_IP = "192.168.1.10"
UDP_PORT = 7

delimiter = ' '

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

        set_payload_flag = 0
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
            set_payload_flag = -1;
            send_flag = -1;

        #Ping - Pings device
        elif options.command == "ping":
            options.message = ''
            packet_length += 2;

        #Read or Rite
        elif options.command == "read" or options.command == "rite":
            options.message = raw_input('Enter a message to send: ');
            packet_length += 3;
            options.message = options.message.strip()

        #Invalid command
        else:
            print "Not a valid command"
            set_payload_flag = -1

        if set_payload_flag == 0:
            #Put together the command and message
            all_commands = all_commands + delimiter + options.command + delimiter + options.message
            all_commands = all_commands.strip()

    #include the packet length and return back to main
    payload = str(packet_length) + delimiter + all_commands
    return payload;

def main():
    sock = setup_connection()
    parser = setup_commands()
    length_and_commands = get_commands(parser)

    #Send over the udp packet
    sock.sendto(length_and_commands, (UDP_IP, UDP_PORT))

    data, server = sock.recvfrom(4096)
    print >>sys.stderr, 'received "%s"' % data

main()