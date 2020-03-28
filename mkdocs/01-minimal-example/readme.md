# MkDocs minimal example

The example contains minimal example that uses MkDocs and [material-theme](https://github.com/squidfunk/mkdocs-material). See this [list](https://github.com/mkdocs/mkdocs/wiki/MkDocs-Themes) for full list of third party themes. There are also [build-in themes](https://www.mkdocs.org/user-guide/styling-your-docs/).

Note: the below samples make use of `make` tool. Inspect `Makefile` for raw commands you could directly run from your terminal if needed.

## 0. Pre-requisities

Create python virtual environment where you will install python libraries.

Using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) tool type:
```
mkvirtualenv mkdocs
workon mkdocs
```

In [plain python](https://docs.python.org/3/library/venv.html) you would use:
```
python3 -m venv ~/.venv/mkdocs
source ~/.venv/mkdocs/bin/activate
```

See [virtual environment tutorial](/virtualenv) for more details.

## 1. Install MkDocs library and material theme

To install required libraries type:
```
pip install -r requirements.txt
```
or type `make build`.

## 2. Setup site

Create following content:

- `mkdocs.yml` is single file that holds the site configuration.
- `docs/` directory will hold content (markdown files).

The `mkdocs.yml` is configuration for our site:

```
site_name: My MkDocs example site
theme:
  name: 'material'
nav:
    - Home: index.md
    - About: about.md
    - Text examples: examples.md
```

In `docs/` folder create `.md` files as defined in `.yml` file. Make sure there is at least `index.md`.

## 3. Preview site

Type `make serve` to build and preview the documetation. Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to open the site.

## 4. Build site

Type `make doc`. This creates `site/` directory with all html files and static content.

## 5. Deploy

Grap `site/` directory and copy it to your favorite server, cloud or use [GitHub Pages](https://pages.github.com/). 

# What's next?

Now you should be ready to inspect [more advanced example](../02-advanced-example/).


