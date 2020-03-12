import hashlib
import requests
import time

import sys
import json


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    
    block_string = json.dumps(block, sort_keys=True)
    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1

    return proof

# @staticmethod
def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 3
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    # TODO return True or False
    return guess_hash[:3] == "000"

if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    lambda_coins = 0
    # Run forever until interrupted
    while True:
        start_time = time.time()

        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break
        
        print('data', data)

        # TODO: Get the block from `data` and use it to look for a new proof
        last_block = data['last_block']
        new_proof = proof_of_work(last_block)

        if new_proof:
            print(f'Proof found: {new_proof}')

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        # TODO: Catch non-json responses error
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # TODO: If the server responds with a 'message' 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.
        if 'Your block has been mined and added to the chain, congrats!' in data['message']:
            end_time = time.time() 
            result = end_time - start_time
            minutes = 0
            while result >= 60:
                minutes += 1
                result -= 60
            lambda_coins += 1

            print(f'The time it took was {minutes} minutes and {int(result)} seconds.')
            print(f'Congrats! You have earned a lambda coin! Total Lambda Coins: {lambda_coins}')