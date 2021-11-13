#!/bin/python

import os
import sys
import re
import subprocess


RUN_PATTERN = re.compile(
    r'^<!\-\-\-?\s+#RUN\s+(?P<var>[a-zA-Z_][a-zA-Z0-9_]*)\s+(?P<cmd>.+)\s+\-\->')

ECHO_BEGIN_PATTERN = re.compile(
    r'^<!\-\-\-?\s+#ECHO\s+(?P<var>[a-zA-Z_][a-zA-Z0-9_]*)\s+\{\s+\-\->')

ECHO_END_PATTERN = re.compile(
    r'^<!\-\-\-?\s+#ECHO\s+\}\s+\-\->')


def handle_file(in_file, out_file):
    env = os.environ.copy()
    skip_line = False
    within_code_block = False

    with open(in_file, 'r') as f:
        lines = f.read().splitlines()

    out_file_lines = []
    for line in lines:
        if line.startswith('```'):
            within_code_block = not within_code_block

        if skip_line and not within_code_block:
            match = ECHO_END_PATTERN.match(line)
            if match:
                skip_line = False
                out_file_lines.append(line)
            continue

        if skip_line:
            continue

        if within_code_block:
            out_file_lines.append(line)
            continue

        match = RUN_PATTERN.match(line)
        if match:
            result = subprocess.run(match.group(
                'cmd').replace('\\\\', '\\'), shell=True, text=True, check=True, stdout=subprocess.PIPE, env=env)
            env[match.group('var')] = result.stdout
            out_file_lines.append(line)
            continue

        match = ECHO_BEGIN_PATTERN.match(line)
        if match:
            skip_line = True
            out_file_lines.append(line)
            new_lines = env.get(match.group('var'), '').splitlines()
            for new_line in new_lines:
                out_file_lines.append(new_line)
            continue

        out_file_lines.append(line)

    with open(out_file, 'w') as f:
        for line in out_file_lines:
            f.write(line + '\n')


def main(roots):
    for root in roots:
        if os.path.isfile(root):
            handle_file(root, root)
            continue

        for path, dirs, files in os.walk(root):
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(path, file)
                    handle_file(file_path, file_path)


if __name__ == '__main__':
    main(sys.argv[1:])
