#!/usr/bin/python3

import logging
import socket
import sys
import select

irc = {
    'host': '',
    'port': 1459,
}

user = {
    'nick': 'nick',
    'ip': 'userIp',
}


def __log__(e):
    """
        Return the error log.
    """
    logging.exception(e)


def irc_conn():
    """
        Establish connection with the IRC server.
    """
    try:
        print('Connecting to the server : {port}...'.format(**irc))
        sock.connect((irc['host'], irc['port']))
    except socket.error:
        print('Error: Unable to connect to IRC server {host}:{port}'.format(**irc))
        sys.exit(1)


def send_data(data):
    """
        Send a data to the server.

    :param data: Data block to send
    """
    sock.send(data.encode())


def join(channel):
    """
        Join a channel

    :param channel: Target channel.
    """
    try:
        send_data("JOIN %s" % channel)
    except ValueError as e:
        print('Error: channel cannot be empty.')
        __log__(e)


def nick_first():
    """
        Define a nick for a user.

    """
    try:
        n = input('Choose a nickname:')
        print('You chose %s' % n)
        send_data('NICK %s' % n)
        return n
    except Exception as e:
        print('Error: nickname cannnot be empty.')
        __log__(e)


def nick(n):
    """
        Define a nick for a user.

    """
    try:
        send_data('NICK %s' % n)
    except Exception as e:
        print('Error: nickname cannnot be empty.')
        __log__(e)


def private(usr, msg):
    """
        Send a private message to an user
    :param msg:
    :param usr
    """
    try:
        send_data("MSG %s %s" % (usr, msg))
    except ValueError as e:
        print('Error: user cannot be empty.')
        __log__(e)


def rename(channel):
    """
        Rename channel
    @param channel: The new name of the channel
    """
    try:
        send_data("REN %s" % channel)
    except ValueError as e:
        print('Error: channel cannot be empty')
        __log__(e)


"""ADMINISTRATOR COMMANDS"""


def grant(u):
    if u:
        send_data("GRANT %s" % u)


def kick(u):
    """
        Kick the client from its channel.

    :param u: Target client.
    """
    if u:
        send_data("KICK %s" % u)


def send_msg():
    i, o, e = select.select([sys.stdin], [], [], 0.5)

    command = 'ACK' if not i else sys.stdin.readline().strip()

    # entered a command
    if command != 'ACK':
        # is a simple command
        if command == '/LIST':
            send_data("LIST")
        elif command == '/WHO':
            send_data("WHO")
        elif command == '/LEAVE':
            send_data("LEAVE")
        elif command == '/BYE':
            send_data("BYE")
        elif command == '/HELP':
            send_data("HELP")

        # is a command with parameters
        elif '/' in command:
            tmp.append((command.split()))

            if '/JOIN' in command:
                if len(tmp[0]) == 1:
                    print('Please enter a channel :')
                    new = input('')
                    join(new)
                else:
                    join(tmp[0][1])

            elif '/MSG' in command:
                if len(tmp[0]) <= 2:
                    print('Please enter a name and a message :')
                    new = input('')
                    new = new.split()
                    private(new[0], new[1])
                else:
                    private(tmp[0][1], tmp[0][2])

            elif '/KICK' in command:
                if len(tmp[0]) == 1:
                    print('Please enter a name :')
                    new = input('')
                    kick(new)
                else:
                    kick(tmp[0][1])

            elif '/REN' in command:
                if len(tmp[0]) == 1:
                    print('Please enter a new name :')
                    new = input('')
                    rename(new)
                else:
                    rename(tmp[0][1])

            elif '/NICK' in command:
                if len(tmp[0]) == 1:
                    print('Please enter a nickname : ')
                    new = input()
                    nick(new)
                else:
                    nick(tmp[0][1])

            elif '/GRANT' in command:
                if len(tmp[0]) == 1:
                    print('Please enter a user name')
                    new = input('')
                    grant(new)
                else:
                    rename(tmp[0][1])

            # it's an unkown command
            else:
                send_data("ERROR")
                # send message
        else:
            send_data(command)
    # send ACK
    else:
        send_data(command)


""" MAIN """

# Opening a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
# Connects to the IRC server
irc_conn()
# Defines a nickname
nickname = nick_first()
print("You choose the nick %s, to see the commands, entered '/HELP' \n" % nickname)

while True:
    tmp = []
    message = sock.recv(4096).decode()
    if message != '' and message != 'ACK':
        print(message)
    send_msg()
