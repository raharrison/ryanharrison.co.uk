---
layout: post
title: Automatically Update Dependencies with GitHub Dependabot
tags:
  - github
  - dependencies
  - dependabot
  - automatic
  - java
  - python
typora-root-url: ..
---

With the introduction of [Actions]({{ site.baseurl }}{% post_url 2020-04-12-kotlin-java-ci-with-github-actions %}), GitHub is quickly becoming the one-stop shop for all things CI. But one, perhaps less well-known feature, is `dependabot` which allows you to automatically keep all your dependencies up to date. Depending on which language/framework you are using, making sure all your libraries are on the latest versions can be tricky. `Maven`/`Gradle` have plugins which will notify you of new versions, but this is a decidedly manual process. Plus if you are unlucky enough to develop in JS land, then good luck attempting to keep your 400 `npm` dependencies updated at any reasonable recurrence.

Instead, GitHub `Dependabot` will automatically read your project build files (`build.gradle`, `package.json`, `requirements.txt` etc) and create new pull requests to update libraries to newer versions. If you have a GitHub Action configured to run your build on all PR's, then you can also gain some reasonable level of confidence that such newer versions won't break your project (of course depending on quality of your tests).

### Updating Java Dependencies

Configuring `Dependabot` is as simple as adding a `dependendabot.yml` file in the `.github` directory at the root level of your project (the same place any action workflow config files are also placed).

```yaml
version: 2
updates:
  # Enable version updates for Gradle
  - package-ecosystem: "gradle"
    # Look for `build.gradle` in the `root` directory
    directory: "/"
    # Check for updates once daily
    schedule:
      interval: "daily"
```

The above example sets up the most simple of use cases, which will use the `gradle` package manager to search for a `build.gradle` file in the `/` directory of your project and attempt to update any libraries on a daily basis.

When a new library version is released, a new Pull Request will be opened on your project - in the below example for Kotlin `Ktor`:

![Dependabot Pull Request](./images/2020/dependabot_pr.png)

The great thing about Dependabot though is that these pull requests aren't just notifications - it's clever enough to actually modify the build files (`build.gradle` in this case to the newer version):

![Dependabot Changes](./images/2020/dependabot_changes.png)

If all looks good (and hopefully your build still passes), all you have to do is merge the PR and you are good to go.

### Updating Python Dependencies

The config for Python is very much the same (and for a variety of other languages). In this case, the scheduled interval is set to weekly instead of daily to avoid too much PR noise for fast moving dependencies. It is also set to ignore all updates to `flask` libraries - useful if you are required to fix at an older level for some reason:

```yaml
  - package-ecosystem: "pip"
    # Look for `build.gradle` in the `root` directory
    directory: "/"
    # Check for updates once weekly
    schedule:
      interval: "weekly"
      ignore:
      # Ignore updates to packages that start 'aws'
      # Wildcards match zero or more arbitrary characters
      - dependency-name: "flask*"
```

Make sure that you have your build workflow configured to run on all pull requests to the master branch in order to run your build automatically. See [this previous post]({{ site.baseurl }}{% post_url 2020-04-12-kotlin-java-ci-with-github-actions %}) on how to setup build actions.

```yaml
name: Build

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]
```

You will then see the standard "All checks have passed" message on the PR if your build still passes on the newer dependency version. Make sure that you have adequate tests before you hit merge without trying it yourself though - ideally decent integration tests which actually start up your application. Unit tests are generally not enough to verify this kind of thing.

![Dependabot Build](./images/2020/dependabot_build.png)

### Additional Commands

You can interact with Dependabot by leaving comments on the pull requests that it opens - if for example you want to rebase against newer changes you've committed since it was run, or if you want to ignore a certain major/minor release version:

- `@dependabot rebase` will rebase this PR
- `@dependabot merge` will merge this PR after your CI passes on it
- `@dependabot squash and merge` will squash and merge this PR after your CI passes on it
- `@dependabot reopen` will reopen this PR if it is closed
- `@dependabot close` will close this PR and stop Dependabot recreating it. You can achieve the same result by closing it manually
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)

### More Info

[GitHub Dependabot Docs](https://docs.github.com/en/github/administering-a-repository/about-github-dependabot-version-updates)

[Above Examples](https://github.com/raharrison/lynks-server/blob/master/.github/dependabot.yml)

[dependabot.yml](https://docs.github.com/en/github/administering-a-repository/configuration-options-for-dependency-updates)