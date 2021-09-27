#!/bin/bash
for filename in ./*.zip; do
  mkdir "${filename%.*}"
  cd "${filename%.*}"
  unzip ../"$filename"
  cd ../
done
