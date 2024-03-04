# Time to Read Telegram Bot in Python using pyTelegramBotAPI

## Introduction
The Time to Read Telegram Bot is designed to motivate and remind its followers to engage with reading regularly. Leveraging the pyTelegramBotAPI, it integrates with the Google Books API and MongoDB to offer features such as reminding followers to read at a specified time, providing a "BOOK OF THE DAY", suggesting "RANDOM BOOK", and enabling "SEARCH BOOK BY TITLE" functionalities.

## Features
- **Reminders**: Set reminders for followers to read at specific times.
- **Book of the Day**: Daily recommendations to expose readers to new literature.
- **Random Book**: Suggests a random book to users.
- **Search Book by Title**: Allows users to search for books specifically by title.

## Usage
**To interact with the bot, users can use the following commands within the Telegram app:**

- **/start** to begin interaction with the bot.
- **/help** for a list of available commands and functionalities.
- **/subscribe** to opt-in for daily reminders and book recommendations.
- **/unsubscribe** to opt-out of the reminders and recommendations.
- **/dailybook** to receive the book of the day.
- **/randombook** for a random book suggestion.
- **/search** to search for a book by its title.

## Installation
**To set up the Time to Read Telegram Bot, ensure you have Python installed on your machine and then install the necessary dependencies:**

```bash
pip install pyTelegramBotAPI pymongo requests
```

## Dependencies

**To run the "Time to Read Telegram Bot", you'll need the following dependencies installed:**

- Python 3.x
- pyTelegramBotAPI
- MongoDB
- pymongo
- requests
- threading (built-in with Python)
- datetime (built-in with Python)
- re (built-in with Python)
- random (built-in with Python)

## Configuration

**Before you can run the bot, you need to configure it with your own credentials. Replace the placeholder values in the script with your actual data:**

- `MONGODB_URI`: Replace `YOUR_MONGODB_URI` with the URI of your MongoDB instance.
- `TOKEN`: Replace `YOUR_TELEGRAMBOT_KEY` with your Telegram Bot API token.
- `GOOGLE_BOOKS_API`: Replace `YOUR_GOOGLE_BOOKS_KEY` with your Google Books API key.

These values are essential for connecting to your database, Telegram, and the Google Books API, enabling the bot's full functionality.


