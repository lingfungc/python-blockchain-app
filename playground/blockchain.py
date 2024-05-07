blockchain = [[1]]


def get_last_backchain_value():
    return blockchain[-1]


def add_value(transaction_amount):
    blockchain.append([get_last_backchain_value(), transaction_amount])


add_value(11)
add_value(33)
add_value(55)

print(blockchain)


def greet(name, age=33):
    print(f"Hello {name}. I am {age} year old.")


greet(name="Chris")
greet("Joe", age=66)
greet(age=44, name="Martin")
