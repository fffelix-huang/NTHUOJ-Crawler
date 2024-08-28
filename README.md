# NTHUOJ Crawler

Crawler for [NTHUOJ](https://acm.cs.nthu.edu.tw/).

## Installation

```
git clone https://github.com/fffelix-huang/NTHUOJ-Crawler.git
cd NTHUOJ-Crawler
pip3 install -r requirements.txt
```

## Usage

Prepare a CSV file with the following format:

| | `<Problem ID 1>` | `<Problem ID 2>` | `<Problem ID 3>` | ... |
| - | - | - | - | - |
| `<Username 1>` |
| `<Username 2>` |
| `<Username 3>` |
| ... |

Suppose the CSV file is called `data.csv`, Run `python3 main.py data.csv`. The output will be in `dump.csv` (you can use the `--dest` flag to specify destination file).

Add `--partial` flag to enable partial scoring.

Run `python3 main.py -h` for more details.
