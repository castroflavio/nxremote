Introduction
============
This package provides a Python API to access [NeXus 
data](http://www.nexusformat.org/) across a network utilizing the Pyro4 package. 

The latest development version is always available from [NeXpy's GitHub
repository](https://github.com/nexpy/nxremote).

Installing and Running
======================
The source code can be downloaded from the NeXpy Git repository:

```
    $ git clone http://github.com/nexpy/nxremote.git
```

To install in the standard Python location:

```
    $ python setup.py install
```

To install in an alternate location:

```
    $ python setup.py install --prefix=/path/to/installation/dir
```

Prerequisites
=============
The following libraries are used by the full installation of NeXpy. There is 
more details of the nature of these dependencies in the 
[NeXpy documentation](http://nexpy.github.io/nexpy).

* numpy                http://numpy.org
* h5py                 http://www.h5py.org
* pyro4                http://pythonhosted.org//Pyro4/

User Support
============
If you discover any bugs, please submit a 
[Github issue](https://github.com/nexpy/nxremote/issues), preferably with 
relevant tracebacks.
