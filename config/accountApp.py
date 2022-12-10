"""
CREATE ACCOUNT FOR DEVICE MANAGEMENT
"""
import pickle


def main():
    print("1. View Accounts")
    print("2. Add Account")
    print("3. Delete Account")

    while True:
        command = input("What do you want to do? ")

        accounts = readAccount()
        if command == "1":
            viewAccounts(accounts)
        elif command == "2":
            createAccount(accounts)
        elif command == "3":
            deleteAccount(accounts)
        else:
            break


def viewAccounts(accounts):
    for account in accounts:
        print(account[0], account[1])


def createAccount(accounts):
    name = input("Enter username: ")
    password = input("Enter password: ")

    account = [name, password]
    accounts.append(account)
    saveAccount(accounts)
    print(f"{name} is added")

def deleteAccount(accounts):
    name = input("Enter username: ")
    idx = [idx for idx, a in enumerate(accounts) if accounts[idx][0] == name]

    accounts.pop(idx[0])
    saveAccount(accounts)
    print(f"{name} is deleted")

def saveAccount(accounts):
    with open("accounts", "wb") as input_file:
        pickle.dump(accounts, input_file)


def readAccount():
    try:
        with open("accounts", "rb") as output_file:
            accounts = pickle.load(output_file)
    except EOFError:
        accounts = []
    except FileNotFoundError:
        print("File not found:", "accounts")
        accounts = None
    return accounts


main()
