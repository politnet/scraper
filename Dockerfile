# Use an official Python runtime as a parent image
FROM python:3.11.6

# Set the working directory in the container to /app
WORKDIR /app

# Add the requirment.txt and src directory contents into the container at /app
ADD requirements.txt /app
ADD ./src /app/src

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run init script and then the scheduler scraping all the politicians tweets every 30 minutes
CMD python src/init.py && python src/main.py -e $TWITTER_EMAIL_ENV -u $TWITTER_USERNAME_ENV -p $TWITTER_PASSWORD_ENV schedule-tweets-scraping 30