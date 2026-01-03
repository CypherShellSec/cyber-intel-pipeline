#!/bin/bash

# news_pipeline.sh
# Run your RSS → extract → summarize pipeline daily
TODAY="$(date +%Y-%m-%d)"
# Optional: Log everything for debugging
LOG_FILE="/log/file/location.log"

echo "==========================================" >> "$LOG_FILE"
echo "Pipeline started at $(date)" >> "$LOG_FILE"

# Change to the directory where your Python scripts live
cd /directory/for/project || {
    echo "ERROR: Could not cd to project directory" >> "$LOG_FILE"
    exit 1
}

# Activate your virtual environment (if you use one)
# Adjust to specific python virtual environment!!!
source .venv/bin/activate

# Run scripts one after another
echo "Step 1: Fetching new RSS links..." >> "$LOG_FILE"
python3 rssFeeder.py sources/sources.txt > "rssOutput/ro_$TODAY.txt" 2>> "$LOG_FILE" || {
    echo "ERROR in rssFeeder.py" >> "$LOG_FILE"
}

echo "Step 2: Extracting article bodies..." >> "$LOG_FILE"
python3 articleBody.py "rssOutput/ro_$TODAY.txt" -o "articleOutput/ao_$TODAY.json" 2>> "$LOG_FILE" || {
    echo "ERROR in articleBody.py" >> "$LOG_FILE"
}

echo "Step 3: Generating summaries with Ollama..." >> "$LOG_FILE"
python3 aiSummary.py "articleOutput/ao_$TODAY.json" -o "aiOutput/ai_$TODAY.txt" 2>> "$LOG_FILE" || {
    echo "ERROR in aiSumary.py" >> "$LOG_FILE"
}

echo "Pipeline finished at $(date)" >> "$LOG_FILE"
echo "==========================================\n" >> "$LOG_FILE"

echo "Daily news pipeline completed!"
