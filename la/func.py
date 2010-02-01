"Functions that operate on larrys."

import numpy as np

from la.deflarry import larry
from la.util.misc import list2index, fromlists


# Creation ------------------------------------------------------------------
   
def fromtuples(data):
    """
    Convert a list of tuples to a larry.
    
    The input data, if there are N dimensions and M data points, should have
    this form:
    
    [(label0_1, label1_1, ..., labelN_1, value_1),
     (label0_2, label1_2, ..., labelN_2, value_2),
     ...
     (label0_M, label1_M, ..., labelN_M, value_M)]
    
    Parameters
    ----------
    data : list of tuples
        The input must be a list of tuples where each tuple represents one
        data point in the larry: (label0, label1, ..., labelN, value)   
        
    Returns
    -------
    y : larry
        A larry constructed from `data` is returned.
        
    See Also
    --------
    la.larry.totuples : Convert to a flattened list of tuples.
    la.fromlist : Convert a list of tuples to a larry.
    la.fromdict : Convert a dictionary to a larry.

    
    Notes
    -----
    fromlist is faster than fromtuples since fromtuples must do one extra
    step: unzip the labels and data values.

    Examples
    --------
    Convert a list of label, value pairs to a larry:
    
    >>> data = [('r0', 'c0', 1), ('r0', 'c1', 2), ('r1', 'c0', 3), ('r1', 'c1', 4)]
    >>> la.fromtuples(data)
    label_0
        r0
        r1
    label_1
        c0
        c1
    x
    array([[ 1.,  2.],
           [ 3.,  4.]])
            
    What happens if we throw out the last data point? The missing value
    becomes NaN:       
            
    >>> data = data[:-1]
    >>> la.fromtuples(data)
    label_0
        r0
        r1
    label_1
        c0
        c1
    x
    array([[  1.,   2.],
           [  3.,  NaN]])
            
    """
        
    # Split data into label and x
    labels = zip(*data)
    xs = labels.pop(-1)   
    
    # Determine labels, shape, and index into array	
    x, label = fromlists(xs, labels)  
    
    return larry(x, label) 
    
def fromlist(data):
    """
    Convert a flattened list to a larry.
    
    The input data, if there are N dimensions and M data points, should have
    this form:
    
    [[value_1,  value_2,  ..., value_M],
     [(label0_1, label1_1, ..., labelN_1),
      (label0_2, label1_2, ..., labelN_2),
      ...
      (label0_M, label1_M, ..., labelN_M)]]    
    
    Parameters
    ----------
    data : list
        The input must be a list such as that returned by larry.tolist. See
        the example below.  
        
    Returns
    -------
    y : larry
        A larry constructed from `data` is returned.
        
    See Also
    --------
    la.larry.tolist : Convert to a flattened list.
    la.fromtuples : Convert a list of tuples to a larry.
    la.fromdict : Convert a dictionary to a larry.  

    Examples
    --------
    >>> data = [[1, 2, 3, 4], [('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd')]]
    >>> la.fromlist(data)
    label_0
        a
        b
    label_1
        c
        d
    x
    array([[ 1.,  2.],
           [ 3.,  4.]])
           
    """
    x, label = fromlists(data[0], zip(*data[1]))      
    return larry(x, label)             

def fromdict(data):
    """
    Convert a dictionary to a larry.
    
    The input data, if there are N dimensions and M data points, should have
    this form:
    
    {(label0_1, label1_1, ..., labelN_1): value_1,
     (label0_2, label1_2, ..., labelN_2): value_2,
     ...
     (label0_M, label1_M, ..., labelN_M): value_M}   
    
    Parameters
    ----------
    data : dict
        The input must be a dictionary such as that returned by larry.todict
        See the example below. 
        
    Returns
    -------
    y : larry
        A larry constructed from `data` is returned.
        
    See Also
    --------
    la.larry.todict : Convert to a dictionary. 
    la.fromtuples : Convert a list of tuples to a larry.
    la.fromlist : Convert a list of tuples to a larry.

    Examples
    --------
    >>> data = {('a', 'c'): 1, ('a', 'd'): 2, ('b', 'c'): 3, ('b', 'd'): 4}
    >>> la.fromdict(data)
    label_0
        a
        b
    label_1
        c
        d
    x
    array([[ 1.,  2.],
           [ 3.,  4.]])
           
    """  
    return fromlist([data.values(), data.keys()])  

# Labels --------------------------------------------------------------------
    
def union(axis, *args):
    """
    Union of labels along specified axis.
    
    Parameters
    ----------
    axis : int
        The axis along which to take the union of the labels.
    args : larrys
        The larrys (separated by commas) over which the union is taken.
        
    Returns
    -------
    out : list
        A list containing the union of the labels.
        
    See Also
    --------
    la.intersection : Intersection of labels along specified axis.
    
    Examples
    --------            
    >>> import la
    >>> y1 = larry([[1, 2], [3, 4]], [['a', 'b'], ['c', 'd']])
    >>> y2 = larry([[1, 2], [3, 4]], [['e', 'b'], ['f', 'd']])
    >>> la.union(0, y1, y2)
    ['a', 'b', 'e']
    >>> la.union(1, y1, y2)
    ['c', 'd', 'f']
    
    """
    rc = frozenset([])
    for arg in args:
        if isinstance(arg, larry):
            rc = frozenset(arg.label[axis]) | rc
        else:
            raise TypeError, 'One or more input is not a larry'
    rc = list(rc)
    rc.sort()
    return rc

def intersection(axis, *args):
    """
    Intersection of labels along specified axis.
    
    Parameters
    ----------
    axis : int
        The axis along which to take the intersection of the labels.
    args : larrys
        The larrys (separated by commas) over which the intersection is taken.
        
    Returns
    -------
    out : list
        A list containing the intersection of the labels.
        
    See Also
    --------
    la.union : Union of labels along specified axis.
    
    Examples
    --------            
    >>> import la
    >>> y1 = larry([[1, 2], [3, 4]], [['a', 'b'], ['c', 'd']])
    >>> y2 = larry([[1, 2], [3, 4]], [['e', 'b'], ['f', 'd']])
    >>> la.intersection(0, y1, y2)
    ['b']
    >>> la.intersection(1, y1, y2)
    ['d']
    
    """
    rc = frozenset(args[0].label[axis])
    for i in xrange(1, len(args)):
        arg = args[i]
        if isinstance(arg, larry):
            rc = frozenset(arg.label[axis]) & rc
        else:
            raise TypeError, 'One or more input is not a larry'
    rc = list(rc)
    rc.sort()
    return rc

# Concatenating -------------------------------------------------------------
    
def stack(mode, **kwargs):
    """Stack 2d larrys to make a 3d larry.
    
    Parameters
    ----------
    mode : {'union', 'intersection'}
        Should the 3d larry be made from the union or intersection of all the
        rows and all the columns?
    kwargs : name=larry
        Variable length input listing the z axis name and larry. For example,
        stack('union', momentum=x, volume=y, ep=z)
        
    Returns
    -------
    out : larry
        Returns a 3d larry.
        
    Raises
    ------
    ValueError
        If mode is not union or intersection or if any of the input larrys are
        not 2d.
                    
    """
    if not np.all([kwargs[key].ndim == 2 for key in kwargs]):
        raise ValueError, 'All input larrys must be 2d'
    if mode == 'union':
        logic = union
    elif mode == 'intersection':
        logic = intersection
    else:    
        raise ValueError, 'mode must be union or intersection'   
    row = logic(0, *kwargs.values())
    col = logic(1, *kwargs.values())
    x = np.zeros((len(kwargs), len(row), len(col)))
    zlabel = []
    for i, key in enumerate(kwargs):
        y = kwargs[key]
        y = y.morph(row, 0)
        y = y.morph(col, 1)
        x[i] = y.x
        zlabel.append(key)
    label = [zlabel, row, col]
    return larry(x, label)    
