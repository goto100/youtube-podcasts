# youtube-podcasts

## Run

### Prepare download.sh

You could add more lines as you wish

```/volume1/workdir/download.sh

youtube-dl --proxy socks5://127.0.0.1:1086 https://www.youtube.com/channel/CHANNEL_ID```

### Run youtube-podcasts

* Add the website visit endpoint as parameter at the end
* Run it periodic is recommended, use `crontab`

```sudo docker run --network host --rm -i -v $(pwd):/workdir:rw goto100/youtube-podcasts download.sh "http://my-server-host/"```

### Publish a static website

Nginx example:

```
server {
    listen      80;
    server_name my-server-host;
    root    "/volume1/workdir";
}
```

### Using it with apple Podcast app

The podcast feed url is `http://my-server-host/CHANNEL_NAME/podcast.xml`

## Build

```sudo docker build -t goto100/youtube-podcasts -f Dockerfile .```
