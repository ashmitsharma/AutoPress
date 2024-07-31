# AutoPress

AutoPress is a Python-based application for automating the process of publishing blog posts and web stories to a WordPress site. It fetches anime news, paraphrases the content, creates web stories, and publishes both the blog post and web stories to a WordPress site.

## Features

- Fetches the latest anime news from Anime News Network
- Summarizes and paraphrases content using various APIs
- Creates web stories from the content
- Publishes blog posts and web stories to a WordPress site
- Updates sitemap after publishing new stories


## Installation

1. Clone the repository:

    ```
    git clone https://github.com/yourusername/autopress.git
    cd autopress
    ```

2. Create and activate a virtual environment:

    ```
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the `autopress` directory with the following content:

    ```
    FTP_HOST=your_ftp_host
    FTP_USERNAME=your_ftp_username
    FTP_PASSWORD=your_ftp_password
    GOOGLE_API_KEY=your_google_api_key
    SUMMARIZER_API_KEY=your_summarizer_api_key
    PARAPHRASING_BY_HEALTHY_TECH_API_KEY=your_paraphrasing_by_healthy_tech_api_key
    PARAPHRASING_BY_NEURAL_NETWORK_API_KEY=your_paraphrasing_by_neural_network_api_key
    PLAGIARISM_REMOVER_BY_HEALTHY_TECH_API_KEY=your_plagiarism_remover_by_healthy_tech_api_key
    WORDPRESS_USERNAME=your_wordpress_username
    WORDPRESS_PASSWORD=your_wordpress_password
    ```

## Usage

To start the AutoPress application, simply run:

```
python main.py
```

The application will run in an infinite loop, fetching and publishing new content every 3 hours.

## Configuration
The configuration is handled via environment variables defined in the .env file. This includes FTP credentials, API keys, and WordPress credentials.

## Modules
### config/config.py
Loads environment variables from a .env file.

### utils/content_utils.py
Contains functions for fetching data, generating related keywords, and API calls for paraphrasing.

### utils/ftp_utils.py
Contains functions for uploading files and updating the sitemap via FTP.

### utils/summarizer_utils.py
Contains the function for summarizing content using the Summarizer API.

### utils/web_story_utils.py
Contains functions for creating web stories from content.

### utils/wordpress_utils.py
Contains functions for publishing content to a WordPress site.

### main.py
Main script that orchestrates the fetching, processing, and publishing of content.
