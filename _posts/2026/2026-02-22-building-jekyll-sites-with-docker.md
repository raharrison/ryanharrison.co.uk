---
layout: post
title: Building Jekyll Sites with Docker
tags:
  - jekyll
  - docker
  - ci
  - devops
  - static-site
  - docker-compose
---

This site is built with Jekyll. That unfortunately often means wrestling with Ruby versions, gem dependencies, and environment configuration.
Different machines require different setups, and what works on your machine might not work in CI or on your VPS. Docker solves this
for many other areas by providing a standalone and reproducible build environment, so why not here as well?

The challenge is that the official Jekyll Docker images are no longer being actively maintained. Thankfully, there's a decent
community alternative that handles modern Jekyll sites without the maintenance burden.

The [bretfisher/jekyll-serve](https://github.com/BretFisher/jekyll-serve) image is well-maintained (for now) and works as a
drop-in replacement for the official Jekyll images. By default, it serves your site locally via `jekyll serve`, but you can
override the command to run any Jekyll operation you need.

The image handles all the Ruby and gem setup for you, so you don't need to worry about version conflicts or system dependencies.

## Local Development with Docker Compose

For local development, the fastest approach is using Docker Compose. Create a `compose.yml` file in your Jekyll project
root:

```yaml
services:
  jekyll:
    image: bretfisher/jekyll-serve
    volumes:
      - .:/site
    ports:
      - "4000:4000"
```

Start your development server with:

```bash
docker compose up
```

Your site will be available at `http://localhost:4000` with live reload enabled. The key benefit here is that Docker Compose
reuses the same container across runs, which caches your gems. This means subsequent starts are very quick - typically just a few
seconds once the gems are installed.

Without compose, you can achieve the same result with:

```bash
docker run -p 4000:4000 -v $(pwd):/site bretfisher/jekyll-serve
```
However, this creates a new container each time, which means reinstalling gems on every run (unless you mess around with more 
volume mounts, see below).

## Building for CI/CD

For continuous integration or deployment builds, you want to build the static site without running the server. Override the
default command to run the Jekyll build process:

```bash
docker run -v $(pwd):/site bretfisher/jekyll-serve bundle exec jekyll build
```

This generates your static site into the `_site` directory. Here's an example GitHub Actions workflow that builds on every push (also the one used to build this site):

```yaml
name: Build Jekyll Site
on:
  push:
    branches: [ master ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Build with Jekyll
        run: |
          docker run -v ${{ github.workspace }}:/site \
            bretfisher/jekyll-serve bundle exec jekyll build
```

The build is completely reproducible because the Docker image contains a known-good version of Ruby and all the necessary build
tools.

## Building on Low Memory Machines

If you're like me and building Jekyll sites on machines with limited memory (1GB or less), you might run into issues. Gem installation often
requires building native extensions, which can be memory-intensive. The `bretfisher/jekyll-serve` image runs
`bundle install --retry 5 --jobs 20` by default, which parallelizes gem installation, but uses more memory. This caused issues for me on resource-restricted boxes.

You can override the `entrypoint` to reduce the number of parallel jobs:

```bash
docker run -v $(pwd):/site \
  --entrypoint /bin/bash \
  bretfisher/jekyll-serve \
  -c "bundle install --jobs 2 && bundle exec jekyll build"
```

Reducing `--jobs` from 20 to 2 significantly reduces memory usage during the gem installation phase. The build will take a bit
longer, but it won't crash on memory-constrained systems.

<!--more-->

## Caching Gems for Faster Builds

If you're building on a persistent machine like a VPS, you can use a volume mount to cache gems across builds:

```bash
docker run -v $(pwd):/site \
  -v jekyll-gems:/usr/local/bundle \
  bretfisher/jekyll-serve bundle exec jekyll build
```

The named volume `jekyll-gems` persists the installed gems. The first build installs all gems, but subsequent builds skip gem
installation entirely and jump straight to building your site. This is much faster and significantly less resource-intensive.

You can also apply this technique in docker-compose:

```yaml
services:
  jekyll:
    image: bretfisher/jekyll-serve
    volumes:
      - .:/site
      - jekyll-gems:/usr/local/bundle
    ports:
      - "4000:4000"

volumes:
  jekyll-gems:
```

That's pretty much it. Easy enough Jekyll builds without messing around with Ruby/gem packages/versions.

## More Reading

- [bretfisher/jekyll-serve on GitHub](https://github.com/BretFisher/jekyll-serve)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
