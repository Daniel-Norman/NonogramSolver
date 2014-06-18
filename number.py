'''
Created on Jun 16, 2014

@author: Daniel Norman
Copyright Daniel Norman 2014
'''

class Number(object):
    filled = 0
    
    def __init__(self, size):
        '''
        Constructor
        '''
        self.size = size
        self.temporary_size = size

    def is_filled(self):
        return self.filled >= self.size