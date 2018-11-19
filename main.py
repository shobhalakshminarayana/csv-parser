# main.py
#
# A simple script that help convert CSV file

import csv
import re
from copy import deepcopy
# Script settings
SOURCE_FILE_NAME='convertcsv.csv'
OUTPUT_FILE_NAME='result.csv'
COMMENT_FIELD_NAME_PREFIX='Comment'

# Pre-compile the regex to make things faster
field_name_re = re.compile(r'History/(ArtifactHistory|HistoryChangeSet)/[0-9]+/.*')
# Values that we would like to push to output file
output_data = []
with open(SOURCE_FILE_NAME, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Final data that we will use for the last column
        row_parsed_data = {
            'Artifact': [],
            'ChangeSet': [],
        }
        for key, value in row.items():
            if len(value) and field_name_re.match(key):
                key_parts = key.split('/')
                # The actual name which correspond to this column in our CSV
                field_name = key_parts[-1]

                # The number that corresopnd to order of changes - lol - hard to explain that
                # The regex guarantee that this is a number
                field_counter_id = int(key_parts[-2])

                history_type = key_parts[1].replace('History', '', 1)

                if field_counter_id >= len(row_parsed_data[history_type]):
                    row_parsed_data[history_type].append([])

                row_parsed_data[history_type][field_counter_id].append('{}: {}'.format(
                    field_name,
                    value
                ))

        # print(row_parsed_data)
        for comment_type in ['Artifact', 'ChangeSet']: # Hardcoded huh - Terrible
            comment_line_val = row_parsed_data[comment_type]
            comment_lines = []
            for i, val in enumerate(comment_line_val):
                comment_lines.append('{} {}'.format(
                    str(i),
                    '; '.join(val))
                )

            comment_field_value = '{}'.format(
                '\n'.join(comment_lines)
            )

            comment_field_name = '{}{}'.format(
                COMMENT_FIELD_NAME_PREFIX,
                comment_type
            )

            row.update({comment_field_name: comment_field_value})
            row.move_to_end(comment_field_name, last=True)

        # Copy this now
        output_data.append(deepcopy(row))
        # break

# print(output_data)
# Great, now output it
with open(OUTPUT_FILE_NAME, 'w') as csvfile:
    field_names = [k for k in output_data[0].keys() if not field_name_re.match(k)]
    # field_names = ['CommentArtifact', 'CommentChangeSet']
    writer = csv.DictWriter(csvfile, fieldnames=field_names, extrasaction='ignore')
    writer.writeheader()
    for row in output_data:
        writer.writerow(row)
