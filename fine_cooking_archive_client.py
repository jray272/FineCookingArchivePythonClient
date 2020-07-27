#!/usr/bin/env python3

import argparse
import os.path
import sqlite3

FINE_COOKING_DB_PATH = '/Applications/Fine Cooking Archive/Data-FC/DB/FC.db'

FINE_COOKING_ISSUES_DIR = '/Applications/Fine Cooking Archive/Data-FC/Issues/'

ISSUE_ID_COLUMN = 'c1ISSUE_ID'
PAGE_NUMBER_COLUMN = 'c2PAGE_NUMBER'
MONTH_COLUMN = 'MONTH_'
YEAR_COLUMN = 'YEAR_'
PDF_COLUMN = 'PDF_'
PAGE_TEXT = 'c3PAGE_TEXT'

CONTEXT_CHARACTER_COUNT = 40

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
sql_query = """SELECT c1ISSUE_ID, c2PAGE_NUMBER, MONTH_, YEAR_, PDF_, c3PAGE_TEXT FROM ALL_PAGES_content INNER JOIN ISSUES ON ALL_PAGES_content.c1ISSUE_ID = ISSUES.ID WHERE c3PAGE_TEXT like ? ORDER BY c1ISSUE_ID"""

c.execute(sql_query, (fuzzy_query,))

rows = c.fetchall()

header_format = '{:>13}' * 5

print('Printing matches:')
print(header_format.format(*rows[0].keys()))

for i, row in enumerate(rows):
  row_format = '{:>13}' * 4
  lower_page_text = row[PAGE_TEXT].lower()
  page_text = row[PAGE_TEXT]
  search_query_start_location = lower_page_text.find(args.search_query.lower())
  search_query_end_location = search_query_start_location + len(args.search_query)

  min_context_slice = max(0, search_query_start_location - CONTEXT_CHARACTER_COUNT)
  max_context_slice = min(search_query_end_location + CONTEXT_CHARACTER_COUNT, len(page_text))

  context_text = page_text[min_context_slice:search_query_start_location] + '*' + page_text[search_query_start_location:search_query_end_location] + '*' + page_text[search_query_end_location:max_context_slice]

  row_format += '{:>{length}s}'.format(context_text, length=len(context_text) + 1)

  display_row = (row[ISSUE_ID_COLUMN], row[PAGE_NUMBER_COLUMN], row[MONTH_COLUMN], row[YEAR_COLUMN])
  print(row_format.format(*display_row[:]))

conn.close()
