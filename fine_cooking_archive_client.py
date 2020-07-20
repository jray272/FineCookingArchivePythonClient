#!/usr/bin/env python3

import sys
import sqlite3


if len(sys.argv) != 2:
  print('Usage: python3 script.py <search term>')
  exit(1)

query = sys.argv[1]

FINE_COOKING_DB = '/Applications/Fine Cooking Archive/Data-FC/DB/FC.db'

FINE_COOKING_ISSUES_DIR = '/Applications/Fine Cooking Archive/Data-FC/Issues/'

conn = sqlite3.connect(FINE_COOKING_DB)
conn.row_factory = sqlite3.Row

c = conn.cursor()

# This is how you get fuzzy matches to be accepted by the SQL code placeholder.
fuzzy_query = '%{}%'.format(query)
sql_query = """SELECT docid, c0ID, c1ISSUE_ID, c2PAGE_NUMBER FROM ALL_PAGES_content where c3PAGE_TEXT like ? ORDER BY c1ISSUE_ID"""

print(sql_query)

print('Printing matches:')

c.execute(sql_query, (fuzzy_query,))

rows = c.fetchall()

row_format = '{:>15}' * (len(rows[0]) + 1)

print(row_format.format('', *rows[0].keys()))

for i, row in enumerate(rows):
  if i == 0:
    print(row.keys())
  print(row[:])

conn.close()
