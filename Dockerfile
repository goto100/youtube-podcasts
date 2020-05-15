FROM mikenye/youtube-dl:latest


ENV LIBRARY_PATH=/lib:/usr/lib
ADD sources.list /etc/apt/
RUN apt update && apt install -y python python-pip && pip install lxml python-dateutil Pillow feedgen
RUN apt install -y locales
RUN sed -i -e 's/# zh_CN.UTF-8 UTF-8/zh_CN.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
ENV LANG zh_CN.UTF-8  
ENV LANGUAGE zh_CN:zh:en_US:en   
ENV LC_ALL=zh_CN.UTF-8
COPY config /etc/youtube-dl.conf
COPY youtube-podcasts.py /app/youtube-podcasts.py
COPY sync.sh /app/sync.sh
RUN chmod +x /app/sync.sh
ENTRYPOINT ["/app/sync.sh"]
