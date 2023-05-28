from module.eshop_notifier_db import *
from module.eshop_notifier_email import *
from module.eshop_prices_check import *
from module.eshop_prices_extension import *
import sys

# Read environment file
try:
    with open('config/env.txt', 'r') as env_file:
        RECEIVER_EMAIL = []
        for line in env_file:
            line = line.split(" ")

            if (line[0] == 'SENDER_EMAIL'):
                SENDER_EMAIL = line[2].strip().replace('\'', '')
            elif (line[0] == 'RECEIVER_EMAIL'):
                for receiver_email in line[2].strip().split(';'):
                    RECEIVER_EMAIL.append(receiver_email.replace('\'', ''))
            elif (line[0] == 'SENDER_PASS'):
                SENDER_PASS = line[2].replace('\'', '')
except IOError:
    sys.exit('Environment file could not be found. Create env file using env_example.txt')


# Program execution starts here
eshop_notifier_db = EshopNotifierDB('config/watchlist.txt', 'config/pricelist.json')
eshop_notifier_db.init_db()

eshop_price_checker = EshopPricesCheck(eshop_notifier_db.db, eshop_notifier_db.db_query, 'config/watchlist.txt')
game_with_discount = eshop_price_checker.get_game_with_discount()

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