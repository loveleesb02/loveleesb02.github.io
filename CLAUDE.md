# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A single-file Python script (`grade.py`) that reads student scores from a CSV and prints each student's average and letter grade. It can also save a bar chart of per-subject averages. There is no build step, linter config, or test suite.

## Commands

```sh
pip install -r requirements.txt     # matplotlib (needed only for --chart)
python grade.py                     # reads grades.csv next to the script
python grade.py other.csv           # reads a different CSV
python grade.py --chart [out.png]   # also saves a per-subject average bar chart (default: subject_averages.png)
```

## Chart

`save_subject_chart()` imports matplotlib inside the function, so the table still works without matplotlib installed. It uses the `Agg` backend and sets `font.family` to `Malgun Gothic`; without that font, Korean labels render as boxes.

## Input format

`grades.csv`: the first row is the header (`이름, 국어, 영어, 수학`); the first column is the student name and every other column is a subject score. Subjects come from the header, so you can add or remove columns without changing code. Values may have a space after each comma (read with `skipinitialspace=True`).

## Windows / Korean encoding

- **Input:** the CSV is decoded as `utf-8-sig` first, then `cp949` (Excel on Korean Windows saves as CP949).
- **Output:** `main()` calls `sys.stdout.reconfigure(encoding="utf-8")`. Without it, output to a pipe or Git Bash is encoded as CP949 and the Korean comes out garbled. Keep this line.
- Column alignment uses `str` format widths, which don't account for the double width of Korean characters, so columns can look slightly misaligned.

## Grading

`to_letter()`: A ≥ 90, B ≥ 80, C ≥ 70, D ≥ 60, otherwise F.
