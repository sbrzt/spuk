<img src="static/img/logo.jpeg" alt="logo" width="100"/>

# SPUK (Static PUblisher of Knowledge)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15389756.svg)](https://doi.org/10.5281/zenodo.15389756)

## Description

SPUK is a Static Site Generator (SSG) designed for RDF Knowledge Graphs. It transforms RDF data into a browsable, static HTML website.

## Live Demo

https://sbrzt.github.io/spuk/

## Installation

1. Create a virtual environment to manage the project's dependencies:

    ```bash
    TODO
    ```

2. Activate the virtual environment:

    * On Windows:
    
        ```
        .\.venv\Scripts\activate
        ```

    * On macOS and Linux:

        ```
        source .venv/bin/activate
        ```

3. Install the required dependencies:

    ```
    TODO
    ```

## Usage

SPUK generates static HTML pages from an RDF Knowledge Graph (KG), allowing users to explore the data through a web browser.

### Start the site

TODO

### Examples

TODO

## Testing

TODO

Here's a **cleaner, more structured rewrite** of your roadmap that improves clarity, consistency, and focus. The wording is more actionable, and the hierarchy is easier to scan.

---

## 🚧 Roadmap

### 🧠 Entity Pages

* [x] Integrate graph visualization
* [x] Show directed property relationships
* [x] Display subject–property triples

### 📂 Indexes & Listings

* [ ] Implement pagination
* [ ] Implement search functionality
* [ ] Improve entity listing layout
* [ ] Enhance data visualizations:
  * [ ] Show info without requiring hover
  * [ ] Add download option
  * [x] **Test**: Define personalized data stats via config file
  * [ ] **Test**: Define personalized data charts via config file
* [ ] Consider listing entity properties

### 📚 Documentation

* [ ] Add documentation site/pages
* [ ] Improve internal documentation:
  * [ ] Add docstrings
  * [ ] Add README files

### 🔍 Query Interface

* [ ] Create query page
* [ ] Allow SPARQL query presets via config file

### ⚙️ General Improvements

* [x] Reengineer codebase structure
* [x] Introduce centralized config file
* [ ] Improve developer experience:
  * [ ] Add dev server with file watching & caching
  * [ ] Enable auto-reload on changes
  * [ ] Add dev-specific config parameters
* [x] Redesign footer
* [ ] Consider adding API support for advanced use cases

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