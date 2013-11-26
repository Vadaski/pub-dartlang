---
title: "Command: Serve"
---

    $ pub serve [--port <number>]

This command starts up a _development server_, or _dev server_,
for your Dart web app. The dev server is an HTTP server on localhost
that serves up your web app's [assets](glossary.html#asset).

Start the dev server from the directory that contains your web app's
`pubspec.yaml` file:

    $ cd ~/dart/helloworld
    $ pub serve
    Serving helloworld on http://localhost:8080

The dev server doesn't just serve up assets, it produces them by running
[transformers](glossary.html#transformer). A transformer converts input
assets (such as Dart files or Polymer-formatted HTML) into output assets
(such as JavaScript and HTML).

These output assets aren't in the file system; they exist only in the dev
server. When you're ready to deploy, generate output files by running
[`pub build`](pub-build.html).

Pub automatically includes a dart2js transformer that compiles your Dart code
to JavaScript. With this, you can change some Dart code, refresh your
non-Dartium browser, and immediately see the changes.

See [Assets and Transformers](assets-and-transformers.html) for
information on:

* Where in your package to put assets.
* What URLs to use when referring to assets.
* How to use `pubspec.yaml` to specify which transformers run, and in
  what order.

## Options

### `--port`

By default the dev server uses `http://localhost:8080`. To change the port
number, use the `--port` option:

    $ pub serve --port 9080
    Serving helloworld on http://localhost:9080

### `--mode=<mode>`

Specifies a transformation mode. Typical values are "debug" and "release", but
any word is allowed. Transformers may use this to change how they behave.

If set to "release" pub will generate minified JavaScript using dart2js.
Otherwise, it generates it unminified. Also, in release mode, Pub will not
include any source .dart files in the resulting build output since they have
been compiled to JavaScript. In any other mode, the raw Dart files will be
included.

If omitted, it defaults to "debug".

## What about Dart Editor's server?

Dart Editor has its own dev server. We plan to unify it with the
pub dev server soon.
