from uuid import uuid4

from blockchain import Blockchain
from verification import Verification


class Node:

    # Every Node Is Responsible for Its Own Blockchain
    def __init__(self):
        self.id = str(uuid4())
        self.blockchain = Blockchain(self.id)

    def get_transaction_value(self):
        """ Ask the user and returns the input of the user (a new transaction amount) as a float. """
        tx_recipient = input("Who is the recipient of the transactions: ")
        tx_amount = float(input("The transaction amount: "))

        return tx_recipient, tx_amount

    def get_user_action(self):
        """ Ask the user for the action and return it. """
        user_action = input("What do you want to do? ")
        return user_action

    def print_blockchain_elements(self):
        """ Output all blocks of the blockchain. """
        for block in self.blockchain.chain:
            print(f"\nPrinting the block: {block}")
        else:
            print("-" * 20)

    def run(self):
        waiting_for_user_input = True

        while waiting_for_user_input:
            print('\nPlease choose your actions:')
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            # print('4: Output participants')
            print('4: Check transaction validity')
            # print('h: Manipulate the chain')
            print('q: Quit')
            print('\n')

            user_choice = self.get_user_action()

            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data

                if self.blockchain.add_transaction(recipient,
                                                   self.id,
                                                   amount=amount):
                    print('Added transaction!')
                else:
                    print('Transaction failed!')

                print(self.blockchain.open_transactions)

            elif user_choice == '2':
                self.blockchain.mine_block()

            elif user_choice == '3':
                self.print_blockchain_elements()

            # elif user_choice == '4':
            #     print(participants)

            elif user_choice == '4':
                if Verification.verify_transactions(
                        self.blockchain.open_transactions,
                        self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')

            # We do this action to check if we can verify the blockchain successfully when the user tries to manipulate one of the block
            # elif user_choice == 'h':
            #     if len(blockchain) >= 1:
            #         blockchain[0] = {
            #             'previous_hash':
            #             '',
            #             'index':
            #             0,
            #             'transactions': [{
            #                 'sender': 'Chris',
            #                 'recipient': 'Sam',
            #                 'amount': 100.0
            #             }]
            #         }

            elif user_choice == 'q':
                waiting_for_user_input = False

            else:
                print('Input was invalid, please pick a value from the list!')

            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print('The blockchain is invalid!')
                break

            print('Balance of {}: {:6.2f}'.format(
                self.id, self.blockchain.get_balance()))
        else:
            print('User left!')

        print('Done!')


node = Node()
node.run()
