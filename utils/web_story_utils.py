import requests
import re

def create_web_story_html(title, content, images_url, file_name):
    final_html = """
            <!DOCTYPE html>
            <html ⚡>
            <head>
              <meta charset="utf-8">
              <title>{title}</title>
              <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
              <link rel="canonical" href="https://oniichan.in/web-stories/{file_name}">
              <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
              <script async src="https://cdn.ampproject.org/v0.js"></script>
              <script async custom-element="amp-video" src="https://cdn.ampproject.org/v0/amp-video-0.1.js"></script>
              <script async custom-element="amp-story" src="https://cdn.ampproject.org/v0/amp-story-1.0.js"></script>
              <link href="https://fonts.googleapis.com/css?family=Oswald:200,300,400" rel="stylesheet">
              <script async custom-element="amp-analytics" src="https://cdn.ampproject.org/v0/amp-analytics-0.1.js"></script>


              <style amp-custom>
              amp-story {{
                    font-family: 'Oswald',sans-serif;
                    color: #fff;
                  }}
                h2 {{
                    font-weight: bold;
                    font-weight: normal;
                    line-height: 1.174;
                  }}
                h1 {{

                    font-weight: bold;
                    font-weight: normal;
                    line-height: 1.174;
                  }}
                  p {{
                    font-weight: normal;
                    font-size: 1em;
                    line-height: 1.2em;
                    color: #fff;
                  }}
                amp-story-grid-layer.center-text {{
                    align-content: center;
                  }}
                .banner-text {{
                padding: 0.5em;
                    text-align: center;
                    background-color: rgba(0, 0, 0, 0.6);
                border-radius: 25px;
                  }}
              amp-story-grid-layer.noedge {{
                    padding: 0px;
                  }}
              .wrapper {{
                    display: grid;
                    grid-template-columns: 50% 50%;
                    grid-template-rows: 50% 50%;
                  }}
              </style>
            </head>
            <body>

              <amp-story standalone
              title="{title}"
                publisher="Onii Chan"
                publisher-logo-src="https://oniichan.in/wp-content/uploads/2023/07/web-story-logo.png"
                poster-portrait-src="{cover_url}">

                <amp-analytics type="gtag" data-credentials="include">
                <script type="application/json">
                {{
                  "vars" : {{
                    "gtag_id": "G-FC14YS5K2Z",
                    "config" : {{
                      "G-FC14YS5K2Z": {{ "groups": "default" }}
                    }}
                  }}
                }}
                </script>
                </amp-analytics>

                <!-- Title Slide -->

              <amp-story-page id="cover" auto-advance-after="5s">
                    <amp-story-grid-layer template="fill">
                      <amp-img src="{cover_url}" layout="fill"></amp-img>
                  </amp-story-grid-layer>
                  <amp-story-grid-layer template="thirds">
                  <div grid-area="lower-third" >
                  <h2 class="banner-text">{title}</h2>
                  </div>
                    </amp-story-grid-layer>
                  </amp-story-page>
            """
    # define images
    if len(images_url) > 1:
        cover_image_url = images_url[0]
        images_url = images_url[1:]
    else:
        cover_image_url = images_url[0]

    final_html = final_html.format(title=title, cover_url=cover_image_url, file_name=file_name)

    for i, item in enumerate(content):
        image_index = i % len(images_url)  # Calculate the index of the image URL to use
        image_url = images_url[image_index]  # Get the corresponding image URL
        add_slide_html = """
            <amp-story-page id="page{id}" auto-advance-after="5s"> <!-- changing id is imp -->
                <amp-story-grid-layer template="fill">
                  <amp-img src="{bg_img}" layout="fill"></amp-img> <!-- change src to background image url -->
                </amp-story-grid-layer>
                <amp-story-grid-layer template="thirds">
                    <div grid-area="lower-third" >
                        <p class="banner-text" animate-in="fly-in-bottom">{slide_content}</p>
                    </div>
                </amp-story-grid-layer>
            </amp-story-page>
            """
        add_slide_html = add_slide_html.format(id=i + 1, bg_img=image_url, slide_content=item)

        final_html += add_slide_html

    closing_html = """
        <!--Last Slide With CTA-->
        <amp-story-page id="page{id}">
              <amp-story-grid-layer template="vertical" class="noedge">
                <div class="wrapper">
                  <amp-img src="https://oniichan.in/wp-content/uploads/2023/06/Untitled-1-3-450x450.jpg"
                      width="720" height="1280"
                      layout="responsive"
                      animate-in="fade-in"
                      animate-in-delay="0.4s">
                  </amp-img>
                  <amp-img src="https://oniichan.in/wp-content/uploads/2023/06/Untitled-3-450x450.jpg"
                      width="720" height="1280"
                      layout="responsive"
                      animate-in="fade-in"
                      animate-in-delay="0.6s">
                  </amp-img>
                  <amp-img src="https://oniichan.in/wp-content/uploads/2023/06/Untitled-4-450x450.jpg"
                      width="720" height="1280"
                      layout="responsive"
                      animate-in="fade-in"
                      animate-in-delay=".8s">
                  </amp-img>
                  <amp-img src="https://oniichan.in/wp-content/uploads/2023/06/Untitled-1-2-450x450.jpg"
                      width="720" height="1280"
                      layout="responsive"
                      animate-in="fade-in"
                      animate-in-delay="1s">
                  </amp-img>
                </div>
              </amp-story-grid-layer>
              <amp-story-grid-layer template="vertical" class="center-text">
                <h1 class="banner-text" animate-in="whoosh-in-right">Want Anime Merch ?</h1>
              </amp-story-grid-layer>
          <amp-story-page-outlink layout="nodisplay" theme="dark">
          <a href="https://www.oniichan.in">Shop Now</a>
          </amp-story-page-outlink>
            </amp-story-page>


        </amp-story>

      </body>
      </html>
        """
    last_pg_id = len(content) + 1
    closing_html = closing_html.format(id=last_pg_id)
    final_html += closing_html

    return final_html

def get_cover_image(query, count=1):
    url = f"https://kitsu.io/api/edge/anime?filter[text]={query}&page[limit]={count}"
    response = requests.get(url)
    data = response.json()
    if "data" in data:
        for result in data["data"]:
            if "attributes" in result and "posterImage" in result["attributes"]:
                return result["attributes"]["posterImage"]["original"]
    return None

def search_images(query, api_key, count=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": "00d2aa04fa1404304",
        "q": query,
        "searchType": "image",
        "num": count
    }
    response = requests.get(url, params=params)
    data = response.json()
    images = []
    if "items" in data:
        for item in data["items"]:
            image_url = item["link"]
            image_height = item['image']["height"]
            image_width = item['image']["width"]
            if image_width < image_height:
                images.append(image_url)
    return images

def remove_special_characters(input_string):
    pattern = r'[^a-zA-Z0-9\s]'
    processed_string = re.sub(pattern, '', input_string)
    return processed_string
