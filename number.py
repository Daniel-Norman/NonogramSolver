'''
Created on Jun 16, 2014

@author: Daniel Norman
Copyright Daniel Norman 2014
'''

class Number(object):
    def __init__(self, size):
        '''
        Constructor
        '''
        self.size = size
        self.temporary_size = size
        self.filled = 0

    def is_filled(self):
        return self.filled >= self.size
    
    def __repr__(self):
        return 'Number: %s    Filled: %s' % (self.size, self.filled)