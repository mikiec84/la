"Unit tests of larry functions."

import unittest
import datetime

import numpy as np
nan = np.nan
from numpy.testing import assert_array_equal

from la import larry
from la import (union, intersection, panel, stack, cov, align, binaryop, add,
                subtract, multiply, divide, unique)
from la.util.testing import assert_larry_equal as ale


class Test_func(unittest.TestCase):
    "Test larry functions in flarry"                         
        
    def test_union_1(self):
        "func.union_1" 
        y1 = larry([[1, 2], [3, 4]], [['a', 'b'], ['c', 'd']])
        y2 = larry([[1, 2], [3, 4]], [['e', 'b'], ['f', 'd']])
        actual = union(0, y1, y2)
        desired = ['a', 'b', 'e']
        self.assert_(actual == desired, 'union axis=0')
        actual = union(1, y1, y2)
        desired = ['c', 'd', 'f']
        self.assert_(actual == desired, 'union axis=1') 
        
    def test_intersection_1(self):
        "func.intersection_1" 
        y1 = larry([[1, 2], [3, 4]], [['a', 'b'], ['c', 'd']])
        y2 = larry([[1, 2], [3, 4]], [['e', 'b'], ['f', 'd']])
        actual = intersection(0, y1, y2)
        desired = ['b']
        self.assert_(actual == desired, 'intersection axis=0')
        actual = intersection(1, y1, y2)
        desired = ['d']
        self.assert_(actual == desired, 'intersection axis=1') 
        
    def test_panel_1(self):
        "func.panel_1"         
        original = larry(np.arange(24).reshape(2,3,4))                   
        actual = panel(original)
        x = np.array([[ 0, 12],
                      [ 4, 16],
                      [ 8, 20],
                      [ 1, 13],
                      [ 5, 17],
                      [ 9, 21],
                      [ 2, 14],
                      [ 6, 18],
                      [10, 22],
                      [ 3, 15],
                      [ 7, 19],
                      [11, 23]])
        label = [[(0, 0),
                  (0, 1),
                  (0, 2),
                  (0, 3),
                  (1, 0),
                  (1, 1),
                  (1, 2),
                  (1, 3),
                  (2, 0),
                  (2, 1),
                  (2, 2),
                  (2, 3)], [0, 1]]
        desired = larry(x, label)         
        ale(actual, desired, msg='panel test #1', original=original) 
        
    def test_stack_1(self):
        "func.stack_1"           
        y1 = larry([[1, 2], [3, 4]])
        y2 = larry([[5, 6], [7, 8]])
        actual = stack('union', name1=y1, othername=y2)
        x = np.array([[[ 5.,  6.],
                       [ 7.,  8.]],
                      [[ 1.,  2.],
                       [ 3.,  4.]]]) 
        label = [['othername', 'name1'], [0, 1], [0, 1]]
        desired = larry(x, label)
        ale(actual, desired, msg='stack test #1')              
        
    def test_cov_1(self):
        "func.cov_1" 
        original = larry([[ 2.0, 2.0, 3.0, 1.0],
                          [ 3.0, 2.0, 2.0, 1.0],
                          [ 1.0, 1.0, 1.0, 1.0]])
        original = original.demean(axis=1)      
        desired = larry([[ 0.5,   0.25,  0.  ],
                         [ 0.25,  0.5,   0.  ],
                         [ 0.,    0.,    0.  ]])     
        actual = cov(original)
        ale(actual, desired, msg='cov test #1', original=original)       

    def test_cov_2(self):
        "func.cov_2" 
        original = larry([[nan, 2.0, 1.0],
                          [2.0, 3.0, 1.0],
                          [4.0, 1.0, 1.0]])  
        original = original.demean(1)        
        desired = larry(np.ma.cov(np.ma.fix_invalid(original.x), bias=1).data)
        actual = cov(original)
        ale(actual, desired, msg='cov test #2', original=original) 

    def test_unique_1(self):
        arr = unique(larry([1, 1, 2, 2, 3, 3]))
        assert_array_equal(arr, np.array([1, 2, 3]), "la.unique failed")

    def test_unique_2(self):
        lar = larry([[1, 1], [2, 3]])
        arr = unique(lar)
        assert_array_equal(arr, np.array([1, 2, 3]), "la.unique failed")
    
    def test_unique_3(self):
        lar = larry(['a', 'b', 'b', 'c', 'a'])
        u, indices = unique(lar, return_index=True)
        assert_array_equal(u, np.array(['a', 'b', 'c'], dtype='|S1'))
        assert_array_equal(indices, np.array([0, 1, 3]))
        assert_array_equal(lar[indices], np.array(['a','b','c'], dtype='|S1'))
    
    def test_unique_4(self):
        lar = larry([1, 2, 6, 4, 2, 3, 2])
        u, indices = unique(lar, return_inverse=True)
        assert_array_equal(u, np.array([1, 2, 3, 4, 6]))
        assert_array_equal(indices, np.array([0, 1, 4, 3, 1, 2, 1]))
        assert_array_equal(u[indices], np.array([1, 2, 6, 4, 2, 3, 2]))

class Test_align_1d(unittest.TestCase):
    "Test 1d alignment of larrys"   

    def test_1d1(self):
        "align 1d test #1"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        a1, a2 = align(y1, y2)
        d1 = larry([1, 2])
        d2 = larry([1, 2])
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)            

    def test_1d2(self):
        "align 1d test #2"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        a1, a2 = align(y1, y2, join='inner')
        d1 = larry([1, 2])
        d2 = larry([1, 2])
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2) 

    def test_1d3(self):
        "align 1d test #3"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        a1, a2 = align(y1, y2, join='inner', cast=False)
        d1 = larry([1, 2])
        d2 = larry([1, 2])
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2) 

    def test_1d4(self):
        "align 1d test #4"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        a1, a2 = align(y1, y2, join='outer')
        d1 = larry([1, 2, nan], dtype=float)
        d2 = larry([1, 2, 3])
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)
        
    def test_1d5(self):
        "align 1d test #5"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        self.failUnlessRaises(TypeError, align, y1, y2, 'outer', False)        

    def test_1d6(self):
        "align 1d test #6"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        a1, a2 = align(y1, y2, join='left')
        d1 = larry([1, 2])
        d2 = larry([1, 2])
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)

    def test_1d7(self):
        "align 1d test #7"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        a1, a2 = align(y1, y2, join='right')
        d1 = larry([1, 2, nan], dtype=float)
        d2 = larry([1, 2, 3])
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)
        
    def test_1d8(self):
        "align 1d test #8"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        a1, a2 = align(y1, y2, join=['right'])
        d1 = larry([1, 2, nan], dtype=float)
        d2 = larry([1, 2, 3])
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)        

    def test_1d9(self):
        "align 1d test #9"
        y1 = larry([1, 2])
        y2 = larry([1, 2], [['a', 'b']])
        a1, a2 = align(y1, y2)
        d1 = larry([], dtype=int)
        d2 = larry([], dtype=int)
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)            

    def test_1d10(self):
        "align 1d test #10"
        y1 = larry([1, 2])
        y2 = larry([1, 2], [['a', 'b']])
        a1, a2 = align(y1, y2, join='inner')
        d1 = larry([], dtype=int)
        d2 = larry([], dtype=int)
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2) 

    def test_1d11(self):
        "align 1d test #11"
        y1 = larry([1, 2])
        y2 = larry([1, 2], [['a', 'b']])
        a1, a2 = align(y1, y2, join='inner')
        d1 = larry([], dtype=int)
        d2 = larry([], dtype=int)
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2) 

    def test_1d12(self):
        "align 1d test #12"
        y1 = larry([1, 2])
        y2 = larry([1, 2], [['a', 'b']])
        a1, a2 = align(y1, y2, join='outer')
        d1 = larry([1,   2,   nan, nan], [[0, 1, 'a', 'b']], dtype=float)
        d2 = larry([nan, nan, 1,   2],   [[0, 1, 'a', 'b']], dtype=float)
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)
        
    def test_1d13(self):
        "align 1d test #13"
        y1 = larry([1, 2])
        y2 = larry([1, 2], [['a', 'b']])
        self.failUnlessRaises(TypeError, align, y1, y2, 'outer', False)

    def test_1d14(self):
        "align 1d test #14"
        y1 = larry([1, 2])
        y2 = larry([1, 2], [['a', 'b']])
        a1, a2 = align(y1, y2, join='left')
        d1 = larry([1, 2])
        d2 = larry([nan, nan])
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2) 

    def test_1d15(self):
        "align 1d test #15"
        y1 = larry([1, 2])
        y2 = larry([1, 2], [['a', 'b']])
        a1, a2 = align(y1, y2, join='right')
        d1 = larry([nan, nan], [['a', 'b']])
        d2 = larry([1,   2], [['a', 'b']])
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)
        
    def test_1d16(self):
        "align 1d test #16"
        y1 = larry([1, 2])
        y2 = larry([1, 2], [['a', 'b']])
        a1, a2 = align(y1, y2, join=['left'])
        d1 = larry([1, 2])
        d2 = larry([nan, nan])
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)
        
    def test_1d17(self):
        "align 1d test #17"
        y1 = larry([1, 2])
        y2 = larry([1, 2], [['a', 'b']])        
        self.failUnlessRaises(TypeError, align, y1, y2, 'outer', False) 

    def test_1d18(self):
        "align 1d test #18"
        y1 = larry([1, 2])
        y2 = larry([1, 2])
        a1, a2 = align(y1, y2, cast=False)
        d1 = larry([1, 2])
        d2 = larry([1, 2])
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)
        
    def test_1d19(self):
        "align 1d test #19"
        y1 = larry([True, False])
        y2 = larry([True, False, True])
        a1, a2 = align(y1, y2, join='outer')
        d1 = larry([1, 0, nan], dtype=float)
        d2 = larry([True, False, True])
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)        

    def test_1d20(self):
        "align 1d test #20"
        d = datetime.date
        y1 = larry([d(2011,1,1), d(2011,1,2)])
        y2 = larry([d(2011,1,3), d(2011,1,4), d(2011,1,5)])
        a1, a2 = align(y1, y2, join='outer')
        d1 = larry([d(2011,1,1), d(2011,1,2), None])
        d2 = larry([d(2011,1,3), d(2011,1,4), d(2011,1,5)])
        msg = "align 1d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)

class Test_align_2d(unittest.TestCase):
    "Test 2d alignment of larrys"   

    def test_2d1(self):
        "align 2d test #1"
        y1 = larry([[1, 2], [3, 4]])
        y2 = larry([[1, 2, 5], [3, 4, 6]])
        a1, a2 = align(y1, y2)
        d1 = larry([[1, 2], [3, 4]])
        d2 = larry([[1, 2], [3, 4]])
        msg = "align 2d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)            

    def test_2d2(self):
        "align 2d test #2"
        y1 = larry([[1, 2], [3, 4]])
        y2 = larry([[1, 2, 5], [3, 4, 6]])
        a1, a2 = align(y1, y2, join='inner')
        d1 = larry([[1, 2], [3, 4]])
        d2 = larry([[1, 2], [3, 4]])
        msg = "align 2d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2) 

    def test_2d3(self):
        "align 2d test #3"
        y1 = larry([[1, 2], [3, 4]])
        y2 = larry([[1, 2, 5], [3, 4, 6]])
        a1, a2 = align(y1, y2, join='inner', cast=False)
        d1 = larry([[1, 2], [3, 4]])
        d2 = larry([[1, 2], [3, 4]])
        msg = "align 2d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)

    def test_2d4(self):
        "align 2d test #4"
        y1 = larry([[1, 2], [3, 4]])
        y2 = larry([[1, 2, 5], [3, 4, 6]])
        a1, a2 = align(y1, y2, join='outer')
        d1 = larry([[1, 2, nan], [3, 4, nan]], dtype=float)
        d2 = larry([[1, 2, 5],   [3, 4,   6]])
        msg = "align 2d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)

    def test_2d5(self):
        "align 2d test #5"
        y1 = larry([[1, 2], [3, 4]])
        y2 = larry([[1, 2, 5], [3, 4, 6]])
        self.failUnlessRaises(TypeError, align, y1, y2, 'outer', False)       

    def test_2d6(self):
        "align 2d test #6"
        y1 = larry([[1, 2], [3, 4]])
        y2 = larry([[1, 2, 5], [3, 4, 6]])
        a1, a2 = align(y1, y2, join=['inner', 'outer'])
        d1 = larry([[1, 2, nan], [3, 4, nan]])
        d2 = larry([[1, 2, 5],   [3, 4, 6]])
        msg = "align 2d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)

    def test_2d7(self):
        "align 2d test #7"
        y1 = larry([[1, 2], [3, 4]])
        y2 = larry([[1, 2, 5], [3, 4, 6]])
        j = ['outer', 'inner', 'left']
        self.failUnlessRaises(ValueError, align, y1, y2, j, False)

    def test_2d8(self):
        "align 2d test #8"
        y1 = larry([[1, 2], [3, 4]])
        y2 = larry([[1, 2], [3, 4]])
        a1, a2 = align(y1, y2, cast=False)
        d1 = larry([[1, 2], [3, 4]])
        d2 = larry([[1, 2], [3, 4]])
        msg = "align 2d fail on %s larry"
        ale(a1, d1, msg % 'left', original=y1)
        ale(a2, d2, msg % 'right', original=y2)
        
class Test_binaryop(unittest.TestCase):
    "Test la.binaryop()"   

    def test_binaryop_01(self):
        "binaryop test #01"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2)
        desired = larry([2, 4])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)           

    def test_binaryop_02(self):
        "binaryop test #02"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, join='inner')
        desired = larry([2, 4])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
        
    def test_binaryop_03(self):
        "binaryop test #03"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, join='inner', missone=0)
        desired = larry([2, 4])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
                  
    def test_binaryop_04(self):
        "binaryop test #04"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, join='inner', missone=0, misstwo=0)
        desired = larry([2, 4])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

    def test_binaryop_05(self):
        "binaryop test #05"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, misstwo=0)
        desired = larry([2, 4])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

    def test_binaryop_06(self):
        "binaryop test #06"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, join='outer')
        desired = larry([2, 4, nan])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
        
    def test_binaryop_07(self):
        "binaryop test #07"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, join='outer', missone=0)
        desired = larry([2, 4, 3], dtype=float)
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
                  
    def test_binaryop_08(self):
        "binaryop test #08"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, join='outer', missone=0, misstwo=0)
        desired = larry([2, 4, 3], dtype=float)
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

    def test_binaryop_09(self):
        "binaryop test #09"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, join='outer', misstwo=0)
        desired = larry([2, 4, nan])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
        
    def test_binaryop_10(self):
        "binaryop test #10"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, join='left')
        desired = larry([2, 4])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
        
    def test_binaryop_11(self):
        "binaryop test #11"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, join='left', missone=0)
        desired = larry([2, 4])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
                  
    def test_binaryop_12(self):
        "binaryop test #12"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, join='left', missone=0, misstwo=0)
        desired = larry([2, 4])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)       

    def test_binaryop_13(self):
        "binaryop test #13"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, join='right')
        desired = larry([2, 4, nan])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
        
    def test_binaryop_14(self):
        "binaryop test #14"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, join='right', missone=0)
        desired = larry([2, 4, 3], dtype=float)
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
                  
    def test_binaryop_15(self):
        "binaryop test #15"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, join='right', missone=0, misstwo=0)
        desired = larry([2, 4, 3], dtype=float)
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

    def test_binaryop_16(self):
        "binaryop test #16"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = binaryop(np.add, y1, y2, join='right', misstwo=0)
        desired = larry([2, 4, nan])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
        
    def test_binaryop_17(self):
        "binaryop test #17"
        y1 = larry([1, nan, nan, 1])
        y2 = larry([1, 1,   nan, 1], [[0, 1, 2, 'a']])
        actual = binaryop(np.add, y1, y2)
        desired = larry([2, nan, nan], [[0, 1, 2]])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

    def test_binaryop_18(self):
        "binaryop test #18"
        y1 = larry([1, nan, nan, 1])
        y2 = larry([1, 1,   nan, 1], [[0, 1, 2, 'a']])
        actual = binaryop(np.add, y1, y2, join='outer')
        desired = larry([2, nan, nan, nan, nan], [[0, 1, 2, 3, 'a']])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

    def test_binaryop_19(self):
        "binaryop test #19"
        y1 = larry([1, nan, nan, 1])
        y2 = larry([1, 1,   nan, 1], [[0, 1, 2, 'a']])
        actual = binaryop(np.add, y1, y2, join='outer', missone=0)
        desired = larry([2, 1, nan, 1, 1], [[0, 1, 2, 3, 'a']])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
                                        
    def test_binaryop_20(self):
        "binaryop test #20"
        y1 = larry([1, nan, nan, 1])
        y2 = larry([1, 1,   nan, 1], [[0, 1, 2, 'a']])
        actual = binaryop(np.add, y1, y2, join='outer', missone=0, misstwo=0)
        desired = larry([2, 1, 0, 1, 1], [[0, 1, 2, 3, 'a']], dtype=float)
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

    def test_binaryop_21(self):
        "binaryop test #21"
        y1 = larry([True, True])
        y2 = larry([True, False, True])
        actual = binaryop(np.logical_and, y1, y2)
        desired = larry([True, False])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2) 

    def test_binaryop_22(self):
        "binaryop test #22"
        # This is a corner case. The binaryop function uses the align_raw
        # function which converts the bool larrys to float since it must
        # fill in a missing value. And then logical_and(nan, True) returns
        # True.
        y1 = larry([True, True])
        y2 = larry([True, False, True])
        actual = binaryop(np.logical_and, y1, y2, join='outer')
        desired = larry([True, False, True])
        msg = "binaryop failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2) 

class Test_add(unittest.TestCase):
    "Test la.add()"   

    def test_add_01(self):
        "add test #01"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2)
        desired = larry([2, 4])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)           

    def test_add_02(self):
        "add test #02"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, join='inner')
        desired = larry([2, 4])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
        
    def test_add_03(self):
        "add test #03"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, join='inner', missone=0)
        desired = larry([2, 4])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
                  
    def test_add_04(self):
        "add test #04"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, join='inner', missone=0, misstwo=0)
        desired = larry([2, 4])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

    def test_add_05(self):
        "add test #05"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, misstwo=0)
        desired = larry([2, 4])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

    def test_add_06(self):
        "add test #06"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, join='outer')
        desired = larry([2, 4, nan])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
        
    def test_add_07(self):
        "add test #07"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, join='outer', missone=0)
        desired = larry([2, 4, 3], dtype=float)
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
                  
    def test_add_08(self):
        "add test #08"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, join='outer', missone=0, misstwo=0)
        desired = larry([2, 4, 3], dtype=float)
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

    def test_add_09(self):
        "add test #09"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, join='outer', misstwo=0)
        desired = larry([2, 4, nan])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
        
    def test_add_10(self):
        "add test #10"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, join='left')
        desired = larry([2, 4])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
        
    def test_add_11(self):
        "add test #11"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, join='left', missone=0)
        desired = larry([2, 4])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
                  
    def test_add_12(self):
        "add test #12"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, join='left', missone=0, misstwo=0)
        desired = larry([2, 4])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)       

    def test_add_13(self):
        "add test #13"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, join='right')
        desired = larry([2, 4, nan])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
        
    def test_add_14(self):
        "add test #14"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, join='right', missone=0)
        desired = larry([2, 4, 3], dtype=float)
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
                  
    def test_add_15(self):
        "add test #15"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, join='right', missone=0, misstwo=0)
        desired = larry([2, 4, 3], dtype=float)
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

    def test_add_16(self):
        "add test #16"
        y1 = larry([1, 2])
        y2 = larry([1, 2, 3])
        actual = add(y1, y2, join='right', misstwo=0)
        desired = larry([2, 4, nan])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
        
    def test_add_17(self):
        "add test #17"
        y1 = larry([1, nan, nan, 1])
        y2 = larry([1, 1,   nan, 1], [[0, 1, 2, 'a']])
        actual = add(y1, y2)
        desired = larry([2, nan, nan], [[0, 1, 2]])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

    def test_add_18(self):
        "add test #18"
        y1 = larry([1, nan, nan, 1])
        y2 = larry([1, 1,   nan, 1], [[0, 1, 2, 'a']])
        actual = add(y1, y2, join='outer')
        desired = larry([2, nan, nan, nan, nan], [[0, 1, 2, 3, 'a']])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

    def test_add_19(self):
        "add test #19"
        y1 = larry([1, nan, nan, 1])
        y2 = larry([1, 1,   nan, 1], [[0, 1, 2, 'a']])
        actual = add(y1, y2, join='outer', missone=0)
        desired = larry([2, 1, nan, 1, 1], [[0, 1, 2, 3, 'a']])
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
                                        
    def test_add_20(self):
        "add test #20"
        y1 = larry([1, nan, nan, 1])
        y2 = larry([1, 1,   nan, 1], [[0, 1, 2, 'a']])
        actual = add(y1, y2, join='outer', missone=0, misstwo=0)
        desired = larry([2, 1, 0, 1, 1], [[0, 1, 2, 3, 'a']], dtype=float)
        msg = "add failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

class Test_subtract(unittest.TestCase):
    "Test la.subtract()"   

    def test_subtract_01(self):
        "subtract test #01"
        y1 = larry([1,   2, nan], [['a', 'b', 'c']])
        y2 = larry([1, nan, nan], [['a', 'b', 'dd']])
        actual = subtract(y1, y2)
        desired = larry([0, nan], [['a', 'b']])
        msg = "subtract failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)

    def test_subtract_02(self):
        "subtract test #02"
        y1 = larry([1,   2, nan], [['a', 'b', 'c']])
        y2 = larry([1, nan, nan], [['a', 'b', 'dd']])
        actual = subtract(y1, y2, missone=0)
        desired = larry([0, 2], [['a', 'b']], dtype=float)
        msg = "subtract failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2) 
        
    def test_subtract_03(self):
        "subtract test #03"
        y1 = larry([1,   2, nan], [['a', 'b', 'c']])
        y2 = larry([1, nan, nan], [['a', 'b', 'dd']])
        actual = subtract(y1, y2, join='outer')
        desired = larry([0, nan, nan, nan], [['a', 'b', 'c', 'dd']])
        msg = "subtract failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)         

    def test_subtract_04(self):
        "subtract test #04"
        y1 = larry([1,   2, nan], [['a', 'b', 'c']])
        y2 = larry([1, nan, nan], [['a', 'b', 'dd']])
        actual = subtract(y1, y2, join='outer', missone=0, misstwo=0)
        desired = larry([0, 2, 0, 0], [['a', 'b', 'c', 'dd']], dtype=float)
        msg = "subtract failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)              

class Test_multiply(unittest.TestCase):
    "Test la.multiply()"   

    def test_multiply_01(self):
        "multiply test #01"
        y1 = larry([1,   2, nan], [['a', 'b', 'c']])
        y2 = larry([1, nan, nan], [['a', 'b', 'dd']])
        actual = multiply(y1, y2, join='outer', missone=1, misstwo=2)
        desired = larry([1, 2, 4, 4], [['a', 'b', 'c', 'dd']], dtype=float)
        msg = "multiply failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
 
class Test_divide(unittest.TestCase):
    "Test la.divide()"   

    def test_divide_01(self):
        "divide test #01"
        y1 = larry([1,   2, nan], [['a', 'b', 'c']])
        y2 = larry([1, nan, nan], [['a', 'b', 'dd']])
        actual = divide(y1, y2, join='outer', missone=1, misstwo=2)
        desired = larry([1, 2, 1, 1], [['a', 'b', 'c', 'dd']], dtype=float)
        msg = "divide failed"
        ale(actual, desired, msg, original=y1)
        ale(actual, desired, msg, original=y2)
                    
