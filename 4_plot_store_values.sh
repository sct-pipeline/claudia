#!/bin/bash
#
# This script extracts the metrics and save them as csv files or plots.
#
# NB: add the flag "-x" after "!/bin/bash" for full verbose of commands.
# Charley Gros 2018-09-12
# Modified: 2018-09-12

if [ ! -d "${PATH_RESULTS}" ]; then
	mkdir ${PATH_RESULTS}
fi

cd ${PATH_SCRIPTS}
source sct_launcher
python metrics.py ${PATH_DATA} ${SUBJECT} ${PATH_RESULTS}