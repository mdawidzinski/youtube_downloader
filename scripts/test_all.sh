#!/bin/bash
printf "\nWill now run Pytest tests\n"
nose2 --with-coverage > results.txt
$content < cat results.txt
# TODO FILTER ONLY TO THOSE LESS, THAN 100%
echo "{$content}" | grep -v '00%$'
printf "\nDONE.\n"