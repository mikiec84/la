
===
I/O
===

The la package provides two ways to archive larrys: using archive functions
such as **save** and **load** and using the dictionary-like interface of the
**IO** class. Both I/O methods store larrys in
`HDF5 <http://www.hdfgroup.org/>`_ 1.8 format and require
`h5py <http://h5py.alfven.org>`_.


Archive functions
=================

One method to archive larrys is to use the archive functions (see
:ref:`ioclass` for a second, more powerful method):

* **save**
* **load**
* **delete**
* **archive_directory**
* **is_archived_larry**
* **repack**

To demonstrate, let's start by creating a larry:
::
    >>> import la
    >>> y = la.larry([1,2,3])

Next let's save the larry, *y*, in an archive using the **save** function:
::
    >>> la.save('/tmp/data.hdf5', y, 'y')
    
The contents of the archive:
::
    >>> la.archive_directory('/tmp/data.hdf5')
    ['y']      
    
To load the larry we use the **load** function:
::
    >>> z = la.load('/tmp/data.hdf5', 'y')
    
The entire larry is loaded from the archive. The **load** function does not
have an option to load parts of a larry, such as a slice. (To load parts of
a larrys from the archive, see :ref:`ioclass`.)    

The name of the larry in **save** and **load** statements (and in all the
other archive functions) must be a string. But the string may contain one or
more forward slashes ('/'), which is to say that larrys can be archived in a
hierarchical structure:
::
    >>> la.save('/tmp/data/hdf5', y, '/experiment/2/y')
    >>> z = la.load('/tmp/data/hdf5', '/experiment/2/y')
    
Instead of passing a filename to the archive functions you can optionally
pass a `h5py <http://h5py.alfven.org/>`_ File object:
::
    >>> import h5py
    >>> f = h5py.File('/tmp/data.hdf5')
    >>> z = la.load(f, 'y') 

To check if a larry is in the archive:
::
    >>> la.is_archived_larry(f, 'y')    
    True
    
To delete a larry from the archive:

    >>> la.delete(f, 'y')
    >>> la.is_archived_larry(f, 'y')    
    False

HDF5 does not keep track of the freespace in an archive across opening and
closing of the archive. After repeatedly opening, closing and deleting larrys
from the archive, the unused space in the archive may grow. The only way to
reclaim the freespace is to repack the archive:
::
    >>> la.repack(f)
    
To see how much space the archive takes on disk and to see how much freespace
is in the archive see :ref:`ioclass`.  
     
.. _ioclass:
    
IO class
========

The **IO** class provides a dictionary-like interface to the archive.

To demonstrate, let's start by creating two larrys, *a* and *b*:
::
    >>> import la
    >>> a = la.larry([1.0,2.0,3.0,4.0])
    >>> b = la.larry([[1,2],[3,4]])

To work with an archive you need to create an **IO** object:
::
    >>> io = la.IO('/tmp/data.hdf5')
    
Let's add (save) the two larrys, *a* and *b*, to the archive and then list the
contents of the archive:
::
    >>> io['a'] = a
    >>> io['b'] = b
    >>> io
   
    larry  dtype    shape 
    ----------------------
    a      float64  (4,)  
    b      int64    (2, 2)  

We can get a list of the keys (larrys) in the archive:
::
    >>> io.keys()
        ['a', 'b']
        
    >>> for key in io: print key
    ... 
    a
    b 
    
    >>> len(io)
    2  
    
Are the larrys *a* (yes) and *c* (no) in the archive?
::
    >>> 'a' in io
    True 
    >>> 'c' in io
    False 
        
    >>> list(set(io) & set(['a', 'c']))
    ['a']                   
        
When we load data from the archive using an **IO** object, we get a lara not
a larry:
::
    >>> z = io['a']        
    >>> type(z)
        <class 'la.io.lara'>
        
Whereas a larry stores its data in a numpy array and a list (labels), lara
stores its data in a h5py Dataset object and a list (labels). The reason that
an **IO** object returns a lara instead of a larry is that you may want to
extract only part of a larry, such as a slice, from the archive.

To convert a lara object into a larry, just index into the lara:
::
    >>> z = io['a'][:2]
    >>> type(z)
    <class 'la.deflarry.larry'>

    >>> z
    label_0
        0
        1
    x
    array([ 1.,  2.])

In the example above, only the first two items in the array were loaded from
the archive---a feature that comes in handy when you only need a small part
of a large larry.

Although the data from a larry is not loaded until you index into the lara,
the entire label is always loaded. That allows you to use the labels right
away:
::
    >>> z = io['a']
    >>> type(z)
    <class 'la.io.lara'>

    >>> idx = z.labelindex(1, axis=0)
    >>> type(z[:idx])
    <class 'la.deflarry.larry'>

HDF5 does not keep track of the freespace in an archive across opening and
closing of the archive. After repeatedly opening, closing and deleting larrys
from the archive, the unused space in the archive may grow. The only way to
reclaim the freespace is to repack the archive:
::
    >>> io.repack()
    
Before looking at the size of the archive, let's add some bigger larrys:
::
    >>> import numpy as np
    >>> io['rand'] = la.larry(np.random.rand(1000, 1000))
    >>> io['randn'] = la.larry(np.random.rand(1000, 1000))
    >>> io    
    larry  dtype    shape       
    ----------------------------
    a      float64  (4,)        
    b      int64    (2, 2)      
    rand   float64  (1000, 1000)
    randn  float64  (1000, 1000)
    
How many MB does that archive occupy on disk?
::
    >>> io.space / 1e6    
    16.041224  # MB
    
How much freespace is there?
::
    >>> io.freespace / 1e6 
    0.0090959999999999999  # MB

Let's delete randn from the archive and look at the space and freespace:
::
    >>> del io['randn']
    >>> io.space / 1e6
    16.038632  # MB
    >>> io.freespace / 1e6
    8.0226319999999998  # MB
    
So deleting a larry from the the archive does not reduce the size of the
archive unless you repack:
::
    >>> io.repack()
    >>> io.space / 1e6
    8.0201919999999998  # MB
    >>> io.freespace / 1e6
    0.0041920000000000004  # MB
          
What filename is associated with the archive?
::
    >>> io.filename
    '/tmp/data.hdf5'               


Limitations
===========

There are several limitations of the archiving method used by the la package.
In this section we will discuss two limitations:

* The freespace in the archive is not by default automatically reclaimed after
  deleting larrys.
* In order to archive a larry, its data and labels must be of a type supported
  by HDF5.   

**Freespace**

HDF5 does not keep track of the freespace in an archive across opening and
closing of the archive. Therefore, after opening, closing and deleting larrys
from the archive, the unused space in the archive may grow. The only way to
reclaim the freespace is to repack the archive.

You can use the utility provided by HDF5 to repack the archive or you can use
the repack method or function in the la package:
::
    >>> 
    
**Data types**  

A larry can have labels of mixed type, for example strings and numbers.
However, when archiving larrys in HDF5 format the labels are
converted to Numpy arrays and the elements of a Numpy array must be of the
same type. Therefore, to archive a larry the labels along any one dimension
must be of the same type and that type must be one that is recognized by
h5py and HDF5: strings and scalars. So, for example, if your labels are
datetime.date objects, then you must convert them (perhaps to integers using
the datetime.date.toordinal function) before archiving.


Archive format
==============

An HDF5 archive is contructed from two types of objects: Groups and Datasets.
Groups can contain Datasets and more Groups. Datasets can contain arrays.

larrys are stored in a HDF5 Group. The name of the group is the name of the
larry. The group is given an attribute called 'larry' and assigned the value
True. Inside the group are several HDF5 Datasets. For a 2d larry, for example,
there are three datasets: one to hold the data (named 'x') and two to hold the
labels (named '0' and '1'). In general, for a nd larry there are n+1
datasets.