from datetime import datetime

import scrapy
import json
from scrapy.spiders import Spider

from sia_scrapy.items import ImageItem


class InstagramSpider(Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com', 'cdninstagram.com']

    def __init__(self, users='', **kwargs):
        self.start_urls = [f'https://www.instagram.com/{user}/?__a=1' for user in users.split(',')]
        super().__init__(**kwargs)

    def parse(self, response):
        json_response = json.loads(response.body_as_unicode())

        user = json_response['graphql']['user']

        item = ImageItem()
        item['provider'] = 'instagram'
        item['user'] = user['username']

        timeline = user['edge_owner_to_timeline_media']
        posts = timeline['edges']

        yield from self.parse_posts(posts, item)

    def parse_posts(self, posts, item_parent: ImageItem):
        for p_node in posts:
            item = ImageItem()
            item['provider'] = item_parent['provider']
            item['user'] = item_parent['user']

            post = p_node['node']

            item['name'] = post['shortcode']

            time_created = post.get('taken_at_timestamp')
            if time_created:
                item['time_created'] = datetime.fromtimestamp(time_created)
            else:
                item['time_created'] = item_parent['time_created']

            item['is_video'] = post['is_video']
            if item['is_video']:
                item['file_ending'] = 'mp4'
            else:
                item['file_ending'] = 'jpg'

            post_type = post['__typename']
            if post_type == 'GraphImage':
                url = post['display_url']
                yield scrapy.Request(url, self.parse_image, cb_kwargs=dict(item=item))
            elif post_type == 'GraphVideo':
                shortcode = post['shortcode']
                url = post.get('video_url')
                if url:  # Video in sidecar
                    yield scrapy.Request(url, self.parse_video, cb_kwargs=dict(item=item))
                else:  # Single video post
                    yield scrapy.Request(f'https://www.instagram.com/p/{shortcode}/?__a=1', self.parse_video_post,
                                         cb_kwargs=dict(item=item))
            elif post_type == 'GraphSidecar':
                shortcode = post['shortcode']
                yield scrapy.Request(f'https://www.instagram.com/p/{shortcode}/?__a=1', self.parse_sidecar,
                                     cb_kwargs=dict(item=item))
            else:
                # TODO logging
                print('Unknown post type')

    def parse_sidecar(self, response, item: ImageItem):
        json_response = json.loads(response.body_as_unicode())
        posts = json_response['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']
        yield from self.parse_posts(posts, item)

    def parse_video_post(self, response, item: ImageItem):
        json_response = json.loads(response.body_as_unicode())
        url = json_response['graphql']['shortcode_media']['video_url']
        yield scrapy.Request(url, self.parse_video, cb_kwargs=dict(item=item))

    def parse_image(self, response, item: ImageItem):
        item['data'] = response.body
        yield item

    def parse_video(self, response, item: ImageItem):
        item['data'] = response.body
        yield item
