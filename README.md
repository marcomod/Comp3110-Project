# COMP 3110 LHDiff

We're building a Python version of LHDiff, a language-independent tool that maps source lines between two versions of a file.

## Run the starter

Use Python 3.9 or newer. The starter uses only the standard library. From the repo root, pass the paths to two UTF-8 text files.

```sh
python3 lhdiff.py old.txt new.txt
```

The command prints one mapping per line. For example, `4-5` maps line 4 in the old file to line 5 in the new file.

## Progress

- [x] Normalize case and whitespace, then use `difflib` to find unchanged lines in order and collect unmatched line numbers.
- [ ] Shortlist candidates with SimHash and score them by content and context.
- [ ] Detect lines that split across multiple lines in the new file.
- [ ] Evaluate on existing benchmarks and a new dataset covering at least 25 different files.

## Team

Marco Modestino, Matteo Muscat, Zihe Zhao, and Christopher Chalmers.

The tentative deadline is December 15.
