#!python

import sys
import os
import io
import json
import math
import datetime
import dateutil
from feedgen.feed import FeedGenerator
from PIL import Image

def main():
	prefix = sys.argv[1]
	root = u'.'
	for name in os.listdir(root):
		target_path = os.path.join(root, name)
		if name == 'thumbnails':
			continue
		if not os.path.isdir(target_path):
			continue

		fg = FeedGenerator()
		fg.load_extension('podcast')
		fg.podcast.itunes_category('Goverment')
		process_dir(root, name, fg, prefix)
		if fg.title():
			fg.rss_file(os.path.join(target_path, u'podcast.xml'), pretty=True)
		else:
			print 'no file found, skip'

def process_dir(root, name, fg, prefix):
	path = os.path.join(root, name)
	print "Processing %s" % name

	for file in os.listdir(path):
		parts = os.path.splitext(file)
		if parts[1] != u".mp3":
			continue
		name = parts[0]

		info_filename = os.path.join(path, '%s.info.json' % name)
		if not os.path.exists(info_filename):
			continue

		thumb_dir = os.path.join(root, u'thumbnails')
		if not os.path.exists(thumb_dir):
			os.mkdir(thumb_dir)
			
		info = json.loads(io.open(info_filename, 'r', encoding='utf8').read())
		id = info['id']

		jpg_path = os.path.join(path, u'%s.jpg' % name)
		jpg_resize_path = os.path.join(thumb_dir, u'%s.jpg' % id)
		jpg_url = prefix + u'thumbnails/' + id + u".jpg"
		if not os.path.exists(jpg_resize_path):
			img = Image.open(jpg_path)
			width, height = img.size
			new_img = img.resize((3200, 1800))
			new_img = crop_center(new_img, 1800, 1800)
			new_img.save(jpg_resize_path, "JPEG", optimize=True)


		if not fg.title():
			fg.title(info['uploader'])
			fg.description(name)
			fg.link(href = info['channel_url'])
			fg.podcast.itunes_image(jpg_url)

		mp3 = prefix + info['uploader'] + u'/' + name + u".mp3"
		pub_date = datetime.datetime.strptime(info['upload_date'], '%Y%m%d').replace(tzinfo = dateutil.tz.UTC)

		fe = fg.add_entry()
		fe.id(mp3)
		fe.title(info['title'])
		fe.podcast.itunes_image(jpg_url)
		fe.link(href=info['webpage_url'])
		fe.description(info['description'])
		fe.pubDate(pub_date)
		fe.enclosure(mp3, 0, 'audio/mpeg')

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

if __name__ == "__main__":
	main()
