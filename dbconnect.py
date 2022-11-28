import pymongo as pymongo


def getDBConnection():

    username = "project_bdm113"
    password = "MongoDB"
    host = "cluster0.bbfew31.mongodb.net"

    try:
        conn = "mongodb+srv://%s:%s@%s/?retryWrites=true&w=majority" % (username, password, host)
        client = pymongo.MongoClient(conn)
        database = client["spotify"]
    except Exception as err:
        print(f"Unexpected error: {err}")
        database = None

    return database



