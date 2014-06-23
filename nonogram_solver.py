'''
Created on Jun 16, 2014

@author: Daniel Norman
Copyright Daniel Norman 2014
'''
import sys

def in_range(index, rng):
    return index >= 0 and index < len(rng)

class NonogramSolver:
    def __init__(self):
        pass
    
    def print_row(self, row, numbers, filled_char = 'X', empty_char = ' ', none_char = '_'):
        for number in numbers:
            print number.size,
        sys.stdout.write('[')
        for index, tile in enumerate(row):
            if tile.type == 'none':
                sys.stdout.write(none_char)
            elif tile.type == 'empty':
                sys.stdout.write(empty_char)
            elif tile.type == 'filled':
                sys.stdout.write(filled_char)
            if index % 5 == 4 and index + 1 < len(row):
                sys.stdout.write('|')
            elif index != len(row) - 1:
                sys.stdout.write(':')
        sys.stdout.write(']\n')
    def print_grid(self, tile_grid, filled_char = 'X', empty_char = 'O', none_char = '_'):
        for row in tile_grid:
            self.print_row(row, [], filled_char, empty_char, none_char)
        sys.stdout.write('\n')
        sys.stdout.flush()
        
    def solve_grid(self, grid, numbers, functions, max_tries):
        for k in range(max_tries):
            completed_rows = 0
            for i in range(len(grid) * 2):
                if i < len(grid):
                    row = grid[i]
                    for func in functions:
                        if not self.is_row_complete(row):
                            func(row, numbers[i], 'horiz')
                            #self.check_sides(row, numbers[i], 'horiz')
                        else:
                            completed_rows += 1
                            break
                else:
                    row = [grid[x][i - len(grid) * 2] for x in range(len(grid))]
                    for func in functions:
                        if not self.is_row_complete(row):
                            func(row, numbers[i], 'vert')
                            #self.check_sides(row, numbers[i], 'vert')
                        else:
                            completed_rows += 1
                            break
                if completed_rows == len(grid) * 2:
                    print 'Finished in %s grid searches.' % (k)
                    return
                
    def is_row_complete(self, row):
        for tile in row:
            if not tile.is_empty() and not tile.is_filled():
                return False
        return True
        
    def check_overlap(self, row, numbers, orient):
        '''Checks if there are known filled tiles due to overlapping possible tiles, sets filled if found'''
        tile_owners = [None for _ in range(len(row))]
                
        for numb in numbers:
            numb.temporary_size = numb.size
            
        number_index = 0
        
        for index, tile in enumerate(row):
            if not in_range(number_index, numbers):
                break
            
            if tile.is_empty():
                if numbers[number_index].temporary_size > 0:
                    for i in range(index - (numbers[number_index].size - numbers[number_index].temporary_size), index):
                        tile_owners[i] = None
                    numbers[number_index].temporary_size = numbers[number_index].size
                else:
                    number_index += 1
                continue
            
            if numbers[number_index].temporary_size > 0:        
                tile_owners[index] = numbers[number_index]
                numbers[number_index].temporary_size -= 1
            else:
                number_index += 1
                
        number_index = len(numbers) - 1
        for numb in numbers:
            numb.temporary_size = numb.size
        
        for i, tile in enumerate(row[::-1]):
            index = (len(row) - 1) - i
            if not in_range(number_index, numbers):
                break
            if row[index].is_empty():
                if numbers[number_index].temporary_size > 0:
                    numbers[number_index].temporary_size = numbers[number_index].size
                else:
                    number_index -= 1
                continue
            
            if numbers[number_index].temporary_size > 0:
                if tile_owners[index] is numbers[number_index]:
                        row[index].set_filled(numbers[number_index], orient)
                numbers[number_index].temporary_size -= 1
            else:
                number_index -= 1
        
        
    def check_overlap_without_owners(self, row, numbers, orient):
        '''Checks if there are known filled tiles due to overlapping possible tiles (even if tiles' owners aren't known), sets filled if found'''
        tile_owners = [None for _ in range(len(row))]
                
        for numb in numbers:
            numb.temporary_size = numb.size
            
        number_index = 0
        for index, tile in enumerate(row):
            if numbers[number_index].temporary_size == 0:
                number_index += 1
            
            if not in_range(number_index, numbers):
                break
            
            if tile.is_empty():
                if numbers[number_index].temporary_size > 0:
                    numbers[number_index].temporary_size = numbers[number_index].size
                else:
                    number_index += 1
                continue
            
            if tile.is_filled() or numbers[number_index].temporary_size < numbers[number_index].size:
                tile_owners[index] = numbers[number_index]
                numbers[number_index].temporary_size -= 1
                continue

  
        for numb in numbers:
            numb.temporary_size = numb.size
            
        number_index = len(numbers) - 1
        for i, tile in enumerate(row[::-1]):
            index = (len(row) - 1) - i
            if numbers[number_index].temporary_size == 0:
                number_index -= 1
                
            if not in_range(number_index, numbers):
                break
            
            if tile.is_empty():
                if numbers[number_index].temporary_size > 0:
                    numbers[number_index].temporary_size = numbers[number_index].size
                else:
                    number_index -= 1
                continue
            
            
            if tile.is_filled() or numbers[number_index].temporary_size < numbers[number_index].size:
                if tile_owners[index] is numbers[number_index]:
                    row[index].set_filled(numbers[number_index], orient)
                numbers[number_index].temporary_size -= 1
                continue
            
                
    def check_empty_group(self, row, numbers, orient):
        '''Checks the row one group of unfilled tiles at a time, to see if they should be empty because of coming before a filled tile'''
        group = []
        number_index = 0
        last_passed_index = -1
        
        for tile in row:
            if not tile.is_filled():
                group.append(tile)
            else:
                if tile.get_owner(orient) is numbers[number_index]:
                    last_passed_index = number_index
                    overlay = numbers[number_index].size - numbers[number_index].filled
                    while overlay > 0 and len(group) > 0:
                        group.pop()
                        overlay -= 1
                    for t in group:
                        t.set_empty()
                    group = []
                    
                elif last_passed_index == number_index and in_range(number_index + 1, numbers) and tile.get_owner(orient) is numbers[number_index + 1]:
                    number_index += 1
                    last_passed_index = number_index
                    overlay_right = numbers[number_index].size - numbers[number_index].filled
                    while overlay_right > 0 and len(group) > 0:
                        group.pop()
                        overlay_right -= 1
                    overlay_left = numbers[number_index - 1].size - numbers[number_index - 1].filled
                    while overlay_left > 0 and len(group) > 0:
                        group.pop(0)
                        overlay_left -= 1
                    for t in group:
                        t.set_empty()
                    group = []
                else:
                    break
                
        group = []
        number_index = len(numbers) - 1
        last_passed_index = -1
        
        for tile in row[::-1]:
            if not tile.is_filled():
                group.append(tile)
            else:
                if tile.get_owner(orient) is numbers[number_index]:
                    last_passed_index = number_index
                    overlay = numbers[number_index].size - numbers[number_index].filled
                    while overlay > 0 and len(group) > 0:
                        group.pop()
                        overlay -= 1
                    for t in group:
                        t.set_empty()
                    group = []
                    
                elif last_passed_index == number_index and in_range(number_index + 1, numbers) and tile.get_owner(orient) is numbers[number_index + 1]:
                    number_index += 1
                    last_passed_index = number_index
                    overlay_left = numbers[number_index].size - numbers[number_index].filled
                    while overlay_left > 0 and len(group) > 0:
                        group.pop()
                        overlay_left -= 1
                    overlay_right = numbers[number_index - 1].size - numbers[number_index - 1].filled
                    while overlay_right > 0 and len(group) > 0:
                        group.pop(0)
                        overlay_right -= 1
                    for t in group:
                        t.set_empty()
                    group = []
                else:
                    break        

        
    def check_owners(self, row, numbers, orient):
        for numb in numbers:
            numb.temporary_size = numb.size
        
        number_index = 0
        only_empty_so_far = True
        for tile in row:
            if not in_range(number_index, numbers):
                break

            if tile.is_empty():
                if numbers[number_index].is_filled():
                    number_index += 1
                    continue
                elif not only_empty_so_far:
                    break
            else:
                only_empty_so_far = False
                
            if numbers[number_index].temporary_size < 0:
                break
            
            numbers[number_index].temporary_size -= 1

            if tile.is_filled():
                tile.set_filled(numbers[number_index], orient)
              
        for numb in numbers:
            numb.temporary_size = numb.size
       
        number_index = len(numbers) - 1
        only_empty_so_far = True
        for tile in row[::-1]:
            if not in_range(number_index, numbers):
                break
            
            if tile.is_empty():
                if numbers[number_index].is_filled():
                    number_index -= 1
                    continue
                elif not only_empty_so_far:
                    break
            else:
                only_empty_so_far = False
            
            if numbers[number_index].temporary_size < 0:
                break
            
            numbers[number_index].temporary_size -= 1
                    
            if tile.is_filled():
                tile.set_filled(numbers[number_index], orient)
        
        
        current_owner = None
        for tile in row:
            if tile.is_empty() or (not tile.is_empty() and not tile.is_filled()):
                current_owner = None
            
            if tile.is_filled():
                if tile.get_owner(orient) is None and current_owner is not None:
                    tile.set_filled(current_owner, orient)
                elif tile.get_owner(orient) is not None:
                    current_owner = tile.get_owner(orient)
            
        
        current_owner = None        
        
        for tile in row[::-1]:
            if tile.is_empty() or (not tile.is_empty() and not tile.is_filled()):
                current_owner = None
            
            if tile.is_filled():
                if tile.get_owner(orient) is None and current_owner is not None:
                    tile.set_filled(current_owner, orient)
                elif tile.get_owner(orient) is not None:
                    current_owner = tile.get_owner(orient)
        
    def check_sides(self, row, numbers, orient):
        '''Sets all tiles on the side of filled tile groups as empty'''
        for index, tile in enumerate(row):
            left_index = index - 1
            right_index = index + 1
            if tile.get_owner(orient) is not None and tile.get_owner(orient).is_filled():
                if left_index >= 0 and row[left_index].type != 'filled':
                    row[left_index].set_empty()
                if right_index < len(row) and row[right_index].type != 'filled':
                    row[right_index].set_empty()
    
    def check_filled_between(self, row, numbers, orient):
        '''Checks if there are unknown tiles between known filled tiles from the same owner, sets filled if found'''
        index_left = -1
        current_number = None

        for index, tile in enumerate(row):
            if tile.get_owner(orient) is not None:
                if index_left == -1:
                    index_left = index
                if tile.get_owner(orient) is current_number:
                    for t in row[index_left + 1:index]:
                        if t.is_empty():
                            print 'trying to fill empty tile'
                        t.set_filled(current_number, orient)
                        
                else:
                    index_left = index
                current_number = tile.get_owner(orient)
                

    
    def check_filled_constrained(self, row, numbers, orient):
        '''Checks if there must be filled tiles next to a known filled tile due to lack of space on one side'''
        for index, tile in enumerate(row):
            overlap = -1
            if tile.get_owner(orient) is not None and not tile.get_owner(orient).is_filled():
                for i in range(index, index - tile.get_owner(orient).size, -1):
                    if i < 0 or row[i].is_empty() or (row[i].get_owner(orient) is not None and row[i].get_owner(orient) is not tile.get_owner(orient)):
                        overlap = index - i - 1
                        break 
                if overlap >= 0:
                    for t in row[index:index + (tile.get_owner(orient).size - overlap)]:
                        t.set_filled(tile.get_owner(orient), orient)
                        
        for i, tile in enumerate(row[::-1]):
            index = (len(row) - 1) - i
            overlap = -1
            if tile.get_owner(orient) is not None and not tile.get_owner(orient).is_filled():
                for i in range(index + 1, index + tile.get_owner(orient).size):
                    if i == len(row) or row[i].is_empty() or (row[i].get_owner(orient) is not None and row[i].get_owner(orient) is not tile.get_owner(orient)):
                        overlap = i - index - 1
                        break
                if overlap >= 0:
                    for t in row[index - (tile.get_owner(orient).size - overlap) + 1:index]:
                        t.set_filled(tile.get_owner(orient), orient)
                

