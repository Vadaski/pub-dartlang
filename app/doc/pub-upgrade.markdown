---
title: "Command: Upgrade"
---

    $ pub upgrade [PACKAGE]

Without any additional arguments, `pub upgrade` gets the latest versions of
all the dependencies listed in the [`pubspec.yaml`](pubspec.html) file in the
current working directory, as well as their [transitive
dependencies](glossary.html#transitive-dependencies), to the `packages`
directory located next to the pubspec. For example:

    $ pub upgrade
    Dependencies upgraded!

When `pub upgrade` upgrades dependency versions, it writes a
[lockfile](glossary.html#lockfile) to ensure that future [`pub
get`s](pub-get.html) will use the same versions of those dependencies.
Application packages should check in the lockfile to source control; this
ensures the application will use the exact same versions of all dependencies for
all developers and when deployed to production. Library packages should not
check in the lockfile, though, since they're expected to work with a range of
dependency versions.

If a lockfile already exists, `pub upgrade` will ignore it and generate a new
one from scratch using the latest versions of all dependencies. This is the
primary difference between `pub upgrade` and `pub get`, which always tries to
get the dependency versions specified in the existing lockfile.

## Upgrading specific dependencies

It's possible to tell `pub upgrade` to upgrade specific dependencies to the
latest version while leaving the rest of the dependencies alone as much as
possible. For example:

    $ pub upgrade unittest args
    Dependencies upgraded!

Upgrading a dependency upgrades its transitive dependencies to their latest
versions as well. Usually, no other dependencies are updated; they stay at the
versions that are locked in the lockfile. However, if the requested upgrades
cause incompatibilities with these locked versions, they will be selectively
unlocked until a compatible set of versions is found.

## Getting a new dependency

If a dependency is added to the pubspec before `pub upgrade` is run, it will
get the new dependency and any of its transitive dependencies and place them in
the `packages` directory. This is the same behavior as `pub get`.

## Removing a dependency

If a dependency is removed from the pubspec before `pub upgrade` is run, it
will remove the dependency from the `packages` directory, thus making it
unavailable for importing. Any transitive dependencies of the removed dependency
will also be removed, as long as no remaining immediate dependencies also depend
on them. This is the same behavior as `pub get`.

## Upgrading while offline

If you don't have network access, you can still run `pub upgrade`. Since pub
downloads packages to a central cache shared by all packages on your system, it
can often find previous-downloaded packages there without needing to hit the
network.

However, by default, pub will always try to go online when you upgrade if you
have any hosted dependencies so that it can see if newer versions of them are
available. If you don't want it to do that, pass the `--offline` flag when
running pub. In this mode, it will only look in your local package cache and
try to find a set of versions that work with your package from what's already
available.

Keep in mind that pub *will* generate a lockfile after it does this. If the
only version of some dependency in your cache happens to be old, this will lock
your app to that version. The next time you are online, you will likely want to
run `pub upgrade` again to upgrade to a later version.
