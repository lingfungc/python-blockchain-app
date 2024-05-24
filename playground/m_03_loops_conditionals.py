def get_user_choice():
    return input("Your choice: ")


def get_user_input():
    return float(input("Please provide a new value: "))


def get_last_blockchain_value():
    if len(blockchain) > 0:
        return blockchain[-1]

    return None


def print_blocks():
    # * Create a "for loop" for a List
    for block in blockchain:
        print(f"Printing Block: {block}")
    else:
        print("-" * 30)


def add_transaction(tx_amount):
    blockchain.append([get_last_blockchain_value(), tx_amount])


def verify_chain():
    block_index = 0
    is_valid = True

    # for block in blockchain:
    #     if block_index == 0:
    #         block_index += 1
    #         continue
    #     if block[0] == blockchain[block_index - 1]:
    #         is_valid = True
    #     else:
    #         is_valid = False
    #         break
    #     block_index += 1

    for block_index in range(len(blockchain)):
        print(block_index)

        if block_index == 0:
            block_index += 1
            continue
        if blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
        block_index += 1

    return is_valid


blockchain = [[1]]

waiting_for_input = True

# * Create a "while loop" fo a Condition
while waiting_for_input:
    print("Please choose the action:")
    print("1. Add a new transcation value")
    print("2. Output the blockchain blocks")
    print("Q. Exit the program")

    user_choice = get_user_choice()

    if user_choice == "Q":
        waiting_for_input = False
    elif user_choice == "2":
        print_blocks()
    elif user_choice == "1":
        user_input = get_user_input()
        add_transaction(user_input)
    else:
        print("Invalid choice. Please pick a value from the list.")

    if not verify_chain():
        print("Invalid blockchain!")
        break
else:
    print("The loop is done!")

    # value = float(input("Please provide a new value: "))
    # blockchain.append([blockchain[-1], value])

    # value = float(input("Please provide a new value: "))
    # blockchain.append([blockchain[-1], value])

print("Finished")
