#!/usr/bin/env python3

import argparse
import os.path
import sqlite3

FINE_COOKING_DB_PATH = '/Applications/Fine Cooking Archive/Data-FC/DB/FC.db'

FINE_COOKING_ISSUES_DIR = '/Applications/Fine Cooking Archive/Data-FC/Issues/'


parser = argparse.ArgumentParser(description='Python based client for the Fine Cooking archive')
parser.add_argument('search_query', type=str, help='The term you want to search for in the database')
parser.add_argument('--database_path', type=str, default=FINE_COOKING_DB_PATH, help='Path to FC.db. Default path: {}'.format(FINE_COOKING_DB_PATH))
parser.add_argument('--issues_dir', type=str, default=FINE_COOKING_ISSUES_DIR, help='Path to the directory that contains all of the Fine Cooking issues. Default path: {}'.format(FINE_COOKING_ISSUES_DIR))

args = parser.parse_args()

if not os.path.exists(args.database_path):
  print('Database file {} does not exist, exiting'.format(args.database_path))
  exit(1)

conn = sqlite3.connect(args.database_path)
conn.row_factory = sqlite3.Row

c = conn.cursor()

# This is how you get fuzzy matches to be accepted by the SQL code placeholder.
fuzzy_query = '%{}%'.format(args.search_query)
sql_query = """SELECT docid, c0ID, c1ISSUE_ID, c2PAGE_NUMBER FROM ALL_PAGES_content where c3PAGE_TEXT like ? ORDER BY c1ISSUE_ID"""

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
