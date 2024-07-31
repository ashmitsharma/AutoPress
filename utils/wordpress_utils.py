import os
import requests
import shutil
from datetime import datetime
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from wordpress_xmlrpc.methods import media
from wordpress_xmlrpc.compat import xmlrpc_client
import logging
from ..config.config import *


def publish_on_website(title, thumbnail_url, content, keywords, image_path):
    try:
        url = 'https://oniichan.in/xmlrpc.php'
        username = WORDPRESS_USERNAME
        password = WORDPRESS_PASSWORD
        client = Client(url, username, password)

        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = 'publish'
        post.terms_names = {
            'category': ['Anime News'],
            'post_tag': keywords
        }

        if os.path.exists(image_path):
            os.remove(image_path)
        response = requests.get(thumbnail_url, stream=True)
        with open(image_path, "wb") as file:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, file)
            file.close()

        mime_type = response.headers['Content-Type']
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d-%H-%M-%S")
        upload_image_dict = {
            'name': f"blog_image_{formatted_datetime}_oniichan-in.jpg",
            'type': mime_type,
        }

        with open(image_path, 'rb') as img:
            upload_image_dict['bits'] = xmlrpc_client.Binary(img.read())
            img.close()

        resp = client.call(media.UploadFile(upload_image_dict))
        image_id = resp['id']
        post.thumbnail = image_id

        client.call(NewPost(post))
        log_msg = f"Article: {title}. Posted Successfully"
        logging.info(str(log_msg))
    except Exception as e:
        log_msg = f"Error: {e}"
        logging.error(str(log_msg))
        print(e)
