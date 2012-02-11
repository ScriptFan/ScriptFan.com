#!/usr/bin/env python
from scriptfan import create_app

app = create_app("scriptfan.cfg")

if __name__ == "__main__":
    app.run(debug=True)
