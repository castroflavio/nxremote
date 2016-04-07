Installation
============
Currently, you need to install the package from the source code by cloning 
the latest development version in the 
`NeXpy Git repository <https://github.com/nexpy/nxremote>`_::

    $ git clone https://github.com/nexpy/nxremote.git

You can then install NeXpy by changing to the source directory and typing::

    $ python setup.py install

To install in an alternate location::

    $ python setup.py install --prefix=/path/to/installation/dir

Required Libraries
==================

=================  ===================================================
Library            URL
=================  ===================================================
h5py               http://www.h5py.org
numpy              http://numpy.scipy.org/
pyro4              http://pythonhosted.org//Pyro4/ (for remote server)
=================  ===================================================

Versioning
-------------------
This package uses `Semantic Versioning <http://semver.org/spec/v2.0.0.html>`_.

User Support
------------
If you discover any bugs, please submit a `Github issue 
<https://github.com/nexpy/nxremote/issues>`_, preferably with relevant 
tracebacks.
