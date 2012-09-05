#!/usr/bin/env python
import hashlib

def hashPassword(password):
    return hashlib.md5(password).hexdigest()
