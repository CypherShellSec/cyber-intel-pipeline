# Cyber Intel Pipeline
<img width="1536" height="768" alt="image" src="https://github.com/user-attachments/assets/9727c9f0-6e75-4c4a-87b3-fb8bb3b40c76" />

Daily pipeline of domestic and international news, vulns, PoCs, laws, etc.
This project uses rss feeds for various security news and threat intelligence websites, extracts article links, parses article body text, and then uses a local LLM for automated article summarization.

## 1. Install Ollama
```
curl -fsSL https://ollama.com/install.sh | sh
ollama pull mistral
```
(for Mistral 7B) or use your preferred model.

## 2. Prepare python virtual environment
```
cd /project/directory
python3 -m venv yourenvname
pip install requests feedparser beautifulsoup4 readability_lxml
```

## 3. Modify scripts for personal use
Change log file location and project location in bash script.

## 4. Set up cron job
`crontab -e`
Set cron schedule with text editor.
