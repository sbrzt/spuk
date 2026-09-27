<img src="static/img/logo.svg" alt="logo" width="100" height="auto"/>

# SPUK (Static PUblisher of Knowledge)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15389756.svg)](https://doi.org/10.5281/zenodo.15389756)

## Description

SPUK is a Static Site Generator (SSG) designed for RDF Knowledge Graphs. It transforms RDF data into a browsable, static HTML website: entity pages, indexes with pagination and search, data visualizations, a SPARQL query interface, and optional Markdown documentation pages.

## Live Demo

https://sbrzt.github.io/spuk/

## Requirements

* Python >= 3.11
* [uv](https://docs.astral.sh/uv/) for dependency management

## Installation

1. Clone repo and enter it:

    ```bash
    git clone https://github.com/sbrzt/spuk.git
    cd spuk
    ```

2. Install dependencies (uv creates and manages the virtual environment automatically):

    ```bash
    uv sync
    ```

## Configuration

All generation options live in `config.toml`:

* `[graph_source]`: RDF input, either a local `file_path` (turtle, etc.) or a `sparql_endpoint`.
* `[output]`: output/templates/static/documentation directory paths.
* `[modelling]`: RDF property used to type entities.
* `[custom_stats]`: enable and point to a custom stats config (`src/custom_stats/config.yaml`).
* `[data_viz]`: chart parameters (e.g. `n_objects`).
* `[theme.colors]`: site palette (`primary`, `link`, `info`, `success`, `warning`, `danger`, `chart`), each a `#rrggbb` hex string.
* `[theme.hero.*]`: per-page hero: solid color from `theme.colors`, or an image path inside `static/`.
* `[[predefined_queries]]`: SPARQL presets shown on the query page.
* `[graph_vis_options.*]`: layout/physics options for the entity graph visualization.

## Usage

### Full build

Generates the complete static site into the output directory (`build` by default):

```bash
uv run main.py
```

### Development server

Starts a dev server with file watching, auto-reload and a limited entity count for fast rebuilds:

```bash
./dev.sh
```

This runs `uv run server.py`, which watches `static/`, `templates/`, `src/` and `documentation/`, rebuilding only what changed, and serves the site with live reload.

## Testing

Run the test suite with:

```bash
uv run pytest
```

Tests live under `tests/` and cover the RDF loader, entity model, filesystem helpers, path resolver, stats collector and custom stats.

---

## Roadmap

### Indexes & Listings

* [ ] Enhance data visualizations:
  * [ ] Add literal components (datatypes and languages)
  * [ ] Add subject RDF node types
  * [ ] Add object RDF node types
  * [ ] Add combined node types
  * [ ] Add IRI lengths
  * [ ] Add literal lengths
  * [ ] Add most referenced subjects?
  * [ ] Add most referenced objects?
  * [ ] Define personalized data charts via config file
* [ ] Consider listing entity properties

### Documentation

* [ ] Improve internal documentation:
  * [ ] Add docstrings
  * [ ] Add README files

### General Improvements

* [ ] Consider adding API support for advanced use cases
* [ ] Add CITATION.cff

## Author

Barzaghi, Sebastian (https://orcid.org/0000-0002-0799-1527).

## Citation

```
@software{barzaghi_spuk_2025,
  author       = {Sebastian B.},
  title        = {SPUK: v0.1.0},
  month        = may,
  year         = 2025,
  publisher    = {Zenodo},
  version      = {v0.1.0},
  doi          = {10.5281/zenodo.15389756},
  url          = {https://doi.org/10.5281/zenodo.15389756},
  swhid        = {swh:1:dir:13091e52df66e92690aa1f7d9beac02b0d5acaa4
                   ;origin=https://doi.org/10.5281/zenodo.15389755;vi
                   sit=swh:1:snp:26950210a2176283cdda0ea18c9fda2e0318
                   d697;anchor=swh:1:rel:3303c580deefd97c6b78c48c438e
                   ead829256a51;path=sbrzt-spuk-a7d3250
                  },
}
```
