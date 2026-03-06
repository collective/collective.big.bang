[![Latest Version](https://img.shields.io/pypi/v/collective.big.bang.svg)](https://pypi.python.org/pypi/collective.big.bang/)
[![Tests Status](https://github.com/collective/collective.big.bang/actions/workflows/test.yml/badge.svg)](https://github.com/collective/collective.big.bang/actions/workflows/test.yml)
![Supported - Python Versions](https://img.shields.io/pypi/pyversions/collective.big.bang.svg?style=plastic)
[![License](https://img.shields.io/pypi/l/collective.big.bang.svg)](https://pypi.python.org/pypi/collective.big.bang/)

# collective.big.bang

```
Our whole universe was in a hot, dense state
Then nearly fourteen billion years ago expansion started, wait
The earth began to cool, the autotrophs began to drool
Neanderthals developed tools
We built a wall (we built the pyramids)
Math, science, history, unraveling the mysteries
That all started with the big bang! Hey!
```

So all started with the Plone site! Hey!
This package is used to create a Plone site when Zope is started (just before the `Ready to handle requests` sentence).

You can use environment variables to create the Plone site and choose which packages you would like to install. See "Environment variables".

You can also expand your Plone site by starting automaticaly all pending upgrade steps when database opened.

### Why not use `collective.recipe.plonesite`?

The goal is to create the Plone site when you deploy a new Plone in a containerized environment.
We think it's easier to create the Plone site on start-up, without an entrypoint or extra commands.
It's simpler in a containerized environment than starting a buildout part to create a Plone site.

---

**Fun fact:**
This package is now called `collective.big.bang` instead of the original `collective.bigbang`, because the name `collective.bigbang` was rejected by PyPI.

## Environment variables

You can add environment variables into your buildout under the `instance` part using `environment-vars`:

```
...
[instance]
...
environment-vars =
    PLONE_EXTENSION_IDS plone.app.caching:default,plonetheme.barceloneta:default
    DEFAULT_LANGUAGE fr
    ADMIN_PASSWORD mysuperpa$$w0rd
    ACTIVE_BIGBANG True
    ACTIVE_BIGBANG_EXPANSION True
```

Or use tools like [`direnv`](https://direnv.net/) (example `.envrc` file):

```bash
export PLONE_EXTENSION_IDS=plone.app.caching:default,plonetheme.barceloneta:default
export DEFAULT_LANGUAGE=fr
export ADMIN_PASSWORD=mysuperpa$$w0rd
export ACTIVE_BIGBANG=True
export ACTIVE_BIGBANG_EXPANSION=True
```

### `PLONE_EXTENSION_IDS`
A list of GenericSetup profiles to install.
**Default:** `plone.app.caching:default,plonetheme.barceloneta:default`

### `DEFAULT_LANGUAGE`
The default language of the Plone site.
**Default:** `en`

### `ADMIN_PASSWORD`
The password for the Zope "admin" user.
**Note:** No default. If not set, the admin password will not be updated.

### `ACTIVE_BIGBANG`
Create a Plone site on this instance.
Used to avoid conflict errors; should be `True` on only one instance.
**Default:** `False`

### `ACTIVE_BIGBANG_EXPANSION`
Expansion of the Plone universe, it run all pending upgrades.
Used to avoid conflict errors; should be `True` on only one instance.
**Default:** `False`

---

## Features

- Creates Plone site when Zope is started.
- Run all pending upgrade steps when database is open.
- Run scripts to create sites and run upgrade steps on demand.

---

## Run Scripts

In addition to automatic site creation on startup, `collective.big.bang` provides run scripts for manual execution. These are useful when you want more control over when sites are created or upgrades are run.

### bin/create_site

Creates a Plone site using the modern `plone.distribution` API, supporting distributions like `default`, `classic`, or `volto`.

**Usage:**

```bash
# Create site with defaults
bin/create_site

# Create site with custom settings
SITE_ID=mysite DISTRIBUTION=default bin/create_site

# Recreate existing site
DELETE_EXISTING=True bin/create_site

# With additional profiles
ADDITIONAL_PROFILES="my.addon:default,another.addon:default" bin/create_site
```

**Environment Variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `DISTRIBUTION` | `default` | Distribution name (`default`, `classic`, `volto`) |
| `SITE_ID` | `Plone` | Site ID in Zope |
| `DEFAULT_LANGUAGE` | `en` | Default language code |
| `SETUP_CONTENT` | `True` | Create example content |
| `TIMEZONE` | `Europe/Brussels` | Portal timezone |
| `DELETE_EXISTING` | `False` | Delete existing site if present |
| `ADDITIONAL_PROFILES` | | Comma-separated GenericSetup profiles to install |
| `ADMIN_PASSWORD` | | Password for Zope admin user (optional) |

### bin/upgrade_steps

Runs all pending GenericSetup upgrade steps for all installed profiles.

**Usage:**

```bash
# Run upgrade steps on default site
bin/upgrade_steps

# Run upgrade steps on specific site
SITE_ID=mysite bin/upgrade_steps
```

**Environment Variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `SITE_ID` | `Plone` | Site ID in Zope |

### Alternative: bin/instance run

You can also run the scripts using `bin/instance run`:

```bash
bin/instance run scripts/create_site.py
bin/instance run scripts/upgrade_steps.py
```

---

## Installation

Install `collective.big.bang` by adding it to your `buildout`:

```
[buildout]

...

eggs +=
    collective.big.bang

...

[instance]
...
environment-vars =
    PLONE_EXTENSION_IDS plone.app.caching:default,plonetheme.barceloneta:default
    DEFAULT_LANGUAGE fr
    ADMIN_PASSWORD mysuperpa$$w0rd
    ACTIVE_BIGBANG True
    ACTIVE_BIGBANG_EXPANSION True
```

Then run:

```bash
bin/buildout
```

## Contribute

- [Issue Tracker](https://github.com/collective/collective.big.bang/issues)
- [Source Code](https://github.com/collective/collective.big.bang)

## Support

If you're having issues, please let us know by opening an issue.

## License

The project is licensed under the **GPLv2**.
