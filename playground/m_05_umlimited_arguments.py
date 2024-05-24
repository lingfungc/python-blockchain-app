def unlimited_arguments(*args, **dict_args):

    print(args)

    for argu in args:
        print(argu)

    print(dict_args)

    for k, v in dict_args.items():
        print(k, v)


unlimited_arguments(1, 2, 3, 4)
# Output: (1, 2, 3, 4)

print("\n")

unlimited_arguments(name="Sam", age=30)
# Output: name Sam
# Output: age 30
