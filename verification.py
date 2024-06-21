from hash_util import hash_string_256, hash_block


class Verification:

    @staticmethod
    def valid_proof(transcations, last_hash, proof):
        # Order in the Transactions is important here because we are going to do hashing
        # guess = (str(transcations) + str(last_hash) + str(proof)).encode()
        guess = (str([tx.to_ordered_dict() for tx in transcations]) +
                 str(last_hash) + str(proof)).encode()

        guess_hash = hash_string_256(guess)

        # print(f'valid_proof(): {guess_hash}')
        # print(f'valid_proof(): {guess_hash[0:2]}')

        return guess_hash[0:2] == '00'

    @classmethod
    def verify_chain(cls, blockchain):
        """ Verify the current blockchain and returns True / False """
        for (index, block) in enumerate(blockchain):
            # print(f"The index of the block: {index}")
            # print(f"The details of the block: {block}")
            if index == 0:
                continue

            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False

            # We use [:-1] on transcations to ignore the last transcation which is the 'mining' transaction
            if not cls.valid_proof(block.transactions[:-1],
                                   block.previous_hash, block.proof):
                print('Proof of Work is invalid!')
                return False

            return True

    @staticmethod
    def verify_transaction(transactiion, get_balance):
        """
        Verify a transaction by checking whether the sender has enough / sufficient coins.

        Arguments:
            :transaction: The transaction that should be verified.
        """
        sender_balance = get_balance()

        # print(f'verify_transcation::sender_balance:: {sender_balance}')
        # print(f"verify_transcation::transcation_amount:: {transactiion['amount']}")

        return sender_balance >= transactiion.amount

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        """ Verifies all the open transactions. """
        return all([
            cls.verify_transaction(tx, get_balance) for tx in open_transactions
        ])
