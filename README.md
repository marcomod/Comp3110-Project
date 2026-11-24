# COMP 3110 LHDiff

We're building a Python version of LHDiff, a language-independent tool that maps source lines between two versions of a file.

## Run the starter

Use Python 3.9 or newer. The starter uses only the standard library. From the repo root, pass the paths to two UTF-8 text files.

```sh
python3 lhdiff.py old.txt new.txt
```

The command prints one mapping per line. For example, `4-5` maps line 4 in the old file to line 5 in the new file.

In Python, `lhdiff.match_lines(old_lines, new_lines)` takes two lists of lines and returns 1-based `(old_line, new_line)` pairs.

## Progress

- [x] Normalize case and whitespace, then use `difflib` to find unchanged lines in order and collect unmatched line numbers.
- [ ] Shortlist candidates with SimHash and score them by content and context.
- [ ] Detect lines that split across multiple lines in the new file.
- [ ] Evaluate on existing benchmarks and a new dataset covering at least 25 different files.

## Team

- **Marco Modestino** owns SimHash candidate search, match resolution, integration, existing benchmark setup, and the evaluation write-up.
- **Matteo Muscat** owns content and context similarity scoring.
- **Zihe Zhao** owns line split detection.
- **Christopher Chalmers** owns the evaluation runner and its comparison of predicted and expected mappings.

Everyone contributes labeled file pairs for the new dataset.

The tentative deadline is December 15.
