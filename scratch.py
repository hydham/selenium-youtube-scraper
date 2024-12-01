from bs4 import BeautifulSoup
import requests

YOUTUBE_TRENDING_URL = "https://www.youtube.com/feed/trending"

response = requests.get(YOUTUBE_TRENDING_URL)

print("Status code", response.status_code)
print(response.encoding)

with open('trending.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

doc = BeautifulSoup(response.text, 'html.parser')

print("Page title:", doc.title.text)

# Find all the video divs
video_divs = doc.find_all('div', class_="ytd-video-renderer")

print(f"Found {len(video_divs)} videos")