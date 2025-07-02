<img src="static/img/logo.png" alt="logo" width="100"/>

# SPUK (Static PUblisher of Knowledge)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15389756.svg)](https://doi.org/10.5281/zenodo.15389756)

## Description

SPUK is a Static Site Generator (SSG) designed for RDF Knowledge Graphs. It transforms RDF data into a browsable, static HTML website.

## Installation

1. Create a virtual environment to manage the project's dependencies:

    ```bash
    python -m venv venv
    ```

2. Activate the virtual environment:

    * On Windows:
    
        ```
        .\venv\Scripts\activate
        ```

    * On macOS and Linux:

        ```
        source venv/bin/activate
        ```

3. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

## Usage

SPUK generates static HTML pages from an RDF Knowledge Graph (KG), allowing users to explore the data through a web browser.

### Start the site

If you are launching the code for the first time, before running the main script, make it executable:

    chmod +x main.sh

Start the static site generator:

    ./main.sh

The website will be available at: http://127.0.0.1:8001.

### Examples

...

## Testing

SPUK uses unit tests to ensure code quality and correctness.

If you are launching the testing units for the first time, make the test script executable:

    chmod +x test.sh

Run the test suite with:

    ./test.sh

## Roadmap

- **Entity**
    - [ ] add graph visualization
    - [ ] add directed properties
    - [ ] add triples in which the entity is the object
- **Index**
    - [ ] add functioning pagination
    - [ ] add better way to list entities
    - [ ] add better data visualization
        - [ ] add info not requiring the hover
        - [ ] add download
        - [ ] define personalized data graphs from a defined set through config file
    - [ ] add list properties as well?
- **Documentation**
    - [ ] handle documentation pages
- **Query**
    - [ ] handle query page
    - [ ] manage sparql queries through config file
- **General**
    - [X] codebase reengineering
    - [X] add config file
    - [ ] add smarter dev environment
        - [X] add dev server with file watching and caching
        - [ ] add auto-reload at change
        - [ ] add configuration parameters for dev
    - [ ] design better footer
    - [ ] add API for handling more complex scenarios?

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