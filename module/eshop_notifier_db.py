from tinydb import TinyDB, Query

class EshopNotifierDB:

    def __init__(self, watchlist_filename: str, pricelist_filename : str) -> None:
        self.__HIGHEST_PRICE = 10000000
        self.__DB = TinyDB(pricelist_filename)
        self.__DB_QUERY = Query()
        self.__WATCHLIST_FILENAME = watchlist_filename

    @property
    def db(self) -> TinyDB:
        return self.__DB
    
    @property
    def db_query(self) -> Query:
        return self.__DB_QUERY
    
    @property
    def highest_price(self) -> int:
        return self.__HIGHEST_PRICE

    # Initialize pricelist records and add new url if its not added
    def init_db(self):
        db_query = Query()

        # Add new game detail to pricelist.json
        with open(self.__WATCHLIST_FILENAME, 'r') as reader:
            for line in reader:
                line = line.strip()           
                line = line.split(",")
                game_url = line[0].replace('\n','')

                if(len(self.db.search(db_query.game_url == game_url)) < 1):
                    self.db.insert({'game_url' : game_url, 'price' : self.__HIGHEST_PRICE})
                    
    '''
    Record price to prevent email notification from sending too often
        if current price is lower than previous price, overwrite previous price so user will notified only once for less than target price
        if current price is higher than previous price, reset previous price so that new discount will notify user
    '''
    def record_price(self, game_url, current_price, db):
        pricelist_query = Query()
        previous_price = db.get(pricelist_query.game_url == game_url)['price']

        if (current_price < previous_price):
            db.update({'price': current_price}, pricelist_query.game_url == game_url)
        elif (current_price > previous_price):
            db.update({'price': self.__HIGHEST_PRICE}, pricelist_query.game_url == game_url)