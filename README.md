# Curvenote Template

Curvenote Template is a command line tool (cli) for jinja-style templating of LaTeX documents. This means you can build templates in LaTeX and then quickly or semi-automatically create new latex documents with different content by running the tool. The templating syntax has been chosen specifically to not collide with LaTeX markup.

We built this package while developing our template based PDF export for [Curvenote](https://curvenote.com) and some examples of templates that this package can process are available on the [Curvenote Community Template Repo](https://github.com/curvenote/templates).

You can use this tool free-form with any template layout, and document model that you like but it is opinionated, it does certain things the Curvenote way.

If you are contributing a new template to the [Curvenote Community Template Repo](https://github.com/curvenote/templates) this is definitely the tool you need for development and testing.

## Quick Start

### Template Syntax 101

...

### Free Form Rendering

...

### Rendering with a Curvenote Template

...

## CLI

...

## Technical Details

### Jinja

### Base Configuration

#### Packages

By default Curvenote templates make available the following base packages, which are defined in [package-base.def](curvenote_template/defs/package-base.def)

#### Package Options

Curvenote templates use the `\PassOptionsToPackage` macro in order to forward options to packages without generating options warnings. Base options are defined in [passopts-base.def](defs/passopts-base.def)

- normalem: ulem
- inputenc: utf8
