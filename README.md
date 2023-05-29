# eshop-prices.com game wishlist notifier

![image](https://github.com/wanhuz/eshop-notifier/assets/12682216/1b23d983-26c7-4d2f-87f6-e0216b75ce56)


## Overview

Eshop-notifier is a tool that alert user through email for game discount similar to Steam game wishlist. It can automatically check if there is any discount on user game wishlist and then send an email to user. 

## Features
- automatically check if there is any game on user wishlist that is on discount 
- send beautiful email to alert user on game discount

### Setup
For this application to work, you need have a gmail account to send email from.

Then create two file: 
- env.txt : used to store sensitive information such as your gmail username, password and sender email address, as well as extra settings. See example/env_template.txt.
- watchlist.txt : used to add or remove game that you want to be notitified. See example/watchlist_template.txt.

### Running with Docker Compose (Recommended)
To run the application using Docker Compose, use the following YAML configuration:

```yml
version: "3"
services:
  app:
    image: wanhuz/eshop-notify:latest
    container_name: eshop-notify
    restart: unless-stopped
    volumes:
      - /path/to/config:/usr/src/app/config
```

Change /path/to/config to your env.txt and wishlist.txt directory.

## Running with Python
This application is written and tested on Python 3.11.3

0. Ensure Python is installed
1. Create a folder named 'config' inside application directory
2. Create your env.txt and watchlist.txt and paste it inside the 'config' directory
3. Run 'pip install --upgrade Cython' from terminal/powershell
4. Run 'pip install --no-cache-dir -r requirements.txt' inside application directory
5. Execute the script 'python ./eshop-notify.py'

## Get gmail password for env.txt
How to generate SENDER_PASS for your gmail: 

0. Log in to your gmail account
1. Set up 2-step verification (if not already) at https://myaccount.google.com/u/1/security
2. Generate an App password:
    1. Go to your Google account
    2. Go to Security
    3. Go to 2-steps verification
    4. Go to App passwords
    5. Generate a new one (you may use custom app and give it a custom name)
    6. Copy app password and put it to SENDER_PASS in env.txt


### Important
- Some currency sign that is supposed to be suffix will be a prefix. For example, Swedish Krona.
- Only gmail is supported
  
## Special thanks
- Special thanks to hudsonbrendon for [eshop-prices.com API](https://github.com/hudsonbrendon/nintendo-eshop-prices)
