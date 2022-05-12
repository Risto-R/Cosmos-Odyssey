from CosmosOdyssey import app
from CosmosOdyssey.Config import Config

if __name__ == "__main__":
    from CosmosOdyssey.FlightDataAPI import updateDatabase
    import threading
    t = threading.Thread(target=updateDatabase)
    t.start()
    app.run(port=Config.PORT)
    t.join()
