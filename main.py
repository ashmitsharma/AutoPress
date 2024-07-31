import os
import time
import logging
import multiprocessing
from config.config import *
from utils.ftp_utils import upload_file, update_sitemap
from utils.web_story_utils import create_web_story_html, get_cover_image, search_images, remove_special_characters
from utils.wordpress_utils import publish_on_website
from utils.summarizer_utils import summarize
from utils.content_utils import get_data, get_related_keywords, choose_random_pickup_line, api_call

def get_images(title):
    try:
        images = []
        images.append(get_cover_image(title))
        images.extend(search_images(title, GOOGLE_API_KEY))
        return images
    except:
        images = search_images(title, GOOGLE_API_KEY)
        return images

def post_web_story(title, content):
    try:
        ftp_host, ftp_username, ftp_password = FTP_HOST, FTP_USERNAME, FTP_PASSWORD
        file_name = remove_special_characters(title) + ".html"
        path_with_filename = path + file_name
        images = get_images(title)
        if len(images) != 0:
            points = summarize(content)
            html_code = create_web_story_html(title, points, images, file_name)
            with open(path_with_filename, "w") as file:
                file.write(html_code)
                file.close()
            upload_file(path_with_filename, file_name, ftp_host, ftp_username, ftp_password)
            update_sitemap(file_name, ftp_host, ftp_username, ftp_password, path)
            os.remove(path_with_filename)
            logging.info("Webstory Posted")
        else:
            logging.info("Web Story Not Posted Due No Images were found")
    except Exception as e:
        logging.info(f"Web Story Not Posted Due to: {e}")

def post():
    try:
        with open(previous_titles_file_path, 'r') as title_file:
            saved_titles = title_file.read().split('~')

        news_data = get_data()

        if news_data[0][0] not in saved_titles:
            title = news_data[0][0]
            keywords = get_related_keywords(news_data[0][0])
            img_url = news_data[2][0]
            new_rewritten_content = api_call(news_data[3][0])

            post_web_story(title, new_rewritten_content)

            additional_content = choose_random_pickup_line()
            new_rewritten_content = str(new_rewritten_content) + additional_content

            publish_on_website(title, img_url, new_rewritten_content, keywords, image_path)

            with open(previous_titles_file_path, 'w') as article_file:
                for title in news_data[0]:
                    article_file.write(f"{title}~")
        else:
            logging.info("No New Article Found")
    except FileNotFoundError:
        news_data = get_data()
        with open(previous_titles_file_path, 'w') as article_file:
            for title in news_data[0]:
                article_file.write(f"{title}~")
        title = news_data[0][0]
        keywords = get_related_keywords(news_data[0][0])
        img_url = news_data[2][0]
        new_rewritten_content = api_call(news_data[3][0], api_call_record_file_path)

        additional_content = choose_random_pickup_line()
        new_rewritten_content = str(new_rewritten_content) + additional_content

        publish_on_website(title, img_url, new_rewritten_content, keywords, image_path)

def execute_post():
    while True:
        post()
        time.sleep(3 * 60 * 60)

if __name__ == '__main__':
    path = "/home/ash/oniichan_blog/"
    log_file_path = "/home/ash/oniichan_blog/anime_blog_app.log"
    image_path = "/home/ash/oniichan_blog/images/image.jpg"
    api_call_record_file_path = "/home/ash/oniichan_blog/api_counter.txt"
    previous_titles_file_path = "/home/ash/oniichan_blog/articles_title.txt"

    logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    process = multiprocessing.Process(target=execute_post)
    process.start()
    process.join()
