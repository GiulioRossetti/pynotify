# pynotify
PyNotify is a Python decorator designed to notify via email the termination (and eventual stacktrace in case of failure) of a function.

N.B.: It support only Gmail accounts for both sender and recipients.

### Installation

PyNotify is available (for Python 2.7 and 3.x) through pip.

```bash
pip install pynotify
```

### Usage Example

``` python
from pynotify import pynotify as pn

@pn.ExecutionNotifierDecorator('your.email@gmail.com', 'your_pwd', ['rcp1@gmail.com', 'rcp2@gmail.com'])
def hello():
	print "Hello world!"
	
hello()
```

