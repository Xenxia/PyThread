# PyThread
Thread parelle func

#Exemple

```Python
task = ThreadUP(target=func, args=(2,), returnValue=True)
task.start()
myReturnValue = task.join()
```
