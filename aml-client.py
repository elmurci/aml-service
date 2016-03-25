#!/usr/bin/env python3
import json

# import from the 21 Developer Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

# set up bitrequest client for BitTransfer requests
wallet = Wallet()
username = Config().username
requests = BitTransferRequests(wallet, username)

# server address
server_url = 'http://localhost:5000/'

def buy_aml_check():

    # Ask user to input text in english
    print("Welcome to English-to-Chinese Translation.\n")
    inp_text = input("Enter the English text that you would like translated into Chinese:\n")

    # Send request to server with user input text and user's wallet address for payment
    # 402-payable endpoint URL and request
    url = 'http://' + server_url
    response = requests.get(url=tts_url.format(text))

    # Print the translated text out to the terminal
    print("The following is the translation of the text you input.\n")
    print(response.text)


if __name__ == '__main__':
    print(buy_aml_check())