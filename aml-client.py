#!/usr/bin/env python3

import sys

#import from the 21 Developer Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

#set up bitrequest client for BitTransfer requests
wallet = Wallet()
username = Config().username
requests = BitTransferRequests(wallet, username)

#server address
server_url = 'http://localhost:5000/'

def buy_aml():

    # Ask user to input text in english
    print("Welcome to the AML query service.\n")
    inp_first_name = input("Do you want to filter by first name (press enter if not):\n")
    inp_last_name = input("Do you want to filter by last name (press enter if not):\n")
    inp_nationality = input("Do you want to filter by nationality (example: 'Afghan', press enter if not):\n")
    inp_dob = input("Do you want to filter by date of birth (format: dd/mm/yyyy, press enter if not):\n")
    inp_group_type = input("Do you want to filter by group type (values: Individual or Entity, press enter if not):\n")

    # Send request to server with user input text and user's wallet address for payment
    sel_url = server_url+'aml?first_name={0}&last_name={1}&nationality={2}&dob={3}&group_type={4}'
    response = requests.get(url=sel_url.format(inp_first_name, inp_last_name,inp_nationality,inp_dob,inp_group_type))

    # Print the translated text out to the terminal
    print("The following is the result of your request\n")
    print(response.text)

if __name__ == '__main__':
    buy_aml()