FROM vimagick/youtube-dl

COPY config /etc/youtube-dl.conf
COPY youtube-podcasts.py /youtube-podcasts/youtube-podcasts.py
WORKDIR /youtube-podcasts/