with open("example.txt", "w") as file:
    file.write("Hello, world!\n")
    file.write("This is my file.\n")


with open("example.txt", "r") as file:
    contents = file.read()
    print("---", contents, "---")

with open("example.txt", "r") as fileToRead:
    for line in fileToRead:
        print("---", line.strip(), "---")
