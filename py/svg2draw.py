#!/usr/bin/env python

from xml.dom import minidom

def main():

    # TODO: read file as argument
    doc = minidom.parse("test.svg")

    height = 0
    
    # Walk the elements until <svg> is found, then break
    for elem in doc.getElementsByTagName('svg'):
        # Strip unit from height
        heightStripped = stripUnit(elem.getAttribute('height'))

        # If heightStripped was successfully computed, set height
        # to this value. Otherwise stripUnit() returns None, and
        # height remains unchanged.
        if heightStripped:
            height = heightStripped

        # Once we have found the height we don't need to walk any
        # further (although there is probably only one <svg> tag
        # antway...)
        break

    innerPaths = []
    outerPaths = []

    for path in doc.getElementsByTagName('path'):
        if path.getAttribute('id')[:5] == 'inner':
            innerPaths.append(path.getAttribute('d'))
        else:
            # Any paths where the ID does not begin with
            # 'inner' are interpreted as outer paths
            outerPaths.append(path.getAttribute('d'))

    doc.unlink()

    # TODO: deduce outfile name from infile
    with open('test.dat', 'w') as outfile:
        for path in outerPaths:
            for command in path2fill(path, 10, height):
                outfile.write(command + '\n')
        
        for path in innerPaths:
            for command in path2jumpfill(path, 10, height):
                outfile.write(command + '\n')
        
        # End with a jump to origin to avoid stray lines
        outfile.write("0 0 1\n")

def path2fill(pathString, multiplier, docHeight):
    return path2DRAWcoords(pathString, 2, multiplier, docHeight)

def path2jumpfill(pathString, fill_type, multiplier, docHeight):
    return path2DRAWcoords(pathString, 3, multiplier, docHeight)

def path2DRAWcoords(pathString, fill_type, multiplier, docHeight):
    # Empty list to hold coordinates
    coordList = []

    # Split the path at space characters
    pathData = pathString.split(' ')

    for elem in pathData:
        # If elem contains a comma we conclude that it is a coordinate
        if elem.find(',') >= 0:
            coordList.append(elem.split(','))

    # Empty list to hold formatted command
    commands = []

    for i, point in enumerate(coordList):
        x = int(round(float(point[0]) * multiplier))

        # (0,0) is top left in SVG, but bottom left in DRAW
        y = int(round((docHeight - float(point[1])) * multiplier))
        
        # Format command
        commands.append(str(x) + ' ' + str(y) + ' ' + str(fill_type if i == 0 else 0))

    # TODO: remove direct repetitions
    return commands

def stripUnit(string):
    """
Recursively remove characters from the end of <string> until only a number remains.

Returns a number if successful, or None if not.
"""
    if len(string) == 0:
        return None
    elif string.isnumeric():
        return float(string)
    else:
        return stripUnit(string[:-1])

if __name__ == '__main__':
    main()