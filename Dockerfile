# Use an official Python runtime as a parent image
FROM python:3.11.6

# Set the working directory in the container to /app
WORKDIR /app

# Add the requirment.txt file
ADD requirements.txt /app
# Add src directory
ADD src /app/src
# Add politicians.json file
ADD data/politicians.json /app/data/politicians.json

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run init script and then the scheduler scraping all the politicians tweets every 30 minutes
CMD python src/init.py && python src/main.py schedule-tweets-scraping 30