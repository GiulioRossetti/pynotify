# pynotify
PyNotify is a Python decorator designed to notify via email the termination (and eventual stacktrace in case of failure) of a function.

N.B.: It support only Gmail accounts for both sender and recipients.

### Installation

PyNotify is available (for Python 2.7 and 3.x) through pip.

```bash
pip install pynotify
```

### Usage Example

``` 
from pynotify import pynotify as pn

@pn.ExecutionNotifierDecorator('your.email@gmail.com', 'your_password', ['recipient1@gmail.com', 'recipient2@gmail.com'])
def hello():
	print "Hello world!"
	
hello()
```

