# Use an official Python runtime as a parent image
FROM python:3.11.6

# Set the working directory in the container to /app
WORKDIR /app

# Add the requirment.txt and src directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run your script when the container launches
CMD python src/init.py && python src/main.py -e $TWITTER_EMAIL -u $TWITTER_USERNAME -p $TWITTER_PASSWORD schedule-tweets-scraping 30