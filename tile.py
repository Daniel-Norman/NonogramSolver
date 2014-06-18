'''
Created on Jun 16, 2014

@author: Daniel Norman
Copyright Daniel Norman 2014
'''
class Tile(object):
    owner = None
    type = 'none'
    def __init__(self):
        '''
        Constructor
        '''
        pass
    def set_filled(self, owner):
        self.owner = owner
        if self.type != 'filled':
            self.owner.filled += 1
            self.type = 'filled'
        
    def set_empty(self):
        self.type = 'empty'

        
