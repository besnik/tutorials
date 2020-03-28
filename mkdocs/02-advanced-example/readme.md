# MkDocs advanced example

This example contains MkDocs configured with more plugins for extra formatting options.

See `mkdocs.yml` for configuration details.

## 1. Configuration of material theme

### Markdown extensions

This is complete list of [extensions](https://squidfunk.github.io/mkdocs-material/extensions/admonition/) supported by material theme.

There are several markdown extensions enabled to improve rendering of html:

- `codehilite` for [code highlighting](https://squidfunk.github.io/mkdocs-material/extensions/codehilite/) (has depedency on `pygments` library, see `requirements.txt`).
- `admonition` for [block-styled content](https://squidfunk.github.io/mkdocs-material/extensions/admonition/), e.g. hints and warnings.
- `meta` for extending the content with [metadata](https://squidfunk.github.io/mkdocs-material/extensions/metadata/) for more control over content.
- `toc` for table of contents and [permalinks](https://squidfunk.github.io/mkdocs-material/extensions/permalinks/).
- `pymdownx.details` is extension from [PyMdown extensions](https://squidfunk.github.io/mkdocs-material/extensions/pymdown/) to render [collapsible blocks](https://facelessuser.github.io/pymdown-extensions/extensions/details/). See the whole list of extensions for even more possibilities, e.g. rendering mathematical equations. 

```
markdown_extensions:
    - codehilite
    - admonition
    - meta
    - toc:
        permalink: True
    - pymdownx.details
```

### Plugins

```
plugins:
    - search:
        lang: en
```

### Color palette 

Material theme defines several [colors](https://squidfunk.github.io/mkdocs-material/getting-started/#color-palette) you can use in `.yml` file:
```
theme:
  palette:
    primary: 'deep purple'
    accent: 'deep purple'
```

### Favicon

```
img/favicon.ico
```

### Social icons

```
extra:
  social:
    - type: 'github'
      link: 'https://github.com/squidfunk'
    - type: 'twitter'
      link: 'https://twitter.com/squidfunk'
    - type: 'linkedin'
      link: 'https://www.linkedin.com/in/squidfunk'
```

## 2. Preview site

Type `make serve` to build and preview the documetation. Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to open the site.

## 3. Build site

Type `make doc`. This creates `site/` directory with all html files and static content.

## 4. Deploy

Grap `site/` directory and copy it to your favorite server, cloud or use [GitHub Pages](https://pages.github.com/). 

# What's next?

Get into more details on [official docs](https://www.mkdocs.org/user-guide/writing-your-docs/).
