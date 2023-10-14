# RSS Feed News Notifier 📰🚀

RSS Feed News Notifier is a Python script that monitors specified RSS feeds for news articles containing specific keywords and sends email notifications when new relevant articles are discovered.

## Prerequisites ✅

Before using this script, ensure you have the following prerequisites in place:

1. Python 3.x installed on your system.
2. Required Python libraries, which can be installed using pip:
   - `feedparser`
   - `datetime`
   - `os`
   - `json`
   - `logging`
   - `smtplib`
   - `email`

## Configuration ⚙️

Configure the script by setting the following variables in the script:

- `SENDER` 📧: Email address for sending notifications.
- `RECIPIENT` 📬: Email address for receiving notifications.
- `SUBJECT` 📨: Subject line for email notifications.
- `SMTP` 📤: SMTP server address (e.g., 'smtp.gmail.com' for Gmail).
- `PORT` 🌐: SMTP server port (e.g., 587 for Gmail).
- `APP_PASSWORD` 🔐: Application-specific password for your email account (if required).
- `FEEDS` 📡: Dictionary containing RSS feed names and their URLs.
    - For common feeds, visit https://about.fb.com/wp-content/uploads/2016/05/rss-urls-1.pdf
- `KEYWORDS` 🔍: Set of keywords used to filter relevant news articles.
- `TIMESTAMPS_FILE` 🕒: Name of the JSON file for storing timestamp information.

## Usage 🚀

1. Clone or download the script to your local machine.

2. Configure the script as described in the "Configuration" section.

3. Run the script with the following command:

   ```bash
   python3 rss_notifier.py

This will check the specified RSS feeds, send email notifications for newly discovered relevant articles, and update the timestamps file. For automatic usage, I recommend using `crontab`.

## Logging 📝

The script logs its activities to a file named app.log in the same directory. You can review this log to track the script's behavior and any errors that occur.

## Error Handling 🚨

In case of script errors, it will automatically send an email notification with details of the error.

## License 📜

This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to customize and enhance this script to suit your specific requirements! 🛠️✨
