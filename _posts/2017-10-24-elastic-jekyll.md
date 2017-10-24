---
layout: post
title: ElasticSearch for your Jekyll Blog
tags:
  - elasticsearch
  - jekyll
  - search
---

Search functionality is very helpful to have in pretty much any website, but something that's not particularly easy to do in a static Jekyll site. Fully fledged blog solutions such as Wordpress give you a partial solution (no full text search) for free, however you have to also deal with all the associated bloat and need for a database running in the background. On statically generated sites, you have to role your own. Most of the solutions on the internet seem to lean towards doing full text search completely on the client side using a library such as [LunrJs](https://lunrjs.com/). This will work well, but you end up having to ship your whole site to the client as JSON blob before you perform the search. For smaller sites this might be fine, but otherwise that file can get quite large when you have to include all content across your entire site - no thanks.

My, perhaps heavy handed, solution (which won't work for GitHub Pages) is to use a small [ElasticSearch](https://www.elastic.co/products/elasticsearch) instance on the server side to provide great full text search across your site. It takes a little more work to set up, but once you have it all automated you can just leave it and still take advantage of all the capabilities of ElasticSearch.

I put together [elastic-jekyll](https://github.com/raharrison/elastic-jekyll) which is a small Python library that you can use to automatically index and search across your entire Jekyll blog. I'll cover below how it all fits together and how to use it.

## Parsing your Posts

The first step in the process is to find all of your posts within your site and create an in-memory representation of them with all the attributes we require. In this case the library will try to go through `~/blog/_posts` unless you pass in another path to `main.py`. Once all of the markdown files are found, each one is parsed using `BeautifulSoup` to extract the title and text content (`find_posts.py`):

{% highlight python %}
def parse_post(path):
    with open(path, encoding="utf8") as f:
        contents = f.read()

        soup = BeautifulSoup(contents, 'html.parser')
        title = soup.find('h1', { "class" : "post-title" }).text.strip()
        
        post_elem = soup.find("div", {"class": "post"})
        post_elem.find(attrs={"class": "post-title"}).decompose()
        post_elem.find(attrs={"class": "post-date"}).decompose()

        paras = post_elem.find_all(text=True)

        body = " ".join(p.strip() for p in paras).replace("  ", " ").strip()
        return (title, body)

    raise "Could not read file: " + path
{% endhighlight %}

The output is passed into `create_posts` which creates a generator of `Post` instances. Each contains:

* Id - A unique identifier to let ElasticSearch keep track of this document (modified version of the post filename)
* Url - The relative url of this post so we can create links in the search results (again uses the filename and site base directory)
* Title - The title of the post extracted from the frontmatter of the markdown file
* Text - The text content of the post. Note that this is still in markdown format so contains all of the associated special characters. A future extension might be to do some sort of sanitization on this text

## Indexing your Posts

Once we have all of the current posts properly parsed, we're ready to dump them into ElasticSearch so it can perform its indexing magic on them and let us search through it. In Python this is very straightforward to do using the [Python ElasticSearch client](https://elasticsearch-py.readthedocs.io/en/master/) library.

First we establish a connection to the ElasticSearch server you should already have running on your system. It defaults to port `9200` although you can override it if you want.

{% highlight python %}
from elasticsearch import Elasticsearch

def connect_elastic(host="localhost", port=9200):
    return Elasticsearch([{'host': host, 'port': port}])
{% endhighlight %}

For simplicity, the library will currently blow away any existing blog index that may already exist on the Elastic instance and recreate a new one from scratch. You could of course figure out delta's from the version control history etc, but for a small set of data it's way easier just to re-index everything each time:

{% highlight python %}
# remove existing blog index and create a new blank one
def refresh_index(es):
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    es.indices.create(index=index_name)
{% endhighlight %}

Then we just loop through each of the posts we got from the previous step and push them into the index:

{% highlight python %}
for post in posts:
    doc = {
        "title": post.title,
        "url": post.url,
        "body": post.body
    }

    es.index(index=index_name, doc_type=doc_type, id=post.id, body=doc)
{% endhighlight %}

At this point we now have an index sitting in ElasticSearch that is ready to receive search queries from your users and turn them into a set of search results for relevant posts.

## Searching for your Posts

To actually provide users the ability to search through your index you will need to have some kind of web service open ready to receive such Ajax calls. In my case I have a lightweight `Flask` server running which has an endpoint for searching. It simply passes the query string into ElasticSearch and returns the response as a JSON object. It is of course up to you how you want to do this so I've just provided a generic way of querying your index within `searcher.py`:

{% highlight python %}
from elasticsearch import Elasticsearch

es =  Elasticsearch([{'host': 'localhost', 'port': 9200}])

user_query = "python"

query = {
    "query": {
    "multi_match": {
        "query": user_query,
        "type": "best_fields",
        "fuzziness": "AUTO",
        "tie_breaker": 0.3,
        "fields": ["title^3", "body"]
    }
    },
    "highlight": {
        "fields" : {
            "body" : {}
        }
    },
    "_source": ["title", "url"]
}

res = es.search(index="blog", body=query)
print("Found %d Hits:" % res['hits']['total'])

for hit in res['hits']['hits']:
    print(hit["_source"])
{% endhighlight %}

This snippet will connect to your ElasticSearch instance running under `localhost` and query the `blog` index with a search term of `python`. The `query` object is an Elastic specific search DSL which you can read more about in [their documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html). ElasticSearch is a complicated and powerful beast with a ton of options at your disposal. In this case we are doing a simple `multi_match` query on the title and body fields (providing more weight onto the `title` field). We also use fuzziness to resolve any potential spelling mistakes in the user input. ElasticSearch will return us a set of `hits` which consist of objects containing just the `title` and `url` fields as specified in the `_source` field. We have no use for the others so no point in bloating the response. One cool feature is the use of highlighting which will add `<i>` tags into the body field within the response. This can then be used to apply styling on the client side to show much sections of text the engine has matched on.

This search query seems to work well for my use cases and I've literally just copied the above into the corresponding `Flask` endpoint. On the client side in your Jekyll search page, I've just used a but of good old `JQuery` to perform the Ajax call and fill in a list with the search results. Keep it simple. You can find the JS I use in the [search page](https://ryanharrison.co.uk/search.html) source.

As far as automating the process, I have a script which will rebuild my Jekyll blog after a Git push has been performed into GitHub (via hooks). After the main site is rebuilt I just call `python main.py` and everything is kept up to date. As I said before, it takes a bit of work to set up things up, but once you have it will sync itself every time you make an update.

Full source code can be found in the [GitHub repository](https://github.com/raharrison/elastic-jekyll)