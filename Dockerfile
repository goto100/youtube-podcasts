FROM mikenye/youtube-dl

ENV LIBRARY_PATH=/lib:/usr/lib
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && apk add build-base python-dev py-pip jpeg-dev zlib-dev libxslt-dev && pip install lxml python-dateutil Pillow feedgen
COPY config /etc/youtube-dl.conf
COPY youtube-podcasts.py /app/youtube-podcasts.py
COPY sync.sh /app/sync.sh
RUN chmod +x /app/sync.sh
ENTRYPOINT ["/app/sync.sh"]
