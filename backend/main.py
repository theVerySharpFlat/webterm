import os, sys
import struct
import pty, fcntl, termios
import time

CHILD = 0

try:
    pid, fd = pty.fork()
except OsError as e:
    print(f"OSError: {e}")

if pid < 0:
    # error
    print("pty fork error!")
elif pid == CHILD:
    sys.stdout.flush()
    try:
        env = os.environ
        env["TERM"] = "dumb"
        os.execle("/bin/bash", "/bin/bash", env)
    except:
        print("execl failed!")

else:
    fcntl.ioctl(fd, termios.TIOCSWINSZ, struct.pack("HHHH", 900, 900, 0, 0))

    tcattrib = termios.tcgetattr(fd)
    tcattrib[3] = tcattrib[3] & ~termios.ICANON
    termios.tcsetattr(fd, termios.TCSAFLUSH, tcattrib)
    
    os.write(sys.stdout.fileno(), os.read(fd, 1024))
    os.write(fd, b"echo hello\n")
    time.sleep(3)
    os.write(sys.stdout.fileno(), os.read(fd, 2048))