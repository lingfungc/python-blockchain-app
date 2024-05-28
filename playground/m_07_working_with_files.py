# Create + Write File
file = open('demo.txt', mode='w')

file.write('Hello from Python!')

file.close()

# Read Data from a File
file = open('demo.txt', mode='r')

file_content = file.read()

file.close()

print(file_content)
