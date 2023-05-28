from eshop_prices import EshopPrices
from tinydb import TinyDB, Query

eshop = EshopPrices(currency="MYR")

class EshopPricesCheck:

    def __init__(self, db, db_query, watchlist_filename) -> None:
        self.__db = db
        self.__db_query = db_query
        self.__watchlist_filename = watchlist_filename

    def lines_that_contain(string, fp):
        return [line for line in fp if string in line]


# Compare prices from two data, get game title if condition is fulfilled
    def get_game_below_target_price(self) -> list:
        game_below_min = []

        with open(self.__watchlist_filename, 'r') as reader:
            for line in reader:
                line = line.strip().split(',')

                # Watchlist.txt
                game_url = line[0]

                # Eshop-price.com
                eshop_data = eshop.get_prices_from_url(game_url)
                current_price = eshop_data[0]['price']['current_price'].replace("RM", "")
                current_price = float(current_price)
                original_price = eshop_data[0]['price']['original_price'].replace("RM", "")
                original_price = float(original_price)

                # Pricelist.json
                previous_price = self.__db.get(self.__db_query.game_url == game_url)['price']

                if(self.should_notify(current_price, original_price, previous_price)):
                    game_below_min.append(game_url)

        return game_below_min
    
    @staticmethod
    def should_notify(current_price, original_price, previous_price):
        if ((current_price < original_price) and (current_price < previous_price)):
            return True
        return False
    










