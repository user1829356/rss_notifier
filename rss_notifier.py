import feedparser
import datetime
import os
import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SENDER = ''
RECIPIENT = ''
SUBJECT = ''
SMTP = ''
PORT = 587
APP_PASSWORD = ''

# Add more feeds to fetch
FEEDS = {
    "NYT": 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    "BBC": 'http://feeds.bbci.co.uk/news/rss.xml',
}

# Add more keywords to look for
KEYWORDS = {"apple", "pearl", "lemon"}


TIMESTAMPS_FILE = 'timestamps.json'

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

def send_email(subject, message):

    msg = MIMEMultipart()
    msg['From'] = SENDER
    msg['To'] = RECIPIENT
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP(SMTP, PORT) as server:
            server.starttls()
            server.login(SENDER, APP_PASSWORD)
            server.send_message(msg)
        logging.info('Email sent successfully.')
    except Exception as e:
        logging.error(f'Failed to send email. Error: {str(e)}')

def load_timestamps():
    if os.path.exists(TIMESTAMPS_FILE):
        with open(TIMESTAMPS_FILE, 'r') as f:
            data = json.load(f)
            return {key: datetime.datetime.fromisoformat(value) for key, value in data.items()}
    return {}

def save_timestamps(timestamps):
    with open(TIMESTAMPS_FILE, 'w') as f:
        json_data = {key: value.isoformat() for key, value in timestamps.items()}
        json.dump(json_data, f, indent=4)

def get_news_from_feed(feed_url, feed_name, timestamps):
    last_time_checked = timestamps.get(feed_name, datetime.datetime.now() - datetime.timedelta(days=1))
    feed = feedparser.parse(feed_url)
    relevant_news = []

    if not feed.entries:
        return [], last_time_checked

    latest_timestamp = last_time_checked
    for entry in feed.entries:
        published_time = datetime.datetime(*entry.published_parsed[:6])

        if published_time > last_time_checked:
            for keyword in KEYWORDS:
                if keyword.lower() in entry.title.lower() or keyword.lower() in entry.description.lower():
                    relevant_news.append(entry)
                    if published_time > latest_timestamp:
                        latest_timestamp = published_time
                    break

    return relevant_news, latest_timestamp

def main():
    timestamps = load_timestamps()
    news_content = []  
    
    for feed_name, feed_url in FEEDS.items():
        news, latest_timestamp = get_news_from_feed(feed_url, feed_name, timestamps)
        if news:
            logging.info(f"Found new news from {feed_name}.")
            for item in news:
                news_content.append(f"New news from {feed_name}:")
                news_content.append(f"Title: {item.title}")
                news_content.append(f"Link: {item.link}")
                news_content.append(f"Description: {item.description}")
                news_content.append("------")

        timestamps[feed_name] = latest_timestamp

    if news_content:
        email_subject = SUBJECT
        email_body = "\n".join(news_content)
        send_email(email_subject, email_body)

    save_timestamps(timestamps)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        error_msg = str(e)
        logging.error(f"An error occurred: {error_msg}")
        send_email("Script Error Notification", error_msg)

