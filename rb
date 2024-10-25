#!/bin/bash
# rb: A script to call main.py in tool-suite/rescuebox with all passed arguments

# Call the Python file with the same arguments passed to ./rb
python3 -m rescuebox.main "$@"