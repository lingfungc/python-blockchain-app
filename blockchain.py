import functools
import os
import json
# import pickle
# from collections import OrderedDict

from block import Block
from transaction import Transaction
from verification import Verification
from hash_util import hash_string_256, hash_block

# Reward to Miners (For Creating a New Block)
MINING_REWARD = 10

# Pre-Built First Starting Block for the Blockchain
# genesis_block = {
#     'previous_hash': '',
#     'index': 0,
#     'transactions': [],
#     'proof': 100
# }

# # Initialising the Blockchain List
# blockchain = [genesis_block]
# blockchain = []

# # Open Transacations (Unhandled Transactions before Being Put into the Blockchain)
# open_transactions = []

# Our Identifier (The Owner of this Blockchain Node) E.g. For Sending Coins ...
# owner = "Sam"

# Data Type: Set (No Duplicates) - Registered Participants: Owner + Other People Involved in Sending + Receiving Coins
# participants = {'Sam'}


class Blockchain:

    def __init__(self, hosting_node_id):
        # Starting Block for the Blockchain
        # Pre-Built First Starting Block for the Blockchain
        genesis_block = Block(0, '', [], 100, 0)

        # Initializing (empty) Blockchain List
        self.chain = [genesis_block]

        self.open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

    def load_data(self):
        """
        Read the blockchain and open_transactions data from the 'blockchain.txt'.

        We use 'readlines()' to get the data in a list format.

        We need to use 'json.loads()' to make sure the json-string data is loaded as a Python object.

        We need to us 'global' to let the function to know that these are global variables.

        We need to handle 'OrderedDict' for the data and load the data as 'OrderedDict' (only for transactions).

        We execute this 'load_data()' right after we define this and at the begining of this Python file.
        """
        try:
            if os.path.exists('blockchain.txt'):
                with open('blockchain.txt', mode='r') as f:
                    file_content = f.readlines()

                    blockchain = json.loads(file_content[0][:-1])

                    updated_blockchain = []

                    for block in blockchain:

                        converted_txs = [
                            Transaction(tx['sender'], tx['recipient'],
                                        tx['amount'])
                            for tx in block['transactions']
                        ]

                        updated_block = Block(block['index'],
                                              block['previous_hash'],
                                              converted_txs, block['proof'],
                                              block['timestamp'])

                        updated_blockchain.append(updated_block)

                    blockchain = updated_blockchain

                    open_transactions = json.loads(file_content[1])

                    updated_transactions = []

                    for tx in open_transactions:

                        updated_transaction = Transaction(
                            tx['sender'], tx['recipient'], tx['amount'])

                        updated_transactions.append(updated_transaction)

                    open_transactions = updated_transactions
            else:
                raise IOError
        except (IOError, IndexError):
            # * Ww now handle the IOError (when file not found) by creating the genesis_block in the 'except' block
            # * We also handle the IndexError (when the index is out of range)
            pass
        finally:
            # print(blockchain)
            print("Clean up!")

    def save_data(self):
        """
        Save the blockchain data into a file (Always Overwrite).

        We call this 'save_data()' whenever we add a new transaction or mine a new block.

        We use 'json.dumps()' to save the data as a json-string into the file.

        We can also use 'pickle.dumps()' to save the data as a Binary data in the file.

        Note that we save_data in a 'OrderedDict' (only for transactions).
        """
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [
                    block.__dict__ for block in [
                        Block(block_el.index, block_el.previous_hash,
                              [tx.__dict__ for tx in block_el.transactions],
                              block_el.proof, block_el.timestamp)
                        for block_el in self.chain
                    ]
                ]
                f.write(json.dumps(saveable_chain))

                f.write('\n')

                saveable_txs = [tx.__dict__ for tx in self.open_transactions]

                f.write(json.dumps(saveable_txs))

            # with open('blockchain.p', mode='wb') as f:
            #     save_data = {
            #         'blockchain': blockchain,
            #         'open_transactions': open_transactions
            #     }
            #     f.write(pickle.dumps(save_data))
        except (IOError, IndexError):
            print("Failed to save the data!")

    def proof_of_work(self):
        last_block = self.chain[-1]
        last_hash = hash_block(last_block)
        proof = 0

        while not Verification.valid_proof(self.open_transactions, last_hash,
                                           proof):
            proof += 1

        return proof

    def get_balance(self):
        """
        Calculate and return the balance for a participant.

        Arguments:
            :participant: The person for whom to calculate the balance.
        """
        participant = self.hosting_node

        # Find all the transactions (amount of coins) for the transactions that the participant is the sender (sending out coins) in the Blockchain
        tx_sending = [[
            tx.amount for tx in block.transactions if tx.sender == participant
        ] for block in self.chain]

        # Find all the transactions (amount of coins) for the transactions that the participant is the sender (sending out coins) in the Blockchain
        open_tx_sending = [
            tx.amount for tx in self.open_transactions
            if tx.sender == participant
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
            tx.amount for tx in block.transactions
            if tx.recipient == participant
        ] for block in self.chain]

        amount_received = functools.reduce(
            lambda tx_sum, tx: tx_sum + sum(tx)
            if len(tx) > 0 else tx_sum + 0, tx_receiving, 0)

        # amount_received = 0

        # for tx in tx_receiving:
        #     if len(tx) > 0:
        #         amount_received += tx[0]

        return amount_received - amount_sent

    def get_last_transaction_value(self):
        """ Returns the last value of the current blockchain. """
        if len(self.chain) < 1:
            return None
        return self.chain[-1]

    def add_transaction(self, recipient, sender, amount=1.0):
        """
        Append a new value as well as the last blockchain value to the open transactions.

        Arguments:
            :sender: The participant who is sending out the coins.
            :recipient: The participant who is receiving the coins.
            :amount: The amount of the coins sent with the transaction (default value = 1.0)
        """
        # transaction = OrderedDict([('sender', sender), ('recipient', recipient),
        #                            ('amount', amount)])

        transaction = Transaction(sender, recipient, amount)

        if Verification.verify_transaction(transaction, self.get_balance):
            self.open_transactions.append(transaction)
            # participants.add(sender)
            # participants.add(recipient)

            self.save_data()

            return True
        return False

    def mine_block(self):
        """ Create a NEW block and add open transactions to the block. """
        # last_block = get_last_transaction_value()
        last_block = self.chain[-1]

        hashed_block = hash_block(last_block)

        proof = self.proof_of_work()

        # We need to make sure the hash always has the same order for the data to prevent hashing error
        # reward_transaction = {
        #     'sender': "MINING",
        #     'recipient': owner,
        #     'amount': MINING_REWARD,
        # }

        # reward_transaction = OrderedDict([('sender', 'MINING'),
        #                                   ('recipient', owner),
        #                                   ('amount', MINING_REWARD)])

        reward_transaction = Transaction("MINING", self.hosting_node,
                                         MINING_REWARD)

        # Create a NEW copy of the transaction instead of manipulating the original open_transaction list
        # To ensure that if the mining is failed by some reasons, we won't reward transaction stored in the open transactions
        copied_transactions = self.open_transactions[:]
        copied_transactions.append(reward_transaction)

        # block = {
        #     'previous_hash': hashed_block,
        #     'index': len(blockchain),
        #     'transactions': copied_transactions,
        #     'proof': proof
        # }

        # block = OrderedDict([('previous_hash', hashed_block),
        #                      ('index', len(blockchain)),
        #                      ('transactions', copied_transactions),
        #                      ('proof', proof)])

        block = Block(len(self.chain), hashed_block, copied_transactions,
                      proof)

        self.chain.append(block)

        self.open_transactions = []
        self.save_data()

        return True
