from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import smtplib
from dotenv import load_dotenv
import os
import json
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

load_dotenv()

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

def send_email(filename):
    try:
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()

        gmail_user = 'learntocode655@gmail.com'
        gmail_password = os.getenv('EMAIL_PASSWORD')

        sent_from = gmail_user
        to = 'learntocode655@gmail.com'

        # code to attach file to the email
        msg = MIMEMultipart()   
 
        msg['From'] = sent_from 
   
        msg['To'] = to 
         
        msg['Subject'] = "Top 10 Trending Videos"
        
        body = "Please find attached the csv of top 10 youtube videos that was scraped using selenium"
        
        msg.attach(MIMEText(body, 'plain')) 
        
        # open the file to be sent  
        attachment = open(filename, "rb") 
        
        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 
        
        # To change the payload into encoded form 
        p.set_payload((attachment).read()) 
        
        # encode into base64 
        encoders.encode_base64(p) 
        
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
        
        # attach the instance 'p' to instance 'msg' 
        msg.attach(p) 

        # converts the Multipart msg into a string
        email_text = msg.as_string()

        server_ssl.login(gmail_user, gmail_password)
        server_ssl.sendmail(sent_from, to, email_text)
        server_ssl.close()

        print('Email sent!')

    except Exception as e:
        print('Something went wrong', str(e))
    
if __name__ == "__main__":
    print("Creating driver")
    driver = get_selenium_driver()
    
    print("Fetching trending videos")
    videos = get_videos(driver)

    print(f"Found {len(videos)} videos")

    print("Parsing top 10 videos")
    videos_data = [parse_video(video) for video in videos[:10]]

    print("Save the data to a csv file")
    videos_df = pd.DataFrame(videos_data)
    videos_df.to_csv('trending.csv', index=False )
    
    print("Sending the results over email")
    data = json.dumps(videos_data, indent=4)
    send_email('trending.csv')

    print("Finished")