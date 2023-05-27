from redmail import gmail

class EshopNotifierEmail:

    def __init__(self, SENDER_EMAIL: str, RECEIVER_EMAIL: str, SENDER_PASSWORD: str) -> None:
        self.__BASE_URL = "https://eshop-prices.com/"
        self.__SENDER_EMAIL = SENDER_EMAIL
        self.__RECEIVER_EMAIL = RECEIVER_EMAIL
        self.__SENDER_PASSWORD = SENDER_PASSWORD

    def send_email(self, message, subject):
        gmail.username = self.__SENDER_EMAIL
        gmail.password = self.__SENDER_PASSWORD

        gmail.send(
            subject=subject,
            receivers=self.__RECEIVER_EMAIL,
            html=message
        )

    def compose_message(self, message_template_html: str, 
                        game_url: str,
                        game_url_image: str,
                        original_price: float, 
                        discount_price: float,
                        game_desc: str, 
                        currency: str) -> str:

        discount_percent = round((((original_price - discount_price)/original_price) * 100), 2)

        message_html = message_template_html.replace('@game_url_image', game_url_image)
        message_html = message_html.replace('@discount_percent', "-" + (str(discount_percent) + "%"))
        message_html = message_html.replace('@original_price', currency + str(original_price))
        message_html = message_html.replace('@discount_price', currency + str(discount_price))  
        message_html = message_html.replace('@game_description', game_desc)
        message_html = message_html.replace('@game_url', f"{self.__BASE_URL}{game_url}")

        return message_html

    def compose_subject(self, game_title) -> str:
        return game_title.title() + ' from your eshop wishlist is now on sale!'