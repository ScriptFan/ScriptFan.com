#!/usr/bin/env python
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from scriptfan import app

if __name__ == "__main__":
    app.run(debug=True)
