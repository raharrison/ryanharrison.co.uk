![Jekyll Build](https://github.com/raharrison/ryanharrison.co.uk/workflows/Jekyll%20site%20CI/badge.svg)

# Ryan Harrison's Blog

My personal website and blog. Powered by [Jekyll](https://jekyllrb.com/)

Accessible at <https://ryanharrison.co.uk>

## Serve

```plain
docker-compose up
or
docker run -p 4000:4000 -v $(pwd):/site bretfisher/jekyll-serve
```

## Build

```plain
docker run -v $(pwd):/site bretfisher/jekyll-serve bundle exec jekyll build
```
