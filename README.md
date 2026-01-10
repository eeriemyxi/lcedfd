# Lcedfd
Short for Leetcode Editorial Finder.

This program uses data from the
[leetcode-screenshotter](https://github.com/akhilkammila/leetcode-screenshotter)
project to facilitate ease of use in finding editorials for LeetCode questions
without an account.

# Examples
```yaml
sh-5.3$ lcedfd --no-open Stack
      id: 155
    name: Min Stack
    link: https://github.com/akhilkammila/leetcode-screenshotter/tree/main/editorial-screenshots/1-999/155.%20Min%20Stack.png
      id: 716
    name: Max Stack
    link: https://github.com/akhilkammila/leetcode-screenshotter/tree/main/editorial-screenshots/1-999/716.%20Max%20Stack.png
      id: 895
    name: Maximum Frequency Stack
    link: https://github.com/akhilkammila/leetcode-screenshotter/tree/main/editorial-screenshots/1-999/895.%20Maximum%20Frequency%20Stack.png
      id: 946
    name: Validate Stack Sequences
    link: https://github.com/akhilkammila/leetcode-screenshotter/tree/main/editorial-screenshots/1-999/946.%20Validate%20Stack%20Sequences.png
      id: 225
    name: Implement Stack using Queues
    link: https://github.com/akhilkammila/leetcode-screenshotter/tree/main/editorial-screenshots/1-999/225.%20Implement%20Stack%20using%20Queues.png
```

By default it will automatically open the first result on your default web
browser. You can disable that with `-N` or `--no-open` flag.

```yaml
sh-5.3$ lcedfd https://leetcode.com/problems/unique-paths/
INFO: Detected LeetCode link, parsing it as: 'unique-paths'
      id: 62
    name: Unique Paths
    link: https://github.com/akhilkammila/leetcode-screenshotter/tree/main/editorial-screenshots/1-999/062.%20Unique%20Paths.png
      id: 63
    name: Unique Paths II
    link: https://github.com/akhilkammila/leetcode-screenshotter/tree/main/editorial-screenshots/1-999/063.%20Unique%20Paths%20II.png
      id: 980
    name: Unique Paths III
    link: https://github.com/akhilkammila/leetcode-screenshotter/tree/main/editorial-screenshots/1-999/980.%20Unique%20Paths%20III.png
INFO: Opened link='https://github.com/akhilkammila/leetcode-screenshotter/tree/main/editorial-screenshots/1-999/062.%20Unique%20Paths.png' in your browser
```
LeetCode links are also accepted.


```yaml
sh-5.3$ lcedfd 98
      id: 98
    name: Validate Binary Search Tree
    link: https://github.com/akhilkammila/leetcode-screenshotter/tree/main/editorial-screenshots/1-999/098.%20Validate%20Binary%20Search%20Tree.png
INFO: Opened link='https://github.com/akhilkammila/leetcode-screenshotter/tree/main/editorial-screenshots/1-999/098.%20Validate%20Binary%20Search%20Tree.png' in your browser
sh-5.3$ Opening in existing browser session.
```

Natural number inputs are inferred as ID. You can also try `--by-id` flag to
explicitly use the ID searcher.

# Installation
> [!IMPORTANT]
> Installation of [Git](https://git-scm.com/) is required.

```
pip install git+https://github.com/eeriemyxi/lcedfd
```

## Install from Source
```
git clone --depth 1 https://github.com/eeriemyxi/lcedfd
cd lcedfd
pip install .
```

# Command-line Arguments
```
sh-5.3$ lcedfd --help
usage: lcedfd [-h] [--by-id BY_ID] [-o | --open | --no-open] [--version] [query]

Search lceds database

positional arguments:
  query                 Search text/id/link (inferred)

optional arguments:
  -h, --help            show this help message and exit
  --by-id BY_ID         Find a single entry by ID (overrides query)
  -o, --open, --no-open
                        Open the first result in a web browser (default: True)
  --version             show program's version number and exit
```
