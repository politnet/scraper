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

## Add a politician

General data about the politicians is stored in `data/politicians.json` file. To add new politician to the file and the application run the following command:

```bash
python src/main.py -e [twitter_email] -u [twitter_username] -p [twitter_password] add-twitter-account [twitter_username] [politcal_party]
```

## Scrape tweets - all politicians

When required politicians are already added, you can scrape the tweets that will be saved in `data/tweets/{politician_twitter_account}.json`. To scrape tweets for all of the politicians from `data/politicians.json` file run the following command:

```bash
python src/main.py -e [twitter_email] -u [twitter_username] -p [twitter_password] scrape-tweets --limit [max_number_of_tweets] --batch-size [number_of_politicians_per_batch]
```

## Scrape tweets - one politician

Instead of all of the politician, if needed, only one can be scraped. As previously it will be saved in `data/tweets/{politician_twitter_account}.json`. Remember that the politician has to be present in `data/politicians.json` file. To start scraping run the following command:

```bash
python src/main.py -e [twitter_email] -u [twitter_username] -p [twitter_password] scrape-tweets --account-name [twitter_username] --limit [max_number_of_tweets] --batch-size [number_of_politicians_per_batch]
```
**Note**: Default `limit = math.inf` and `batch-size = 1`

## Schedule tweets scraping - all politicians

To schedule tweets scraping for all of the politicians from `data/politicians.json` file run the following command:

```bash
python src/main.py  -e [twitter_email] -u [twitter_username] -p [twitter_password] schedule-tweets-scraping --interval [interval_in_minutes] --limit [max_number_of_tweets] --batch-size [number_of_politicians_per_batch]
```

**Note**: Default `limit = math.inf` and `batch-size = 1`

## Build query description

This command builds the query ready to be insert for language models like e.g. ChatGPT offers. Query asks to update the description of the politician based on his current description and [--num-of-tweets] unprocessed tweets.

```bash
python src/main.py -e [twitter_email] -u [twitter_username] -p [twitter_password] build-query-description --num-of-tweets [num_of_tweets]
```

**Note**: Default `num-of-tweets = 25`