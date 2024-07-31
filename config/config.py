import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# FTP credentials
FTP_HOST = os.getenv('FTP_HOST')
FTP_USERNAME = os.getenv('FTP_USERNAME')
FTP_PASSWORD = os.getenv('FTP_PASSWORD')

# API keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
# Get API key on https://rapidapi.com/aryanchaurasia348-D-e9g9-G_m/api/summarizer8
SUMMARIZER_API_KEY = os.getenv('SUMMARIZER_API_KEY')
# Get API key on https://rapidapi.com/healthytechguy/api/paraphrasing-tool1
PARAPHRASING_BY_HEALTHY_TECH_API_KEY = os.getenv('PARAPHRASING_BY_HEALTHY_TECH_API_KEY')
# Get API key on https://rapidapi.com/neuralwriter-neuralwriter-default/api/paraphrasing-and-rewriter-api
PARAPHRASING_BY_NEURAL_NETWORK_API_KEY = os.getenv('PARAPHRASING_BY_NEURAL_NETWORK_API_KEY')
# Get API key on https://rapidapi.com/healthytechguy/api/plagiarism-remover
PLAGIARISM_REMOVER_BY_HEALTHY_TECH_API_KEY = os.getenv('PLAGIARISM_REMOVER_BY_HEALTHY_TECH_API_KEY')


# WordPress credentials
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')
