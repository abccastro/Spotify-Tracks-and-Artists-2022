import pickle


def main():
    print("1. View Config")
    print("2. Add Config")
    print("3. Delete")

    while True:
        command = input("What do you want to do? ")

        config = readConfig()
        if command == "1":
            viewConfig(config)
        elif command == "2":
            addConfig(config)
        elif command == "3":
            delConfig(config)
        else:
            break


def viewConfig(config):
    for k, v in config.items():
        print(k, v)


def addConfig(config):
    name = input("Enter config name: ")
    value = input("Enter config value: ")

    config[name] = value
    saveConfig(config)


def delConfig(config):
    name = input("Enter config name: ")
    config.pop(name)
    saveConfig(config)


def saveConfig(config):
    with open("config", "wb") as input_file:
        pickle.dump(config, input_file)


def readConfig():
    try:
        with open("config", "rb") as output_file:
            config = pickle.load(output_file)
    except EOFError:
        config = {}
    except FileNotFoundError:
        print("File not found:", "accounts")
        config = None
    return config


main()
