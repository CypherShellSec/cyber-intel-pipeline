# Cyber Intel Pipeline
Daily pipeline of domestic and international news, vulns, PoCs, laws, etc.
This project uses rss feeds for various security news and threat intelligence websites, extracts article links, parses article body text, and then uses a local LLM for automated article summarization.

## 1. Install Ollama
`curl -fsSL https://ollama.com/install.sh | sh`
`ollama pull mistral` (for Mistral 7B) or use your preferred model.

## 2. Prepare python virtual environment
`cd /project/directory`
`python3 -m venv yourenvname`
`pip install requests feedparser beautifulsoup4 readability_lxml`

## 3. Modify scripts for personal use
Change log file location and project location in bash script.

## 4. Set up cron job
`crontab -e`
Set cron schedule with text editor.
