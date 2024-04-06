FROM ruby:3.0.0

WORKDIR /srv/jekyll
COPY ./static/Gemfile .

ARG uid
ARG uname
ARG gid
ARG gname

RUN groupadd -g $gid $gname
RUN useradd -ms /bin/bash -u $uid -g $gid $uname

RUN gem install jekyll bundler
RUN bundle install

USER 1000:1000
ENV GEM_HOME=/usr/local/bundle
ENV PATH="/usr/local/bundle/bin:${PATH}"

