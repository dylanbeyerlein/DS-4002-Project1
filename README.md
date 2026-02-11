# DS-4002-Project1
UVA DS 4002 Group 4 - Project 1 (text data)

## Software and Platform
Type(s) of software used: GitHub, bag-of-words model [1]

Necessary add-on packages: pandas, re, nltk, from nltk.corpus import stopwords, from nltk.stem import WordNetLemmatizer

The platform: Windows/ Mac

## Map of Documentation

```
UVA_DS_4002_Group_4_Project_1_text_data/
│
├── DATA/
│   ├── News_Uncleaned.csv
│   ├── News_Cleaned.csv
│   ├── Opinion_Uncleaned.csv
│   └── Opinion_Cleaned.csv
│
├── OUTPUT/
│   ├── figures_news_top10.png
│   ├── opinion_top10.png
│   └── word_frequency_table.csv
│
├── SCRIPTS/
│   ├── Analysis.ipynb
│   ├── Cleaning.ipynb
│   ├── extract_articles.py
│   └── mi2ds4002.py
│
├── LICENSE
├── README.md
└── requirements.txt

```

## Instructions for Reproducing Results
Clone the GitHub repository and download the csv files containing the dataset. Run the Cleaning.ipynb and Analysis.ipynb and jupyter notebook scripts found within the SCRIPTS folder. Compare the generated results with the results within the OUTPUT folder. Our results (in the form of bar charts) reveal…
- The top 10 most frequent words in news article titles are: student, uva, committee, university, council, board, discus, honor, new, archive
- The top 10 most frequent words in opinion article titles are: editorial, uva, student, parting, shot, virginia, must, letter, university, kurtzweil
- A two column chart containing the numeric frequency counts of the 26 most common words in the News and Opinion articles.
- Below are our statistics:
   - Chi-square statistic: 438.90
   - Degrees of freedom: 24
   - P-value: 0.000000


## References
[1] 262588213843476. “NLTK’s List of English Stopwords.” Gist, 27 Aug. 2010, gist.github.com/sebleier/554280.
