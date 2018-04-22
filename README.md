Dedupy
======

Python utility to find and remove duplicate files by hash.

```
usage: dedu.py [-h] [-r] [-d] [-f] source target

Deduplicate files by hash.

positional arguments:
  source         read-only source directory to compare files against
  target         target directory to compare and remove duplicate files

optional arguments:
  -h, --help     show this help message and exit
  -r, --recurse  compare files in subdirectories
  -d, --delete   delete duplicate files in target directory
  -f, --force    delete files without asking for confirmation
```
