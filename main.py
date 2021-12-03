import smtplib
import os
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


html_text = 'https://www.youtube.com/feed/trending?bp=6gQJRkVleHBsb3Jl'

def get_driver():
  chrome_options = Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--disable-dev-shm-usage')
  chrome_options.add_argument('--headless')
  driver = webdriver.Chrome(options = chrome_options)

  return driver

def get_videos(driver):
  print("Fetching Videos")
  videos_div_class = 'ytd-video-renderer'
  videos_div = driver.find_elements(By.TAG_NAME, videos_div_class)

  return videos_div

def parse_videos(video):
  #title
  title_tag = video.find_element(By.ID, 'video-title')
  title = title_tag.text

  #link
  link_tag = title_tag.get_attribute('href')

  #creator
  channel_tag = video.find_element(By.CLASS_NAME, 'ytd-channel-name')
  channel = channel_tag.text

  #views and post_created
  # meta_tag = video.find_element(By.ID, 'metadata-line')
  # meta = meta_tag.text

  #description
  desc_tag = video.find_element(By.ID, 'description-text')
  desc = desc_tag.text

  # thumbnail
  thumbnail_tag = video.find_element(By.TAG_NAME, 'img')
  thumbnail = thumbnail_tag.get_attribute('src')

  return {
    'Title': title,
    'Link' : link_tag,
    'Channel Name' : channel,
    # 'Views' : views,
    # 'Created at' : created_at,
    'Description' : desc,
    'Thumbnail Link' : thumbnail
  }

def send_email(body):
  
  try:
    server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_ssl.ehlo()
    SENDER_EMAIL = 'webscraping.trend@gmail.com'
    SENDER_PASSWORD = os.environ['pass']
    RECEIVER_EMAIL = 'webscraping.trend@gmail.com'
    subject = 'Testing SMTP'
    body = f'Youtube Trending Videos\n {body}'

    email_text = f"""\
    From: {SENDER_EMAIL}
    To: {RECEIVER_EMAIL}
    Subject: {subject}

    {body}
    """
    server_ssl.login(SENDER_EMAIL, SENDER_PASSWORD)
    server_ssl.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_text)
    print('Email Sent Successfully')
    server_ssl.close()
  except:
    print('something went wrong')





if __name__ == '__main__':
  print('Generating Driver')
  driver = get_driver()

  print('Fetching Page..')
  driver.get(html_text)
  print('Page Title: ', driver.title)

  videos = get_videos(driver)
  print(f'Found {len(videos)} videos')
  

  print('Parsing 50 Videos')
  videos_data = [parse_videos(video) for video in videos[:50]]

  print('Save the data to CSV File')
  videos_df = pd.DataFrame(videos_data)
  print(videos_df)
  videos_df.to_csv('trending.csv', index=None)

  print('Send result over email')
  body = json.dumps(videos_data, indent=4)
  send_email(body)

  print('Finished')



  

  

  
  


