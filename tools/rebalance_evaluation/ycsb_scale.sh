#!/bin/bash


../motivation/stopall.sh
for letter in {a..f}
do
  echo YCSB workload: $letter
  ./seek_and_insert.sh $letter
  ./compact_and_merge.sh $letter
  ./level_migration.sh $letter
done

