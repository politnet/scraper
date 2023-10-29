# Polinet

Application to scrape and process tweets of the politicians.

## Install and init

To install required packages run:

```bash
pip install -r requirements.txt
```

Then to create necessary directories (`data` and `data/tweets`) and files (`data/politicians.json`) for the application run:

```bash
python src/init.py
```

## Login

Application can be used with (`account-login`) or without (`guest-session`) twitter account, it is described later how to choose it. Generally using `account-login` enable you to get more detailed data from twitter. It is likely that you will encounter the rate limits at some point.

## Add a new twitter account

General data about the politicians is stored in `data/politicians.json` file. To add new politician to the file and the application run the following command:

```bash
python src/main.py guest-session add-twitter-account [twitter_username]
```

or using your twitter account run the following command:

```bash
python src/main.py account-login -e [twitter_email] -u [twitter_username] -p [twitter_password] add-twitter-account [twitter_username]
```

## Scrape tweets - all politicians

When required politicians are already added, you can scrape the tweets that will be saved in `data/tweets/{politician_twitter_account}.json`. To scrape tweets for all of the politicians from `data/politicians.json` file run the following command:

```bash
python src/main.py guest-session scrape-tweets
```

or using your twitter account run the following command:

```bash
python src/main.py account-login -e [twitter_email] -u [twitter_username] -p [twitter_password] scrape-tweets
```

## Scrape tweets - one politician

Instead of all of the politician, if needed only one can be scraped. As previously it will be saved in `data/tweets/{politician_twitter_account}.json`. Remember that the politician has to be present in `data/politicians.json` file. To start scraping run the following command:

```bash
python src/main.py guest-session scrape-tweets --account-name [twitter_username]
```

or using your twitter account run the following command:

```bash
python src/main.py account-login -e [twitter_email] -u [twitter_username] -p [twitter_password] scrape-tweets --account-name [twitter_username]
```

**Note:** Using `account-login` will enable you to scrape more tweets than using `guest-session`.

## Schedule tweets scraping - all politicians

To schedule tweets scraping for all of the politicians from `data/politicians.json` file run the following command:

```bash
python src/main.py guest-session schedule-tweets-scraping --interval [interval_in_minutes]
```

or using your twitter account run the following command:

```bash
python src/main.py account-login -e [twitter_email] -u [twitter_username] -p [twitter_password] schedule-tweets-scraping --interval [interval_in_minutes]
```

**Note:** Using `account-login` will enable you to scrape more tweets than using `guest-session`.

## Build query description

This command builds the query ready to be insert for language models like e.g. ChatGPT offers. Query asks to update the description of the politician based on his current description and [--num-of-tweets] unprocessed tweets.

```bash
python src/main.py guest-session build-query-description --num-of-tweets [num_of_tweets]
```

or using your twitter account run the following command:

```bash
python src/main.py account-login -e [twitter_email] -u [twitter_username] -p [twitter_password] build-query-description --num-of-tweets [num_of_tweets]
```