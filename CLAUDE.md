# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal blog and portfolio website built with Jekyll, a static site generator. The site is accessible at https://ryanharrison.co.uk and contains technology-related blog posts, guides, and project information.

**Important:** This is a standalone site with no external CSS or JavaScript library dependencies. Everything is vanilla - pure CSS/SASS and vanilla JavaScript. Do not add frameworks like React, jQuery, Bootstrap, Tailwind, etc. unless explicitly requested.

## Development Commands

### Local Development

Start the local Jekyll server using Docker:
```bash
docker-compose up
```

The site will be available at http://localhost:4000

Alternative method without docker-compose:
```bash
docker run -p 4000:4000 -v $(pwd):/site bretfisher/jekyll-serve
```

### Building

Build the static site:
```bash
docker run -v $(pwd):/site bretfisher/jekyll-serve bundle exec jekyll build
```

The built site will be output to the `_site/` directory.

## Repository Structure

### Content Organization

- **`_posts/`** - Blog posts organized by year subdirectories (e.g., `_posts/2023/`)
  - Post filenames follow the format: `YYYY-MM-DD-title-slug.md`
  - All posts use YAML front matter with `layout: post`, `title`, and `tags`

- **`images/`** - Static images organized by year subdirectories matching post structure

### Jekyll Configuration

- **`_config.yml`** - Main Jekyll configuration
  - Site uses `jekyll-sitemap` and `jekyll-paginate` plugins
  - Pagination is set to 5 posts per page
  - Excerpt separator is `<!--more-->`
  - Base URL is empty string (root domain)

### Layouts & Templates

- **`_layouts/`** - Page layout templates
  - `default.html` - Base layout with sidebar navigation, masthead, and scroll-to-top functionality
  - `post.html` - Blog post layout with date display, related posts section, and Disqus integration
  - `page.html` - Simple page layout

- **`_includes/`** - Reusable template components
  - `head.html` - HTML head section
  - `sidebar.html` - Sidebar navigation
  - `footer.html` - Footer section
  - `analytics.html` - Google Analytics integration
  - `disqus.html` - Comment system integration
  - `meta.html` - Meta tags for SEO

### Styles

- **`_sass/`** - SASS partials for styling
- **`css/`** - Main CSS files
- Sass is configured with `:compressed` style in production

### Features

- **Search functionality** - Custom search implementation at `search.html`
  - Queries external API: `https://api.ryanharrison.co.uk/blog/search`
  - Uses JSONP callback pattern for cross-origin requests
  - Client-side debouncing for search input

- **Pagination** - Homepage shows 5 posts per page with older/newer navigation

- **Site configuration**:
  - Google Analytics tracking (ID: G-9MVP1BEKQY)
  - Disqus comments (shortname: ryanharrison)
  - RSS feed at `/rss`
  - Social links in footer for GitHub, LinkedIn, Twitter

### Other Files

- **`archive.html`** - Archive page listing all posts
- **`guides.md`** - Guides collection page
- **`contact.html`** - Contact page
- **`about.md`** - About page
- **`404.md`** - Custom 404 error page
- **`feed.xml`** - RSS feed template
- **`search.json`** - JSON endpoint for search indexing
- **`opensearch.xml`** - OpenSearch descriptor for browser search integration

## CI/CD

GitHub Actions workflow at `.github/workflows/build.yml` runs on pushes and PRs to master:
- Uses `jekyll/jekyll:latest` Docker image
- Builds the site with `jekyll build --future` command
- Ensures the site builds successfully before merging

## Writing New Posts

1. Create a new markdown file in `_posts/YYYY/` directory
2. Use the naming convention: `YYYY-MM-DD-post-title.md`
3. Add YAML front matter with required and optional fields:
   ```yaml
   ---
   layout: post                    # Required: Always use 'post'
   title: Your Post Title          # Required: The post title
   tags:                           # Required: List of tags for the post
       - tag1
       - tag2
   image: /images/YYYY/image.png   # Optional: Custom Open Graph/Twitter Card image
                                   #           If omitted, uses site avatar
   last_modified_at: YYYY-MM-DD    # Optional: Shows "Last Updated" date on post
   typora-root-url: ../..          # Optional: For Typora markdown editor image paths
   ---
   ```
4. Add content using Markdown
5. Use `<!--more-->` to mark the excerpt separator (text before this appears on homepage)
6. Reference images as `/images/YYYY/image-name.png`

### Front Matter Field Details

- **layout**: Always set to `post` for blog posts
- **title**: The post title displayed in the browser and on social media
- **tags**: List format, used for keywords meta tag and categorization
- **image** (optional): Path to a custom image for social media sharing (Open Graph/Twitter Cards). If not specified, the site avatar (`/images/avatar.png`) is used as fallback. Most posts don't need this unless they have a particularly relevant hero image.
- **last_modified_at** (optional): Date in `YYYY-MM-DD` format. When present, displays "(Last Updated: date)" next to the post date.
- **typora-root-url** (optional): Set to `../..` if editing in Typora markdown editor for correct image path resolution

## Important Notes

- The `_site/` directory is the generated output and should not be edited directly
- Images should be organized by year to match the post structure
- The site uses a custom external API for search functionality rather than client-side search
- Docker is the preferred method for local development and building
