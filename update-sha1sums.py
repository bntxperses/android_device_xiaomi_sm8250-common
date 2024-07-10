#!/usr/bin/env python
#
# Copyright (C) 2016 The CyanogenMod Project
# Copyright (C) 2017-2020 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import sys
from hashlib import sha1

device = 'sm8250-common'
vendor = 'xiaomi'

def process_file(file_name, cleanup_mode=False):
    with open(file_name, 'r') as f:
        lines = f.read().splitlines()

    vendorPath = '../../../vendor/' + vendor + '/' + device + '/proprietary'
    needSHA1 = False

    def cleanup():
        for index, line in enumerate(lines):
            # Skip empty or commented lines
            if len(line) == 0 or line[0] == '#' or '|' not in line:
                continue

            # Drop SHA1 hash, if existing
            lines[index] = line.split('|')[0]

    def update():
        nonlocal needSHA1
        for index, line in enumerate(lines):
            # Skip empty lines
            if len(line) == 0:
                continue

            # Check if we need to set SHA1 hash for the next files
            if line[0] == '#':
                needSHA1 = (' - from' in line)
                continue

            if needSHA1:
                # Remove existing SHA1 hash
                line = line.split('|')[0]

                filePath = line.split(';')[0].split(':')[-1]
                if filePath[0] == '-':
                    filePath = filePath[1:]

                with open(os.path.join(vendorPath, filePath), 'rb') as f:
                    hash = sha1(f.read()).hexdigest()

                lines[index] = '%s|%s' % (line, hash)

    if cleanup_mode:
        cleanup()
    else:
        update()

    with open(file_name, 'w') as file:
        file.write('\n'.join(lines) + '\n')

if len(sys.argv) == 2 and sys.argv[1] == '-c':
    cleanup_mode = True
else:
    cleanup_mode = False

process_file('proprietary-files.txt', cleanup_mode)
process_file('proprietary-files-phone.txt', cleanup_mode)
