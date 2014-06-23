'''
Created on Jun 16, 2014

@author: Daniel Norman
Copyright Daniel Norman 2014
'''
class Tile(object):
    def __init__(self):
        '''
        Constructor
        '''
        self.owner_vert = None
        self.owner_horiz = None
        self.type = 'none'
        pass
    def set_filled(self, owner, orient):
        if orient == 'vert':
            if self.owner_vert is None and owner is not None:
                self.owner_vert = owner
                self.owner_vert.filled += 1
                if self.owner_vert.filled > self.owner_vert.size:
                    print 'overfilled!'
        else:
            if self.owner_horiz is None and owner is not None:
                self.owner_horiz = owner
                self.owner_horiz.filled += 1
                if self.owner_horiz.filled > self.owner_horiz.size:
                        print 'overfilled!'
        self.type = 'filled'
        
    def set_empty(self):
        if self.type == 'filled':
            print 'trying to set filled as empty'
        self.type = 'empty'
    
    def get_owner(self, orient):
        return self.owner_vert if orient == 'vert' else self.owner_horiz
    
    
    def is_filled(self):
        return self.type == 'filled'
    def is_empty(self):
        return self.type == 'empty'

        
