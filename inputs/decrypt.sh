#!/bin/bash
if [[ -z "$SECRET" || -z "$INPUT_LOC" || -z "$OUTPUT_LOC" ]]; then
	  echo "Error: One or more required variables are not set."
	  exit 1
fi

crypt4gh decrypt --sk $SECRET < $INPUT_LOC > $OUTPUT_LOC