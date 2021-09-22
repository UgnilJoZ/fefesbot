import asyncio
from nio import AsyncClient
import feedparser
from typing import List
import json
from bs4 import BeautifulSoup
import requests

with open('config.json') as js:
    config = json.load(js)

def get_latest_post_id() -> str:
    "Latest known and handled post"
    try:
        return open("latest_post","r").read().strip()
    except FileNotFoundError:
        return ""

def get_formatted_blogpost(url: str) -> str:
    "Retrieve the given blog post as HTML"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    blogpost = "".join(str(item) for item in soup.li.contents)
    return blogpost

def get_new_blogposts() -> List[dict]:
    "Get all posts since the last handled post"
    last_post = get_latest_post_id()
    posts = feedparser.parse("https://blog.fefe.de/rss.xml")['entries']
    new_posts = []
    while posts and (post := posts.pop(0))['id'] != last_post:
        new_posts.append(post)
    new_posts.reverse()
    return new_posts

def save_latest_post_id(id: str) -> None:
    with open("latest_post", "w") as file:
        file.write(id)

def get_client() -> AsyncClient:
    client = AsyncClient(config['server'])
    client.access_token = config['access_token']
    client.user_id = config['user']
    client.device_id = config['user']
    return client

async def post_entry(client, msg: str, formatted: str) -> None:
    await client.room_send(
        room_id=config['room'],
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": msg,
            "format": "org.matrix.custom.html",
            "formatted_body": formatted
        }
    )

async def main() -> None:
    if posts := get_new_blogposts():
        client = get_client()
        for post in posts:
            await post_entry(client, post['title'], get_formatted_blogpost(post['link']))
            print(f"Posted {post['id']}.")
        save_latest_post_id(posts[-1]['id'])
        await client.close()

asyncio.get_event_loop().run_until_complete(main())
