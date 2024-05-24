blockchain = [[1]]


# * Return the Last Element in an Array
def get_last_backchain_value():
    return blockchain[-1]


# * Add a New Element in an Array
def add_value(transaction_amount):
    """ Multiple Line Comment Reference:

        Append a new value as well as the last blockchain value to the blockchain

        Arguments:
            :transaction_amount: The amount that should be added.
            :last_transcation: The last blockchain transaction (default [1])
    """
    blockchain.append([get_last_backchain_value(), transaction_amount])


# * Ask for User Input + Convert a String into a Float
def get_user_input():
    return float(input("Your transaction amount please: "))


# * Reuse a Function
tx_amount = get_user_input()
add_value(tx_amount)

tx_amount = get_user_input()
add_value(tx_amount)

tx_amount = get_user_input()
add_value(tx_amount)

print(blockchain)


# * Set a Default Value for a Function Argument
def greet(name, age=33):
    print(f"Hello {name}. I am {age} year old.")


greet(name="Chris")
greet("Joe", age=66)
greet(age=44, name="Martin")

# * Access + Update a Global Variable inside Function Scope
name = "Max"


def get_name():
    global name
    name = input("Update your name: ")


get_name()
print(name)
