from eshop_prices import EshopPrices
from tinydb import TinyDB, Query

eshop = EshopPrices(currency="MYR")

class EshopPricesCheck:

    def __init__(self, db, db_query, watchlist_filename) -> None:
        self.__db = db
        self.__db_query = db_query
        self.__watchlist_filename = watchlist_filename
        self.__BASE_URL = 'https://eshop-prices.com'

    def lines_that_contain(string, fp):
        return [line for line in fp if string in line]


# Compare prices from two data, get game title if condition is fulfilled
    def get_game_with_discount(self) -> list:
        games_with_discount = []

        with open(self.__watchlist_filename, 'r') as reader:
            for line in reader:
                line = line.strip().split(',')

                # Watchlist.txt
                game_url = line[0]
                game_url = game_url.replace(self.__BASE_URL, '')

                # Eshop-price.com
                eshop_data = eshop.get_prices_from_url(game_url)

                current_price = eshop_data[0]['price']['current_price'].replace("RM", "")
                current_price = float(current_price)
                original_price = eshop_data[0]['price']['original_price'].replace("RM", "")
                original_price = float(original_price)

                # Pricelist.json
                previous_price = self.__db.get(self.__db_query.game_url == game_url)['price']

                if(self.should_notify(current_price, original_price, previous_price)):
                    games_with_discount.append(game_url)

        return games_with_discount
    
    @staticmethod
    def should_notify(current_price, original_price, previous_price):
        if ((current_price < original_price) and (current_price < previous_price)):
            return True
        return False
    










