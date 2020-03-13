import hashlib
import requests
import sys
import json
from time import time


def proof_of_work(block):
    # converts JSON to string
    block_string = json.dumps(block, sort_keys=True)
    # number of proofs before finding a valid one
    proof = 0
    # while we validate the proof, it increases proof by 1.
    line = ''
    while valid_proof(block_string, proof) is False:
        proof += 1
        line += '|'
        if(len(line) > 10):
            line = ''
        print(line)
    return proof


def valid_proof(block_string, proof):
    # this returns the encoded version of the entire string
    guess = f'{block_string}{proof}'.encode()
    # This converts the encoded string into a fixed hexadecimal number
    guess_hash = hashlib.sha256(guess).hexdigest()
        
    return guess_hash[:5] == "00000"

# User Class
class User:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance
        self.transactions = []
    # Updates the user's username
    def set_name(self, username):
        self.username = username
        return f'\n Your username has been updated, {username}!\n'
    # Let the user see his/her balance
    def my_balance(self):
        return f"\nYour current balance is: {self.balance} coins.\n"
    # Let the user see his/her transactions
    def my_transactions(self):
        return f"\nList of transactions: {self.transactions}\n"


if __name__ == '__main__':

    name = input("\nWelcome to Coinbit! What would you like your username to be? ")
    # Creates new instance of user class
    user = User(name)

    message = "What would you like to do next?\n Type 'name' to change your username.\n Type 'balance' to check your current balance.\n Type 'transactions' to see a list of your transactions.\n Type 'new' to make a new transaction.\n Type 'mine' to start mining! \n Type 'quit' to quit the app.\n"

    options = str(input(f"\n Hello {name}! Glad you joined us! Here's what you can do...\n \n Type 'name' to change your username.\n Type 'balance' to check your current balance.\n Type 'transactions' to see a list of your transactions.\n Type 'new' to make a new transaction.\n Type 'mine' to start mining! \n Type 'quit' to quit the app.\n"))
    # Indefinite iterator, until app is interrupted
    while True:
        if (options == 'name'):
            while True:
                name = input('\nType your new username:\n ')
                confirmation = input('Are you sure? y/n ')
                if confirmation == 'y':
                    # updates username
                    user.name = name
                    # prints confirmation
                    print(user.set_name(name))
                    break
                # if confirmation is not y/n, errors out
                elif confirmation != 'y' and confirmation != 'n':
                    print('Invalid command, please try again.')

            options = input(message)

        elif (options == 'balance'):
            print(user.my_balance())
            options = input(message)

        elif (options == 'transactions'):
            print(user.my_transactions())
            options = input(message)

        elif (options == 'new'):
            node = "http://localhost:5000"
            # recipient to where the coin(s) will be sent
            recipient = input("\nType the username of the recipient you will be sending currency to:\n ")
            transaction_message = f"{user.my_balance()} How many coins do you want to send?\n"
    
            amount = input(transaction_message)

            while True:
                # checks if the user has enough coins to send, if not errors out.
                if int(amount) > user.balance:
                    print("\n WARNING: You don't have enough coins to complete transaction.\n")
                    amount = input(transaction_message)
                break
            
            # format in which data is sent to the back end
            post_data = {"sender": user.name, "recipient": recipient, "amount": amount}
            # end point to create our transactions
            r = requests.post(url=node + '/transactions/new', json=post_data)
            data = r.json()
            # we deduct the amount of coins the user sent
            user.balance -= int(amount)
            # we add the transaction information to the transactions list
            user.transactions.append({'sender': user.name, 'recipient': recipient, 'amount': int(amount), 'index': data['message']})
            print(f'\nTransaction completed! You have sent {amount} coin(s) to {recipient}.', data['message'])

            options = input(message)

        elif (options == 'mine'):
            node = "http://localhost:5000"
            lambda_coins = 0
            start_time = time()
            # When found, POST it to the server {"proof": new_proof, "id": username}
            print(f'Id is {user.name}')
            while True:
                r = requests.get(url=node + "/last_block")
                # Handle non-json response
                try:
                    data = r.json()
                except ValueError:
                    print("Error:  Non-json response")
                    print("Response returned:")
                    print(r)
                    break

                # TODO: Get the block from `data` and use it to look for a new proof
                new_proof = proof_of_work(data['last_block'])

                post_data = {"proof": new_proof, "id": user.name}

                r = requests.post(url=node + "/mine", json=post_data)
                data = r.json()
                end_time = time()
                result_time = end_time - start_time
                # TODO: If the server responds with a 'message' 'success'
                # add 1 to the number of coins mined and print it.  Otherwise,
                # print the message from the server.
                if (data['message'] == 'Your block has been mined and added to the chain, congrats!'):
                    end_time = time() 
                    result = end_time - start_time
                    minutes = 0
                    # it converts seconds to minutes and seconds
                    while result >= 60:
                        minutes += 1
                        result -= 60
                    lambda_coins += 1

                    print(f'The time it took was {minutes} minutes and {int(result)} seconds.')
                    print(f'Congrats! You have earned a lambda coin! Total Lambda Coins: {lambda_coins}')
                break
            options = input(message)
        elif (options == 'quit'):
            print('\nThank you for trusting Coinbit! Goodbye!\n')
            break
        else:
            print('Your input was invalid, please try again.')
            options = input(message)