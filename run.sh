#!/bin/bash


# # Windows
# ./backend/env/Scripts/activate

# activate env and start backend
source ./backend/env/bin/activate
python ./backend/app.py &

# start frontend
cd frontend
npm run serve