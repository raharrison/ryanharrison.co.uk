---
layout: post
title: Python - RESTful server with Flask
tags:
    - python
    - rest
    - flask
    - -web
---

[1]: {{ site.baseurl }}{% post_url 2017/2017-10-24-elastic-jekyll %}

The [Flask library](http://flask.pocoo.org/) for Python is a great microframework for setting up simple web servers. Larger sites or REST interfaces might want to tend towards the [Django framework](https://www.djangoproject.com/) instead, but I've found Flask excellent for putting together small sites or a couple endpoints with next to no effort. The API is very Pythonic so of course you can get up and running with very few lines of code. I currently use Flask for the backend API services for this site - which powers the [search page][1], contact page and automated Jekyll builds using Github hooks.

### Installation

To install and start using Flask, just use `pip`:

    $ pip install Flask

### Simple Example

The most basic endpoint looks like:

{% highlight python %}
from flask import Flask
app = Flask(**name**)

@app.route('/')
def hello_world():
return 'Hello, World!'
{% endhighlight %}

We imported the main Flask class and created a new instance passing in the name of the current module as an identifier (so Flask knows where to look for static files and templates). A simple function, which in this case just returns a `String`, can be decorated with `route` to define the URL which will trigger the function.

### Running on a development server

There are a couple ways to run the above example. The first is the way recommended by the Flask team:

    $ export FLASK_APP=hello.py
    $ flask run
    * Running on http://127.0.0.1:5000/

This is fine on Linux boxes (you can also use `set` instead of `export` on Windows), but setting an environment variable on Windows is a bit of a pain, so instead you can start the server via code. Apparently this might cause issues with live reload, but Flask starts up so quickly it's not too much of an issue:

{% highlight python %}
if **name** == '**main**':
app.run(host='0.0.0.0')
{% endhighlight %}

You can then navigate to `http://localhost:5000` and you will see the return value of the `hello_world` function. You can easily return `HTML` or a `JSON` objects as needed depending on what services you wish to build.

### Handling GET Requests

I have focused mainly on using Flask to create basic RESTful web endpoints instead of serving HTML - which Flask can do very well using the `Jinja2` templating engine. The below snippet shows how to create a simple endpoint to handle `GET` requests to retrieve a user by their unique id. The returned object from our dummy service is converted into a JSON response via the built in `jsonify` function:

{% highlight python %}
from Flask import jsonify

# here the user_id parameter is restricted to an int type

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id): # get the user from some service etc
user = user_service.find_user(user_id)
return jsonify(user) # return the user as a JSON object
{% endhighlight %}

### Handling POST Requests

The below snippet shows how we can handle a `POST request`, taking in a `JSON` object and returning a response from our service:

{% highlight python %}
from flask import request

@app.route('/user/' methods=['POST'])
def save_user(): # retrieve the json from the request
new_user = request.get_json(silent=True)
created_user = user_service.create_user(new_user) # return the newly created user as a json object
return jsonify(created_user)
{% endhighlight %}

As you can see, setting up simple endpoints is very quick and easy using Flask. The framework also offers a ton of other useful features including:

-   built-in development server and debugger
-   integrated unit testing support
-   RESTful request dispatching
-   Jinja2 templating
-   support for secure cookies (client side sessions)
-   great documentation

[Flask website](http://flask.pocoo.org/)

[Quickstart guide](http://flask.pocoo.org/docs/0.12/quickstart)
