import time
from PyThreadUp import ThreadManager

def func(t):
    for i in range(90000):
        print(i)

    return t
 
tm = ThreadManager()

tm.thread(name="test", target=func, returnValue=True, args=("test thread",))
tm.start("test")
time.sleep(2)
tm.kill("test")
print("k")
time.sleep(2)
tm.start("test")
print(tm.join("test"))


if not tm.is_alive("test"):
    print('thread killed')