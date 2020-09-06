#!/usr/bin/env python3

import argparse
import os.path
import sqlite3
import traceback

FINE_COOKING_DB_PATH = '/Applications/Fine Cooking Archive/Data-FC/DB/FC.db'

FINE_COOKING_ISSUES_DIR = '/Applications/Fine Cooking Archive/Data-FC/Issues/'

ISSUE_ID_COLUMN = 'c1ISSUE_ID'
PAGE_NUMBER_COLUMN = 'c2PAGE_NUMBER'
MONTH_COLUMN = 'MONTH_'
YEAR_COLUMN = 'YEAR_'
PDF_COLUMN = 'PDF_'
PAGE_TEXT = 'c3PAGE_TEXT'

CONTEXT_CHARACTER_COUNT = 40

FULL_SQL_QUERY = """SELECT c1ISSUE_ID, MONTH_, YEAR_, c2PAGE_NUMBER, PDF_, c3PAGE_TEXT FROM ALL_PAGES_content INNER JOIN ISSUES ON ALL_PAGES_content.c1ISSUE_ID = ISSUES.ID WHERE c3PAGE_TEXT like ? ORDER BY c1ISSUE_ID"""

COUNT_SQL_QUERY = """SELECT COUNT(docid) as hit_count, c1ISSUE_ID, MONTH_, YEAR_ FROM ALL_PAGES_content INNER JOIN ISSUES ON ALL_PAGES_content.c1ISSUE_ID = ISSUES.ID WHERE c3PAGE_TEXT like "%red pepper%" GROUP BY c1ISSUE_ID ORDER BY hit_count DESC"""


def Help(args, cursor):
  print('This script allows the user to search through the Fine Cooking archive')
  print('In general, the best way to learn about a particular command is to add --help to the command line. For example, if you wanted to learn more about the "search" command, just do: script.py search --help')


SEARCH_TEXT_COLUMN_FORMAT = '{:>14}'

def SearchText(args, cursor):
  search_query = args.search_query
  first_search_query = search_query[0]

  # This is how you get fuzzy matches to be accepted by the SQL code placeholder.
  fuzzy_query = '%{}%'.format(first_search_query)

  cursor.execute(FULL_SQL_QUERY, (fuzzy_query,))

  rows = cursor.fetchall()

  header_format = SEARCH_TEXT_COLUMN_FORMAT * 5

  if len(rows) == 0:
    print('Search query {} returned no results'.format(first_search_query))
    return

  print('Printing matches:')
  print(header_format.format(*rows[0].keys()))

  for i, row in enumerate(rows):
    row_format = SEARCH_TEXT_COLUMN_FORMAT * 4
    lower_page_text = row[PAGE_TEXT].lower()
    page_text = row[PAGE_TEXT]
    search_query_start_location = lower_page_text.find(first_search_query.lower())
    search_query_end_location = search_query_start_location + len(first_search_query)

    min_context_slice = max(0, search_query_start_location - CONTEXT_CHARACTER_COUNT)
    max_context_slice = min(search_query_end_location + CONTEXT_CHARACTER_COUNT, len(page_text))

    context_text = page_text[min_context_slice:search_query_start_location] + '*' + page_text[search_query_start_location:search_query_end_location] + '*' + page_text[search_query_end_location:max_context_slice]

    row_format += '{:>{length}s}'.format(context_text, length=len(context_text) + 1)

    display_row = (row[ISSUE_ID_COLUMN], row[PAGE_NUMBER_COLUMN], row[MONTH_COLUMN], row[YEAR_COLUMN])
    print(row_format.format(*display_row[:]))


def SearchArticles(args, cursor):
  print('Unimplemented')


parser = argparse.ArgumentParser(description='Python based client for the Fine Cooking archive')

subparsers = parser.add_subparsers(help='Command to perform on the Fine Cooking Archive')

help_parser = subparsers.add_parser('help', help='Use this command to print out a small tutorial')
help_parser.set_defaults(func=Help)

search_parser = subparsers.add_parser('search', help='Search through a particular portion of the database')

search_subparser = search_parser.add_subparsers(help='The portion of the database that you would like to search through.')

def AddSearchQueryArgumentToParser(parser):
  parser.add_argument('search_query', help='The search query that you would like to use to search through the database, eg "rosemary"', nargs='+')


text_parser = search_subparser.add_parser('text', help='Searches through all of the text in all of the Fine Cooking magazine issues and prints out where your search query appears in each issue along with a little context around where that text occurs.')
text_parser.set_defaults(func=SearchText)
AddSearchQueryArgumentToParser(text_parser)

articles_parser = search_subparser.add_parser('articles', help='Searches through all article headlines, sub-headlines, and abstracts for the search query and returns where any hits can be found. Note that recipes are a subset of articles, so use this cateogry may be used to search through recipes.')
articles_parser.set_defaults(func=SearchArticles)
AddSearchQueryArgumentToParser(articles_parser)


parser.add_argument('--database_path', type=str, default=FINE_COOKING_DB_PATH, help='Path to FC.db. Default path: {}'.format(FINE_COOKING_DB_PATH))
parser.add_argument('--issues_dir', type=str, default=FINE_COOKING_ISSUES_DIR, help='Path to the directory that contains all of the Fine Cooking issues. Default path: {}'.format(FINE_COOKING_ISSUES_DIR))

args = parser.parse_args()

if not os.path.exists(args.database_path):
  print('Database file {} does not exist, exiting'.format(args.database_path))
  print()
  parser.print_help()
  exit(1)

conn = sqlite3.connect(args.database_path)
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

# TODO: Handle multiple search queries.
if len(args.search_query) != 1:
  print('WARNING: only a single search term is supported at this time. The '
        'following search terms are being ignored: {}', search_query[1:])
  print('If you have a multi-word search term that you would like to search '
        'for, try wrapping it in quotation marks. For example, ... search '
        'text "Red pepper"')

try:
  args.func(args, cursor)
except Exception as e:
  print('Toplevel Exception:', str(e))
  track = traceback.format_exc()
  print(track)

conn.close()
