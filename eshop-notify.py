from module.eshop_notifier_db import *
from module.eshop_notifier_email import *
from module.eshop_prices_check import *
from module.eshop_prices_extension import *
import sys
import schedule
import time

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
            elif (line[0] == 'CHECK_PRICE_EVERY_X_MINUTE'):
                MINUTE_TO_REPEAT = line[2].replace('\'', '')
                MINUTE_TO_REPEAT = int(MINUTE_TO_REPEAT)
            elif (line[0] == 'CURRENCY'):
                CURRENCY = line[2].replace('\'', '')
except IOError:
    sys.exit('Environment file could not be found. Create env file using env_example.txt')

try:
    with open('assets/currency-code.txt', 'r', encoding="utf-8") as currency_code_file:
        for line in currency_code_file:
            if (line.split(',')[0] == CURRENCY):
                CURRENCY_SIGN = line.split(',')[1].strip()
                break
except IOError:
    sys.exit('Currency code file could not be found.  Ensure currency-code.txt exists at asset/currency-code.txt')


# Create main job
def job():
    eshop_notifier_db = EshopNotifierDB('config/watchlist.txt', 'config/pricelist.json')
    eshop_notifier_db.init_db()
    
    eshop_price_checker = EshopPricesCheck(eshop_notifier_db.db, eshop_notifier_db.db_query, 'config/watchlist.txt', CURRENCY, CURRENCY_SIGN)
    game_with_discount = eshop_price_checker.get_game_with_discount()

    eshop_prices_extension = EshopPricesExtension(CURRENCY, CURRENCY_SIGN)
    eshop_emailer = EshopNotifierEmail(SENDER_EMAIL, RECEIVER_EMAIL, SENDER_PASS)

    for game_url in game_with_discount:
        game_details = eshop_prices_extension.get_game_details(game_url)
        eshop_notifier_db.record_price(game_url, game_details['current_price'], eshop_notifier_db.db)

        with open('assets/email_template.html', 'r') as email_template:
            message = eshop_emailer.compose_message(email_template.read(), 
                                game_details['game_url'],
                                game_details['game_image_url'],
                                game_details['original_price'],
                                game_details['current_price'], 
                                game_details['game_desc'],
                                CURRENCY_SIGN)

            subject = eshop_emailer.compose_subject(game_details['game_title'])

            eshop_emailer.send_email(message, subject)

# Create scheduler to repeat script
schedule.every(MINUTE_TO_REPEAT).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)