---
title: "Assets and Transformers"
---

The [`pub serve`](pub-serve.html) and [`pub build`](pub-build.html)
commands use [transformers][] to prepare a package's [assets][] to be served
locally or to be deployed, respectively.

Use the `pubspec.yaml` file to specify which transformers your package uses
and, if necessary, to configure the transformers. (See
[Specifying transformers](#specifying-transformers) for details.) For example:

<pre>
name: myapp
dependencies:
  <b>polymer: any</b>
<b>transformers:
- polymer:
    entry_points:
    - web/index.html
    - web/index2.html</b>
</pre>

A package's assets must be in one or more of the following directories:
`lib`, `asset`, and `web`. After transformation by `pub build`, assets are
available under a directory called `build`. Assets generated from
files in a package's `lib` directory appear under a directory named
<code>packages/<em>&lt;pkg_name></em></code>, and those from the package's
`asset` directory appear under <code>assets/<em>&lt;pkg_name></em></code>.
For details, see
[Where to put assets](#where-to-put-assets) and
[How to refer to assets](#how-to-refer-to-assets).

## How transformers work {#how-transformers-work}

Here are some examples of transformers:

* The dart2js transformer, which reads in all of the `.dart` files for a
  program and compiles them to a single `.js` file.
* The polymer transformer, which converts HTML and Dart files into
  optimized HTML and Dart files.
* A linter that reads in files and produces warnings but no actual file.

Although you specify which transformers to use, you don't explicitly say
which transformers should be applied to which assets. Instead, each
transformer determines which assets it can apply itself to. For `pub serve`,
the transformers run when the dev server starts up and whenever a source
asset changes. The `pub build` command runs the transformers once and
then exits.

As the following figure shows, source assets can pass through, untransformed,
and become generated assets. Or a source asset can be transformed, such as a
`.dart` file (along with the `.dart` files that it refers to) that is
compiled to `.js`.

![a figure showing source assets and generated assets; the .html, .css, and .png files pass through, untransformed; the .dart file is transformed into a .js file (and, for pub serve only, the .dart file is passed through, as well)](/img/assets-and-transformers.png)

Dart files are a special case. The `pub build` command doesn't produce `.dart`
files because browsers in the wild don't support Dart natively (yet). The `pub
serve` command, on the other hand, does generate `.dart` assets, because
you can use Dartium while you're developing your app.

## Specifying transformers  {#specifying-transformers}

To tell pub to apply a transformer to your package's assets, specify the
transformer, as well as the package that contains the transformer, in your
package's `pubspec.yaml` file. In the following pubspec, the bold lines
specify that this package requires the polymer transformer, which is in the
polymer package (along with the rest of Polymer.dart):

<pre>
name: myapp
dependencies:
  <b>polymer: any</b>
<b>transformers:
- polymer:
    entry_points: web/index.html</b>
</pre>

We expect more transformers to be available in the future. You can specify
multiple transformers, to run either in parallel (if they're independent of
each other) or in separate phases. To specify that transformers run in
parallel, use [<code><em>transformer_1</em>, ...,
<em>transformer_n</em></code>]. If order matters, put the transformers on
separate lines.

For example, consider three transformers, specified as follows:

{% highlight yaml %}
transformers:
- [t1, t2]
- t3
{% endhighlight %}

The `t1` and `t2` transformers run first, in parallel. The `t3` transformer
runs in a separate phase, after `t1` and `t2` are finished, and can see the
outputs of `t1` and `t2`.

Pub implicitly appends a transformer that converts your Dart code to
JavaScript, so your code can run in any modern browser.

## Where to put assets  {#where-to-put-assets}

If you want a file to be an _asset_&mdash;to either be in or be used to
generate files in the built version of your package&mdash;then you need to
put it under one of the following directories:

* `lib`: Dart libraries defining the package's public API. Visible in all
  packages that use this package.
* `asset`: Other public files. Visible in all packages that use this
  package.
* `web`: A web app's static content plus its main Dart file (the one that
  defines `main()`). Visible _only_ to this package.

The following picture shows how you might structure your app's source assets,
with your main Dart file under `web` and additional Dart files under `lib`.

<pre>
<em>app</em>/
  lib/
    *.dart
  packages/
    pck/
      lib/
        *.dart
        *.js
      asset/
        *.png
        *.html
        ...
  web/
    <em>app</em>.dart
    *.html
    *.css
    *.png
    ...
</pre>

After transformation, `pub build` places generated assets under a directory
named `build`, which we'll call the _build root_. The build root has two
special subdirectories: `packages` and `assets`. The dev server simulates this
hierarchy without generating files.

The following figure shows the source assets above, plus the generated assets
produced by `pub build` if the only transformer is dart2js. In this example,
all the source files have corresponding generated files, and all the Dart
files have been compiled into a single JavaScript file.

![under the build directory are assets/ and packages/ directories, plus a bunch of files derived from the web/ directory: app.dart.js, *.html, *.css, *.png, ...](/img/input-and-output-assets.png)


## How to refer to assets

Here's how source asset locations correlate to generated asset locations,
for untransformed files:

<table>
  <tr>
    <th> Source asset location </th>
    <th> Generated asset location<br>(under the build root) </th>
  </tr>
  <tr>
    <td> <code>.../<em>&lt;your_pkg></em>/web/<em>&lt;path></em></code> </td>
    <td> <code>/<em>&lt;path></em></code> </td>
  </tr>
  <tr>
    <td> <code>.../<em>&lt;pkg_name></em>/asset/<em>&lt;path></em></code> </td>
    <td> <code>/assets/<em>&lt;pkg_name></em>/<em>&lt;path></em></code> </td>
  </tr>
  <tr>
    <td> <code>.../<em>&lt;pkg_name></em>/lib/<em>&lt;path></em></code> </td>
    <td> <code>/packages/<em>&lt;pkg_name></em>/<em>&lt;path></em></code> </td>
  </tr>
</table>

For example, consider a helloworld app's HTML file, which is in the
helloworld directory at `web/helloworld.html`. Running `pub build` produces a
copy at `build/helloworld.html`. In the dev server, you can get the HTML file
contents by using the URL `http://localhost:8080/helloworld.html`.

Transformers might change any part of <em>&lt;path></em>, especially the
filename, but they can't change the directory structure above
<em>&lt;path></em>.

[assets]: glossary.html#asset
[transformers]: glossary.html#transformer
