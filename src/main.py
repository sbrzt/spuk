from functions import generate_page, generate_pages_recursive, copy_static
import sys


def main():
    copy_static("static", "docs")
    if sys.argv[0]:
        basepath = sys.argv[1]
    else:
        basepath ="/"
    generate_pages_recursive(basepath, "content", "content/template.html", "docs")


if __name__ == "__main__":
    main()