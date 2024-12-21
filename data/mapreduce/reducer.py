#!/usr/bin/env python3
import sys

current_isbn = None
users_set = set()

for line in sys.stdin:
    line = line.strip()
    isbn, user_id = line.split("\t")
    users_set.add(user_id)
    
    if current_isbn != isbn:
        if current_isbn is not None:
            print(f"{current_isbn}\t{len(users_set)}")
        current_isbn = isbn
        users_set = {user_id}
        
if current_isbn:
    print(f"{current_isbn}\t{len(users_set)}")