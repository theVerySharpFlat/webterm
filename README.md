# Webterm

A terminal emulator with a static HTML/CSS/JS frontend and a python backend.

## How it works
The frontend is a react app that uses xtermjs to bring a terminal emulator to the user. The backend is a python script that hosts an ASGI server using uvicorn. The frontend and backend communicate through socketio. The backend sends tty output to the frontend and the frontend sends user input back in a loop. Technically you can modify the script and host this project on your own domain to give your users access to a terminal. However, I would strongly recommend against this as no thought has been put into security. Instead, you should host it locally.

## Building
```bash
$ chmod +x ./build.sh
$ ./build.sh
...
```

## Run
```bash
$ cd build
$ chmod +x ./run.py
$ ./run.py # alternatively, you could host the frontend and backend in seperate processes
```

**NOTE**: The `backend/main.py` script with install the uvicorn and python-socketio packages automatically if they are not found. You could install them yourself if you wish. If you get an error while installing uvicorn, try upgrading pip.

## Configuration
In the build directory, modify the backend-config.json to change the shell used and the ports that the backend and frontend are hosted on.
