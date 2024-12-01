from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

YOUTUBE_TRENDING_URL = "https://www.youtube.com/feed/trending"

def get_selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_videos(driver):
    VIDEO_DIV_TAG = "ytd-video-renderer"
    driver.get(YOUTUBE_TRENDING_URL)
    videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
    return videos

def parse_video(video):
        title_tag = video.find_element(By.ID, 'video-title')
        title = title_tag.text
        url = title_tag.get_attribute('href')

        thumbnail_url = video.find_element(By.TAG_NAME, 'img').get_attribute('src')

        channel = video.find_element(By.CLASS_NAME, 'ytd-channel-name').text

        metadata_spans = video.find_elements(By.CLASS_NAME, 'inline-metadata-item')
        views = metadata_spans[0].text
        uploaded = metadata_spans[1].text

        description = video.find_element(By.ID, 'description-text').text

        video_data = {'title': title, 'url': url, 'thumbnail_url': thumbnail_url, 'channel': channel, 'views': views, 'uploaded': uploaded,
                'description': description}
        return video_data

    
if __name__ == "__main__":
    print("Creating driver")
    driver = get_selenium_driver()
    
    print("Fetching trending videos")
    videos = get_videos(driver)

    print(f"Found {len(videos)} videos")

    print("Parsing top 10 video")
    videos_data = [parse_video(video) for video in videos[:10]]

    print("Save the data to a csv file")
    videos_df = pd.DataFrame(videos_data)
    print(videos_df)
    videos_df.to_csv('trending.csv', index=False )
    













