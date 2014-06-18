'''
Created on Jun 16, 2014

@author: Daniel Norman
Copyright Daniel Norman 2014
'''
class NonogramSolver:
    def __init__(self):
        pass
    def print_row(self, row, numbers):
        for number in numbers:
            print number.size,
        print '[',
        for index, tile in enumerate(row):
            if tile.type == 'none':
                print ' ',
            elif tile.type == 'empty':
                print 'X',
            else:
                print 'O',
            if index == 4 or index == 9:
                print '|',
            elif index != len(row) - 1:
                print ':',
        print ']'
        
    def check_overlap(self, row, numbers):
        '''Checks if there are known filled tiles due to overlapping possible tiles, sets filled if found'''
        tile_owners = [None for _ in range(len(row))]       #Hold temporary owners of each tile
                
        for numb in numbers:
            numb.temporary_size = numb.size
            
        number_index = 0
        
        for index, tile in enumerate(row):
            if number_index == len(numbers):        #break if out of numbers
                break
            
            if tile.type == 'empty':
                if numbers[number_index].temporary_size > 0:        #if we encounter an empty tile while filling out temporary owners,
                    for i in range(index - (numbers[number_index].size - numbers[number_index].temporary_size), index):     #reset all the spots that we would have set from this number
                        tile_owners[i] = None
                    numbers[number_index].temporary_size = numbers[number_index].size       #reset this number
                else:
                    number_index += 1       #move on to the next number if we filled tiles up until an empty tile
                continue
            
            if numbers[number_index].temporary_size > 0:        
                tile_owners[index] = numbers[number_index]      #set this tile's temporary owner as our current number
                numbers[number_index].temporary_size -= 1
            else:
                number_index += 1
                
        number_index = len(numbers) - 1
        for numb in numbers:
            numb.temporary_size = numb.size
        
        for i, tile in enumerate(row[::-1]):
            index = (len(row) - 1) - i
            if number_index < 0:
                break
            if row[index].type == 'empty':
                if numbers[number_index].temporary_size > 0:
                    numbers[number_index].temporary_size = numbers[number_index].size
                else:
                    number_index -= 1
                continue
            
            if numbers[number_index].temporary_size > 0:
                if numbers[number_index] is tile_owners[index]:     #if the tile's temporary owner is the same number as when going backwards, its real owner must be that number
                        row[index].set_filled(numbers[number_index])
                numbers[number_index].temporary_size -= 1
            else:
                number_index -= 1
            
    
    def check_empty_between(self, row, numbers):
        '''Checks if there are empty tiles between known empty tiles, sets empty if found'''
        '''TODO check empty between filled tiles'''
        index_left = 0
        number_index = 0
        move_next_number = False
        for index, tile in enumerate(row):
            if tile.owner is not None:
                if tile.owner is not numbers[number_index]:
                    number_index += 1
                move_next_number = True
            if tile.type != 'empty':
                continue
            else:
                if numbers[number_index].size > (index - index_left):
                    for empty_tile in row[index_left:index + 1]:
                        empty_tile.set_empty()
                index_left = index + 1
                if move_next_number:
                    number_index += 1
                move_next_number = False
        
        if number_index == len(numbers) or numbers[number_index].size > (index - index_left):
                    for empty_tile in row[index_left:index + 1]:
                        empty_tile.set_empty()
        
        index_right = len(row) - 1
        number_index = len(numbers) - 1
        move_next_number = False
        
        for i, tile in enumerate(row[::-1]):
            index = (len(row) - 1) - i
            if tile.owner is not None:
                if tile.owner is not numbers[number_index]:
                    number_index -= 1
                move_next_number = True
            if tile.type != 'empty':
                continue
            else:
                if numbers[number_index].size > (index_right - index):
                    for empty_tile in row[index:index_right + 1]:
                        empty_tile.set_empty()
                index_right = index - 1
                if move_next_number:
                    number_index -= 1
                move_next_number = False
        if number_index == -1 or numbers[number_index].size > (index_right - index):
                    for empty_tile in row[index:index_right + 1]:
                        empty_tile.set_empty()
                
    def check_sides(self, row, numbers):
        '''Sets all tiles on the side of filled tile groups as empty'''
        for index, tile in enumerate(row):
            left_index = index - 1
            right_index = index + 1
            if tile.owner is not None and tile.owner.is_filled():
                if left_index >= 0 and row[left_index].type != 'filled':
                    row[left_index].set_empty()
                if right_index < len(row) and row[right_index].type != 'filled':
                    row[right_index].set_empty()
    
    def check_filled_between(self, row, numbers):
        '''Checks if there are unknown tiles between known filled tiles from the same owner, sets filled if found'''
        index_left = -1
        current_number = None
        for index, tile in enumerate(row):
            if tile.owner is not None:
                if index_left == -1:
                    index_left = index
                if tile.owner is current_number:
                    for t in row[index_left + 1:index]:
                        t.set_filled(current_number)
                else:
                    index_left = index
                current_number = tile.owner
                

    
    def check_filled_constrained(self, row, numbers):
        '''Checks if there must be filled tiles next to a known filled tile due to lack of space on one side'''
        for index, tile in enumerate(row):
            overlap = -1
            if tile.owner is not None and not tile.owner.is_filled():
                for i in range(index, index - tile.owner.size, -1):
                    if i < 0 or row[i].type == 'empty' or (row[i].owner is not None and row[i].owner is not tile.owner):
                        overlap = index - i - 1
                        break
                if overlap >= 0:
                    for t in row[index:index + (tile.owner.size - overlap)]:
                        t.set_filled(tile.owner)
                        
        for i, tile in enumerate(row[::-1]):
            index = (len(row) - 1) - i
            overlap = -1
            if tile.owner is not None and not tile.owner.is_filled():
                for i in range(index + 1, index + tile.owner.size):
                    if i == len(row) or row[i].type == 'empty' or (row[i].owner is not None and row[i].owner is not tile.owner):
                        overlap = i - index - 1
                        break
                if overlap >= 0:
                    for t in row[index - (tile.owner.size - overlap) + 1:index]:
                        t.set_filled(tile.owner)
                

