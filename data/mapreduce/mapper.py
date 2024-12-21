#!/usr/bin/env python3

import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split(";")
    
    if len(fields) != 3:
        continue
    
    user_id, isbn, rating = fields
    
    print(f"{isbn}\t{user_id}")