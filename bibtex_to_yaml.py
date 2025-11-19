#!/usr/bin/env python3
import sys
import yaml
import bibtexparser
import re


def clean_field(value: str) -> str:
    """
    Remove outer { } used in BibTeX to preserve capitalization,
    but keep internal braces (e.g. math) untouched.
    """
    value = value.strip()
    # Remove leading/ending braces ONLY if they wrap the whole string
    if value.startswith("{") and value.endswith("}"):
        value = value[1:-1]
    return value.replace("{", "").replace("}", "")


def split_authors(author_field: str):
    """
    Split a BibTeX 'author' field on ' and '.
    """
    return [a.strip() for a in author_field.replace("\n", " ").split(" and ") if a.strip()]


def parse_name(name: str):
    """
    Parse BibTeX names into (given, family).
    Handles:
      - "Last, First Middle"
      - "First Middle Last"
    """
    if "," in name:
        family, given = [s.strip() for s in name.split(",", 1)]
    else:
        parts = name.split()
        if len(parts) == 1:
            given, family = "", parts[0]
        else:
            given = " ".join(parts[:-1])
            family = parts[-1]
    return given, family


def bibtex_to_yaml(bibtex_text: str) -> str:
    db = bibtexparser.loads(bibtex_text)
    entries_yaml = []

    for entry in db.entries:
        out = {}

        out["id"] = entry.get("ID")
        out["type"] = entry.get("ENTRYTYPE")

        # Clean selected fields
        for field in (
            "title", "journal", "booktitle", "year", "volume",
            "number", "pages", "publisher", "doi"
        ):
            if field in entry:
                out[field] = clean_field(entry[field])

        # Authors
        if "author" in entry:
            authors_yaml = []
            for raw in split_authors(entry["author"]):
                given, family = parse_name(raw)
                full_name = (given + " " + family).strip()
                authors_yaml.append(full_name)
            out["authors"] = authors_yaml

        entries_yaml.append(out)

    # Dump YAML normally
    raw = yaml.safe_dump(entries_yaml, sort_keys=False, allow_unicode=True)

    # Add a blank line between top-level entries
    raw = raw.replace("- id:", "\n- id:").lstrip()

    return raw


if __name__ == "__main__":
    bibtext = sys.stdin.read()
    print(bibtex_to_yaml(bibtext), end="")
