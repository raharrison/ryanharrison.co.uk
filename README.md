![Jekyll Build](https://github.com/raharrison/ryanharrison.co.uk/workflows/Jekyll%20site%20CI/badge.svg)

# Ryan Harrison's Blog

My personal website and blog. A standalone Jekyll site with vanilla CSS and JavaScript - no external frameworks or libraries.

**Live Site:** <https://ryanharrison.co.uk>

## Tech Stack

- **Static Site Generator:** [Jekyll](https://jekyllrb.com/)
- **Styling:** Vanilla CSS (SASS/SCSS)
- **JavaScript:** Pure JavaScript (no frameworks)

## Development

### Local Server

Start the local Jekyll development server:

```bash
docker compose up
```

Alternative without docker-compose:
```bash
docker run -p 4000:4000 -v $(pwd):/site bretfisher/jekyll-serve
```

The site will be available at http://localhost:4000

### Build

Build the static site for production:

```bash
docker run -v $(pwd):/site bretfisher/jekyll-serve bundle exec jekyll build
```

Output will be in the `_site/` directory.

### Dependencies

Update Ruby gems:
```bash
bundle update
```

## Project Structure

```
├── _config.yml          # Jekyll configuration
├── _includes/           # Reusable template components
├── _layouts/            # Page layouts
├── _posts/              # Blog posts (organized by year)
├── _sass/               # SASS partials
├── css/                 # Main stylesheets
├── images/              # Static images (organized by year)
├── .github/workflows/   # CI/CD configuration
└── _site/               # Generated static site (git-ignored)
```

## Writing Posts

Create a new post in `_posts/YYYY/YYYY-MM-DD-post-title.md`:

```markdown
---
layout: post                    # Required: Always 'post'
title: Your Post Title          # Required
tags:                           # Required: List of tags
    - tag1
    - tag2
image: /images/YYYY/image.png   # Optional: Social media share image
last_modified_at: YYYY-MM-DD    # Optional: Last update date
typora-root-url: ../..          # Optional: For Typora editor
---

Post excerpt here...

<!--more-->

Full post content here...
```

### Front Matter Fields

- **layout**: Always `post` for blog posts
- **title**: Post title shown in browser and social media
- **tags**: List of tags for categorization and SEO
- **image** (optional): Custom image for Open Graph/Twitter Cards. If omitted, defaults to site avatar. Only add if the post has a particularly relevant image.
- **last_modified_at** (optional): Shows "Last Updated" date on the post
- **typora-root-url** (optional): Set to `../..` for Typora markdown editor compatibility

## CI/CD

GitHub Actions automatically builds and tests the site on every push to `master`.

## Contributing

This is a personal blog, but if you find issues or have suggestions, feel free to open an issue.

## License

See [LICENSE.md](LICENSE.md)
