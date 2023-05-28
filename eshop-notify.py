from module.eshop_notifier_db import *
from module.eshop_notifier_email import *
from module.eshop_prices_check import *
from module.eshop_prices_extension import *


'''
How to generate app password for your gmail: 

1. Set up 2-step verification (if not already) at https://myaccount.google.com/u/1/security
2. Generate an App password:
    a. Go to your Google account
    b. Go to Security
    c. Go to 2-steps verification
    d. Go to App passwords
    e. Generate a new one (you may use custom app and give it a custom name)
    f. Copy app password
'''
SENDER_EMAIL = '<SENDER EMAIL>'
SENDER_PASS = '<APP PASSWORD>'
RECEIVER_EMAIL = ['<RECEIVER ADDRESS 1', '<RECEIVER ADDRESS 2>']

eshop_notifier_db = EshopNotifierDB('watchlist.txt', 'pricelist.json')
eshop_notifier_db.init_db()

eshop_price_checker = EshopPricesCheck(eshop_notifier_db.db, eshop_notifier_db.db_query, 'watchlist.txt')
game_with_discount = eshop_price_checker.get_game_below_target_price()

eshop_prices_extension = EshopPricesExtension()
eshop_emailer = EshopNotifierEmail(SENDER_EMAIL, RECEIVER_EMAIL, SENDER_PASS)

for game_url in game_with_discount:
    game_details = eshop_prices_extension.get_game_details(game_url)
    eshop_notifier_db.record_price(game_url, game_details['current_price'], eshop_notifier_db.db)

    with open('email_template.html', 'r') as email_template:
        message = eshop_emailer.compose_message(email_template.read(), 
                            game_details['game_url'],
                            game_details['game_image_url'],
                            game_details['original_price'],
                            game_details['current_price'], 
                            game_details['game_desc'],
                            "RM")

        subject = eshop_emailer.compose_subject(game_details['game_title'])

        eshop_emailer.send_email(message, subject)