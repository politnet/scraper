# Build image from Dockerfile called polinet-scraper
docker build -t polinet-scraper .

# Run docker compose in detached mode
docker-compose up -d