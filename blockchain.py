import functools
import os
import json
from collections import OrderedDict

from hash_util import hash_string_256, hash_block

# Reward to Miners (For Creating a New Block)
MINING_REWARD = 10

# Pre-Built First Starting Block for the Blockchain
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': [],
    'proof': 100
}

# Initialising the Blockchain List
blockchain = [genesis_block]

# Open Transacations (Unhandled Transactions before Being Put into the Blockchain)
open_transactions = []

# Our Identifier (The Owner of this Blockchain Node) E.g. For Sending Coins ...
owner = "Sam"

# Data Type: Set (No Duplicates) - Registered Participants: Owner + Other People Involved in Sending + Receiving Coins
participants = {'Sam'}


def load_data():
    """
    Read the blockchain and open_transactions data from the 'blockchain.txt'.

    We use 'readlines()' to get the data in a list format.

    We need to use 'json.loads()' to make sure the json-string data is loaded as a Python object.

    We need to us 'global' to let the function to know that these are global variables.

    We need to handle 'OrderedDict' for the data and load the data as 'OrderedDict' (only for transactions).

    We execute this 'load_data()' right after we define this and at the begining of this Python file.
    """
    if os.path.exists('blockchain.txt'):
        with open('blockchain.txt', mode='r') as f:
            file_content = f.readlines()

            global blockchain
            blockchain = json.loads(file_content[0][:-1])

            updated_blockchain = []

            for block in blockchain:
                updated_block = {
                    'previous_hash':
                    block['previous_hash'],
                    'index':
                    block['index'],
                    'proof':
                    block['proof'],
                    'transactions': [
                        OrderedDict([('sender', tx['sender']),
                                     ('recipient', tx['recipient']),
                                     ('amount', tx['amount'])])
                        for tx in block['transactions']
                    ]
                }
                updated_blockchain.append(updated_block)

            blockchain = updated_blockchain

            global open_transactions
            open_transactions = json.loads(file_content[1])

            updated_transactions = []

            for tx in open_transactions:
                updated_transaction = OrderedDict([('sender', tx['sender']),
                                                   ('recipient',
                                                    tx['recipient']),
                                                   ('amount', tx['amount'])])
                updated_transactions.append(updated_transaction)

            open_transactions = updated_transactions


load_data()


def save_data():
    """
    Save the blockchain data into a file (Always Overwrite).

    We call this 'save_data()' whenever we add a new transaction or mine a new block.

    We use 'json.dumps()' save the data as a json-string into the file.

    Note that we save_data in a 'OrderedDict' (only for transactions).
    """
    with open('blockchain.txt', mode='w') as f:
        f.write(json.dumps(blockchain))
        f.write('\n')
        f.write(json.dumps(open_transactions))


def valid_proof(transcations, last_hash, proof):
    guess = (str(transcations) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)

    # print(f'valid_proof(): {guess_hash}')
    # print(f'valid_proof(): {guess_hash[0:2]}')

    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0

    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1

    return proof


def get_balance(participant):
    """
    Calculate and return the balance for a participant.

    Arguments:
        :participant: The person for whom to calculate the balance.
    """
    # Find all the transactions (amount of coins) for the transactions that the participant is the sender (sending out coins) in the Blockchain
    tx_sending = [[
        tx['amount'] for tx in block['transactions']
        if tx['sender'] == participant
    ] for block in blockchain]

    # Find all the transactions (amount of coins) for the transactions that the participant is the sender (sending out coins) in the Blockchain
    open_tx_sending = [
        tx['amount'] for tx in open_transactions if tx['sender'] == participant
    ]

    # Sum up all the sending transactions
    tx_sending.append(open_tx_sending)

    # The first 2 empty lists in the 'tx_sending' are from the 'genesis_block' and the 'mining_block' which the 'participant' is NOT the 'sender'
    # The third block is ths list which holds all open transactions (the amount that the participant sent), e.g. [8.9, 6.4]
    print(tx_sending)

    amount_sent = functools.reduce(
        lambda tx_sum, tx: tx_sum + sum(tx)
        if len(tx) > 0 else tx_sum + 0, tx_sending, 0)

    # amount_sent = 0

    # for tx in tx_sending:
    #     if len(tx) > 0:
    #         amount_sent += tx[0]

    # We don't count the open transactions because the coins are NOT in the wallet yet
    tx_receiving = [[
        tx['amount'] for tx in block['transactions']
        if tx['recipient'] == participant
    ] for block in blockchain]

    amount_received = functools.reduce(
        lambda tx_sum, tx: tx_sum + sum(tx)
        if len(tx) > 0 else tx_sum + 0, tx_receiving, 0)

    # amount_received = 0

    # for tx in tx_receiving:
    #     if len(tx) > 0:
    #         amount_received += tx[0]

    return amount_received - amount_sent


def get_last_transaction_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def verify_transaction(transactiion):
    """
    Verify a transaction by checking whether the sender has enough / sufficient coins.

    Arguments:
        :transaction: The transaction that should be verified.
    """
    sender_balance = get_balance(transactiion['sender'])

    # print(f'verify_transcation::sender_balance:: {sender_balance}')
    # print(f"verify_transcation::transcation_amount:: {transactiion['amount']}")

    return sender_balance >= transactiion['amount']


def add_transaction(recipient, sender=owner, amount=1.0):
    """
    Append a new value as well as the last blockchain value to the open transactions.

    Arguments:
        :sender: The participant who is sending out the coins.
        :recipient: The participant who is receiving the coins.
        :amount: The amount of the coins sent with the transaction (default value = 1.0)
    """
    transaction = OrderedDict([('sender', sender), ('recipient', recipient),
                               ('amount', amount)])

    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)

        save_data()

        return True
    return False


def mine_block():
    """ Create a NEW block and add open transactions to the block. """
    last_block = get_last_transaction_value()

    hashed_block = hash_block(last_block)

    proof = proof_of_work()

    # We need to make sure the hash always has the same order for the data to prevent hashing error
    # reward_transaction = {
    #     'sender': "MINING",
    #     'recipient': owner,
    #     'amount': MINING_REWARD,
    # }

    reward_transaction = OrderedDict([('sender', 'MINING'),
                                      ('recipient', owner),
                                      ('amount', MINING_REWARD)])

    # Create a NEW copy of the transaction instead of manipulating the original open_transaction list
    # To ensure that if the mining is failed by some reasons, we won't reward transaction stored in the open transactions
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)

    # block = {
    #     'previous_hash': hashed_block,
    #     'index': len(blockchain),
    #     'transactions': copied_transactions,
    #     'proof': proof
    # }

    block = OrderedDict([('previous_hash', hashed_block),
                         ('index', len(blockchain)),
                         ('transactions', copied_transactions),
                         ('proof', proof)])

    blockchain.append(block)

    return True


def get_transaction_value():
    """ Ask the user and returns the input of the user (a new transaction amount) as a float. """
    tx_recipient = input("Who is the recipient of the transactions: ")
    tx_amount = float(input("The transaction amount: "))

    return tx_recipient, tx_amount


def get_user_action():
    """ Ask the user for the action and return it. """
    user_action = input("What do you want to do? ")
    return user_action


def print_blockchain_elements():
    """ Output all blocks of the blockchain. """
    for block in blockchain:
        print(f"\nPrinting the block: {block}")
    else:
        print("-" * 20)


def verify_chain():
    """ Verify the current blockchain and returns True / False """
    for (index, block) in enumerate(blockchain):
        # print(f"The index of the block: {index}")
        # print(f"The details of the block: {block}")
        if index == 0:
            continue

        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False

        # We use [:-1] on transcations to ignore the last transcation which is the 'mining' transaction
        if not valid_proof(block['transactions'][:-1], block['previous_hash'],
                           block['proof']):
            print('Proof of Work is invalid!')
            return False

        return True


def verify_transactions():
    """ Verifies all the open transactions. """
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_user_input = True

while waiting_for_user_input:
    print('\nPlease choose your actions:')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('5: Check transaction validity')
    print('h: Manipulate the chain')
    print('q: Quit')
    print('\n')

    user_choice = get_user_action()

    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data

        if add_transaction(recipient, amount=amount):
            print('Added transaction!')
        else:
            print('Transaction failed!')

        print(open_transactions)

    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()

    elif user_choice == '3':
        print_blockchain_elements()

    elif user_choice == '4':
        print(participants)

    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')

    # We do this action to check if we can verify the blockchain successfully when the user tries to manipulate one of the block
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash':
                '',
                'index':
                0,
                'transactions': [{
                    'sender': 'Chris',
                    'recipient': 'Sam',
                    'amount': 100.0
                }]
            }

    elif user_choice == 'q':
        waiting_for_user_input = False

    else:
        print('Input was invalid, please pick a value from the list!')

    if not verify_chain():
        print_blockchain_elements()
        print('The blockchain is invalid!')
        break

    print('Balance of {}: {:6.2f}'.format(owner, get_balance(owner)))
else:
    print('User left!')

print('Done!')
