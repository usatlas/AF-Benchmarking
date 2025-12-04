# Quick development

The fastest way to start with development is to use pixi. If you don't have pixi
installed, you can install it by following the instructions at
[pixi documentation](https://pixi.sh). On macOS, you can use
`brew install pixi`.

## Available Environments

This project uses pixi with multiple environments:

- **`docs`** - Documentation building (Python 3.14, mkdocs, plugins)
- **`kibana`** - Parsing and Kibana upload (Python 3.13, elasticsearch)

## Documentation Development

To work on documentation, use the `docs` environment:

```console
$ pixi task list -e docs     # List all available documentation tasks
$ pixi run -e docs build      # Build the documentation
$ pixi run -e docs serve      # Build and serve the docs locally (with auto-reload)
$ pixi run -e docs build-check # Build and validate all links
$ pixi run -e docs validate   # Validate links in the built site
```

You can also pass arguments to customize the config file:

```console
$ pixi run -e docs build --config custom-mkdocs.yml
$ pixi run -e docs serve --config custom-mkdocs.yml
```

## Parsing/Kibana Development

To work on parsing and Kibana integration:

```console
$ pixi shell -e kibana  # Enter the kibana environment shell
$ python parsing/scripts/...  # Run parsing scripts
```

pixi handles everything for you, including setting up a temporary virtual
environment with all required dependencies.

# Setting up a development environment manually

If you prefer not to use pixi, you can set up a development environment by
running:

```bash
python3 -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

Then you can run mkdocs directly:

```bash
mkdocs build  # Build the documentation
mkdocs serve  # Build and serve the docs locally
```

# Post setup

You should prepare pre-commit, which will help you by checking that commits pass
required checks:

```bash
pip install pre-commit # or brew install pre-commit on macOS
pre-commit install # Will install a pre-commit hook into the git repo
```

You can also/alternatively run `pre-commit run` (changes only) or
`pre-commit run --all-files` to check even without installing the hook.

# Building docs

This project uses MkDocs for documentation. The documentation is automatically
built and published via GitHub Pages when changes are pushed to the main branch.

You can build the docs locally using pixi:

```bash
pixi run -e docs build
```

You can see a preview with live reload (great for iterating on documentation):

```bash
pixi run -e docs serve
```

Then open http://127.0.0.1:8000 in your browser.

To validate all links in the documentation:

```bash
pixi run -e docs build-check
```

This will build the documentation without directory URLs and run linkchecker to
validate all links (note: requires a `.linkcheckerrc` configuration file).

# Pre-commit

This project uses pre-commit for all style checking and linting. Install
pre-commit and run:

```bash
pre-commit run -a
```

to check all files.
