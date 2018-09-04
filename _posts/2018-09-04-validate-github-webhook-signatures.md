---
layout: post
title: Validate GitHub Webhook Signatures
tags:
  - github
  - webhook
  - signature
  - HMAC
typora-root-url: ..
---

I've mentioned using [GitHub webhooks](https://developer.github.com/webhooks) in a [previous post]({% post_url 2018-07-05-jekyll-rebuild-github-webhook %}) where they got used to kick-off a new Jekyll build every time a new commit is pushed. This usually involves having some kind of web server (in my case [Flask](http://flask.pocoo.org/)) running that listens for requests on some endpoint. The hope of course is that these requests only come from GitHub, but really there is nothing stopping any malicious actor from causing a denial of service attack by hitting that endpoint constantly and using up server resources.

To get around this, we need to perform some kind of validation to make sure that only requests from GitHub cause a rebuild.

## Signature Header

The folks at GitHub have thought about this and so have included an extra header in all their webhook requests. This takes the form of `X-Hub-Signature` which, from the [docs](https://developer.github.com/webhooks/#payloads), contains:

> The `HMAC` hex digest of the response body. This header will be sent if the webhook is configured with a [`secret`](https://developer.github.com/v3/repos/hooks/#create-hook-config-params). The `HMAC` hex digest is generated using the `sha1` hash function and the `secret` as the HMAC `key`.

Therefore, as described in their example, a request coming from GitHub looks like:

```
POST /payload HTTP/1.1
Host: localhost:4567
X-Github-Delivery: 72d3162e-cc78-11e3-81ab-4c9367dc0958
X-Hub-Signature: sha1=7d38cdd689735b008b3c702edd92eea23791c5f6
User-Agent: GitHub-Hookshot/044aadd
Content-Type: application/json
Content-Length: 6615
X-GitHub-Event: issues
{
  "action": "opened",
  "issue": {
  ...
```

This mentions a `secret` which gets used to construct the signature. You can set this value in the main settings page for the webhook. Of course make sure that this is strong, not repeated anywhere else and is kept private.

![GitHub Webhook](/images/2018/github-webhook.png)

## Signature Validation

As mentioned in the [docs](https://developer.github.com/webhooks/#payloads), the `X-Hub-Signature` header value will be the `HMAC SHA-1` hex digest of the request payload using the secret we defined above as the key.

Sounds complicated, but it's really quite simple to construct this value in most popular languages. In this case I'm using Python with `Flask` to access the payload and headers. The below snippet defines a `Flask` endpoint which the webhook will hit and accesses the signature and payload of the request:

```python
@app.route('/refresh', methods=['POST'])
def refresh():
    if not "X-Hub-Signature" in request.headers:
        abort(400) # bad request if no header present

    signature = request.headers['X-Hub-Signature']
    payload = request.data
```

Next, you need to get hold of the `secret` which is used as the `HMAC` key. You *could* hardcode this, but that's generally a bad idea. Instead, store the value in a permissioned file and read the contents in the script:

```python
with open(os.path.expanduser('~/github_secret'), 'r') as secret_file:
    webhook_secret = secret_file.read().replace("\n", "")
```

We now have the header value, payload and our secret. Now all that's left to do is construct the same `HMAC` digest from the payload we get and compare it with the one from the request headers. As only you and GitHub know the secret, if two signatures match, the request will have originated from GitHub.

```python
secret = webhook_secret.encode() # must be encoded to a byte array

# contruct hmac generator with our secret as key, and SHA-1 as the hashing function
hmac_gen = hmac.new(secret, payload, hashlib.sha1)

# create the hex digest and append prefix to match the GitHub request format
digest = "sha1=" + hmac_gen.hexdigest()

if signature != digest:
    abort(400) # if the signatures don't match, bad request not from GitHub

# do real work after
...
```

[Automate Jekyll with GitHub Webhooks]({% post_url 2018-07-05-jekyll-rebuild-github-webhook %})
<https://docs.python.org/3.7/library/hmac.html>
<https://developer.github.com/webhooks>
