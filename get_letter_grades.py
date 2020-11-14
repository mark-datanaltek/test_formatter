#!/usr/bin/env python

from functools import partial
import pandas as pd

def get_categories(categories_file):
  # expect headers of letter-grade, min, max
  categories = pd.read_csv(categories_file, sep='\t')
  for indx in range(len(categories) - 1):
    err_msg = "min/max mismatch on:\n{0}\n{1}".format(
      categories.iloc[indx], categories.iloc[indx+1]
    )
    if categories.iloc[indx]["min"] != categories.iloc[indx+1]["max"]:
      raise ValueError(err_msg)

  return categories

def get_num_grades(num_grades_file):
  # expect header of lastname, firstname, course-num-grade
  num_grades = pd.read_csv(num_grades_file, sep='\t', skip_blank_lines=True)
  return num_grades

def categorize(row, categories):
  result = categories[(categories["min"] <= row["course-num-grade"]) & (row["course-num-grade"] < categories["max"])]["letter-grade"].values[0]
  return result

def get_letter_grades(num_grades, categories):
  #num_grades["course-letter-grade"] = num_grades.apply(lambda r: categorize(r, categories), axis=1)
  num_grades["letter-grade"] = num_grades.apply(lambda r: categorize(r, categories), axis=1)
  return num_grades


if __name__ == "__main__":
  import argparse

  parser = argparse.ArgumentParser(description="get letter grades for numerical grades",
          formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--categories", "-c", default="grade_categories.txt", help="grade_categories file")
  parser.add_argument("--num_grades", "-n", default="num_grades.txt", help="number grades file")
  parser.add_argument("--categorized_grades", "-g", default="categorized_grades.txt", help="output categorized grades file")
  args = parser.parse_args()

  categories = get_categories(args.categories)
  num_grades = get_num_grades(args.num_grades)
  categorized_grades = get_letter_grades(num_grades, categories)
  categorized_grades.to_csv(args.categorized_grades, sep='\t', index=False)
