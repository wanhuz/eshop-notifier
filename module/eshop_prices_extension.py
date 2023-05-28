import bs4
import requests
from eshop_prices import EshopPrices

class EshopPricesExtension:
    def __init__(self, currency, currency_sign) -> None:
        self.__BASE_URL = "https://eshop-prices.com/"
        self.__CURRENCY = currency
        self.__CURRENCY_SIGN = currency_sign

    @property
    def base_url(self) -> str:
        return self.__BASE_URL
    
    @property
    def headers(self) -> str:
        return {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0"}

    def get_url_image_from_url(self, game_url: str) -> str:
        request_url = f"{self.base_url}{game_url}"
        response = requests.get(
            request_url,
            headers=self.headers,
        )

        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.text, "lxml")

            url_image = soup.find_all("source", {"type": "image/jpeg"})[0]
            url_image = url_image['srcset'].split(',')[3].replace(' 480w', '').strip()

            return url_image
        return f"Error getting image url from url! (Status = {response.status_code})"

    def get_description_from_url(self, game_url: str) -> str:
        request_url = f"{self.base_url}{game_url}"
        response = requests.get(
            request_url,
            headers=self.headers,
        )

        if response.status_code == 200:
            soup = bs4.BeautifulSoup(response.text, "lxml")

            game_description = soup.find_all("p", {"class": "game-description"})[0]
            game_description = game_description['title']

            return game_description
        return f"Error getting game description from url! (Status = {response.status_code})"
    
    def get_game_details(self, game_url : str) -> list:
        eshop = EshopPrices(self.__CURRENCY)
        eshop_data = eshop.get_prices_from_url(game_url)

        game_title = game_url
        game_title = game_title[game_title.index("-") + 1:]
        game_title = game_title.replace('-', ' ').capitalize()

        current_price = eshop_data[0]['price']['current_price'].replace(self.__CURRENCY_SIGN, "")
        current_price = float(current_price.replace(',','.'))

        original_price = eshop_data[0]['price']['original_price'].replace(self.__CURRENCY_SIGN, "")
        original_price = float(original_price.replace(',' , '.'))        

        game_details = {'game_title': game_title, 
                        'game_url': game_url,
                        'game_image_url' : self.get_url_image_from_url(game_url),
                        'game_desc' : self.get_description_from_url(game_url),
                        'current_price' : current_price,
                        'original_price' : original_price}
        
        return game_details