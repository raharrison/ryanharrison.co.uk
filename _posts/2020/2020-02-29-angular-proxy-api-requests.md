---
layout: post
title: Angular - Proxy API Requests
tags:
    - angular
    - proxy
    - api
    - request
typora-root-url: ../..
---

If you are developing with Angular locally, then chances are you also have some kind of API server also running on the same machine that you need to make requests to. The problem is, your local environment setup may not reflect that of a real-world deployment - where you might use something like Nginx as a reverse proxy. CORS (Cross-Origin-Resource-Sharing) policy starts to become a problem when you have something like:

-   Angular dev server on `localhost:4200`
-   Some kind of HTTP API listening on `localhost:8080`

If you try to make a request from your Angular app to `localhost:8080`, your browser will block you as it's effectively trying to access a separate host. You _could_ enable CORS on your server to explicitly enable access from different origins - but this is not something you want to turn on just to get a working dev environment.

A much better option is to use the built-in proxying support of the Angular dev server (webpack) to proxy certain URL patterns to your backend server - essentially making your browser think that they are being served from the same origin.

### Create a Proxy config file

To get this setup, simply create a config file called `proxy.conf.json` in the root of your Angular project (the name doesn't matter, but is just a convention). The most basic example is:

```
{
  "/api": {
    "target": "http://localhost:8080",
    "secure": false
  }
}
```

In this case, all requests to `http://localhost:4200/api` will be forwarded to `http://localhost:8080/api` where you API is able to handle them and pass back the responses.

More options are available in this config file, see [here](https://webpack.js.org/configuration/dev-server/#devserverproxy) for the docs from webpack.

### Point Angular to the proxy config

Next we need to point Angular to the newly created proxy config file to make sure webpack picks it up when the dev server is started (via `ng serve`).

In the main `angular.json` file, add the `proxyConfig` option to the serve target, pointing to your config file:

```
"architect": {
  "serve": {
    "builder": "@angular-devkit/build-angular:dev-server",
    "options": {
      "browserTarget": "your-application-name:build",
      "proxyConfig": "proxy.conf.json"
    },
```

When you restart the dev server, you should start seeing the proxy take effect and requests being passed through to your API server accordingly.

### Rewriting the URL paths

A very common use case when running proxies is to rewrite the URL paths - the `pathRewrite` option can be used in this scenario. For example, in the below config all requests to `http://localhost:4200/api` will be proxied straight to `http://localhost:8080` (note the absence of the `/api` path).

```
{
  "/api": {
    "target": "http://localhost:8080",
    "secure": false,
    "pathRewrite": {
      "^/api": ""
    }
  }
}
```

### More complex configuration

More complicated configuration use cases can be achieved by a creating a proxy JS config file `proxy.conf.js` instead of `JSON` (make sure to update the `proxyConfig` path if you do). The below example shows how to proxy multiple entries to the same target path:

```
const PROXY_CONFIG = [
    {
        context: [
            "/all",
            "/these",
            "/endpoints",
            "/go",
            "/to",
            "/proxy"
        ],
        target: "http://localhost:8080",
        secure: false
    }
]

module.exports = PROXY_CONFIG;
```

Because this config file is now a standard JS file, if you need to bypass the proxy, or dynamically change the request before it's sent, you can perform whatever processing you need in the JS config blocks:

```
const PROXY_CONFIG = {
    "/api/proxy": {
        "target": "http://localhost:8080",
        "secure": false,
        "bypass": function (req, res, proxyOptions) {
            if (req.headers.accept.indexOf("html") !== -1) {
                console.log("Skipping proxy for browser request.");
                return "/index.html";
            }
            req.headers["X-Custom-Header"] = "yes";
        }
    }
}

module.exports = PROXY_CONFIG;
```
