#!/bin/bash
#
# This is a wrapper to processing scripts, that loops across subjects.
#
# Usage:
#   ./run_process.sh <script>
#
# Example:
#   ./run_process.sh 1_label_data.sh
#
# Note:
#   Make sure to edit the file parameters.sh with the proper list of subjects and variable.
#
# NB: add the flag "-x" after "!/bin/bash" for full verbose of commands.
# Charley Gros 2018-05-13
# modified: 2018-09-12

# Load parameters
source parameters.sh
 
# build syntax for process execution
PATH_PROCESS=`pwd`/$1
 
# Loop across subjects
for subject in ${SUBJECTS[@]}; do
	# Display stuff
	echo "Processing subject: ${subject}"
	# go to subject folder
	cd ${PATH_DATA}${subject}
	export SUBJECT=${subject}
	if [ "$1" == "4_plot_store_values.sh" ]; then
		$PATH_PROCESS ${subject}
	else
		for scan in ${SCANS[@]}; do
			if [ -d "${scan}" ]; then
				cd ${scan}
				echo -e "\tProcessing scan: ${scan}"
				export SCAN=${scan::-1}
				# run process
				$PATH_PROCESS ${subject}${scan}
				cd ..
			fi
		done
	fi
done
