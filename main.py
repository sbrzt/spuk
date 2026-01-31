# main.py

from src.builder import SiteBuilder

if __name__ == "__main__":
    builder = SiteBuilder()
    builder.run_full_build()