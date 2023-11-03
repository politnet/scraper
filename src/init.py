import globals
import os 

print("Initializing...")

# Create 'data' directory if it doesn't exist
if not os.path.exists(globals.DATA_DIRECTORY):
    print(f"Creating {globals.DATA_DIRECTORY} directory...")
    os.makedirs(globals.DATA_DIRECTORY)
    
# Create 'data' directory if it doesn't exist
if not os.path.exists(globals.TWEETS_DIRECTORY):
    print(f"Creating {globals.TWEETS_DIRECTORY} directory...")
    os.makedirs(globals.TWEETS_DIRECTORY)
    
# Create 'data' directory if it doesn't exist
if not os.path.exists(globals.LOGS_DIRECTORY):
    print(f"Creating {globals.LOGS_DIRECTORY} directory...")
    os.makedirs(globals.LOGS_DIRECTORY)
    
# Create json file with politicians if it doesn't exist
if not os.path.exists(globals.POLITICIANS_FILE):
    print(f"Creating {globals.POLITICIANS_FILE} file...")
    with open(globals.POLITICIANS_FILE, 'w') as f:
        f.write("{}")

print("Done.")