# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 19:21:48 2016

@author: phyrct
"""
from Stoner.Image import ImageArray,ImageFile
import unittest
from os.path import dirname,join

thisdir=dirname(__file__)

class FuncsTest(unittest.TestCase):
    
    def setUp(self):
        self.a=ImageArray(join(thisdir,'coretestdata/im2_noannotations.png'))
        self.a1=ImageArray(join(thisdir,'coretestdata/im1_annotated.png'))
        
    def test_funcs(self):
        b=self.a.translate((2.5,3))
        self.c=b.correct_drift(ref=self.a)
        self.d=b.align(self.a,method="scharr")
        print(self.d["tvec"],self.c["correct_drift"])
#        print("#"*80)
#        print(self.a.metadata)
#        print(self.a1.metadata)
#        print(all([k in self.a.metadata.keys() for k in self.a1.metadata.keys()]))
                
if __name__=="__main__": # Run some tests manually to allow debugging
    test=FuncsTest("test_funcs")
    test.setUp()
    unittest.main()

