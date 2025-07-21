# mdm-deck-crawler

# Overview
This is an automated scraper for collecting deck data from the Top Decks section of Master Duel Meta.
Due to the structure of the website, the scraper works by automatically clicking the "Saved as YDK file" button on each individual deck page to retrieve the data.

# Usage
Simply run main.py to start the scraping process.
You can adjust the scraping range by modifying the start_page and end_page variables in the script.

# Notes
1. The number of decks visible is limited for non-members. If needed, please log into your account on the automated browser before starting the scraping process.
2. Network instability may cause interruptions during scraping.
