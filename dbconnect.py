import pickle

import pymongo as pymongo


def getDBConnection():

    try:
        with open("config", "rb") as output_file:
            config = pickle.load(output_file)

        conn = "mongodb+srv://%s:%s@%s/?retryWrites=true&w=majority" % (config["db_username"],
                                                                        config["db_password"],
                                                                        config["db_host"])
        client = pymongo.MongoClient(conn)
        database = client["spotify"]

    except FileNotFoundError as err:
        print(f"Missing config file: {err}")
    except Exception as err:
        print(f"Unexpected error: {err}")
        database = None

    return database
