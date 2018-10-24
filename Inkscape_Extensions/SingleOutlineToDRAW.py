#!/usr/bin/env python

## SingleOutlineToDRAW extension for Inkscape
#
#  Based on Simarilius' extension 'ExportXY' which
#  does not explicitly state a license.
#  http://www.inkscapeforum.com/viewtopic.php?t=8826
#
#  Works on a single outline with less than 1000 nodes.

import inkex
import sys

class TemplateEffect(inkex.Effect):
    def __init__(self):
        # Call base class construtor.
        inkex.Effect.__init__(self)
        
        # Define string option "--what" with "-w" shortcut and default value "World".
        self.OptionParser.add_option('-m', '--mul', action = 'store',
            type = 'int', dest = 'mul', default = 10,
            help = 'Multiply coordinates by x')

    def effect(self):

        # Get script's "--mul" option value.
        mul = self.options.mul

        # Get access to main SVG document element and get its dimensions.
        svg = self.document.getroot()

        # Get the height of the document
        height  = self.unittouu(svg.get('height'))

        # Create the string variable which will hold the formatted data
        outputString = ""
        
        # Loop through all the selected items in Inkscape
        for id, node in self.selected.iteritems():

            # Check if the node is a path ( "svg:path" node in XML ) 
            if node.tag == inkex.addNS('path','svg'):

                # The 'd' attribute is where the path data is stored as a string
                pathData = node.get('d')

                # Split the string with the space character, thus getting an array of the actual SVG commands
                pathData = pathData.split(' ')

                # We want to know if i is the first coordinate we have encountered (Note: i == 0 may not be a coordinate)
                flagFirst = True

                # Iterate through all the coordinates, ignoring the 'M' (Move To) and 'z' (Close Path) commands.
                # Note that any other command (such as bezier curves) are unsupported and will likely make bad things happen...
                for i in range( len(pathData) ):

                    # If there is a comma, we know that we are dealing with coordinates (format "X,Y").
                    # Any other SVG command (such as 'M', 'z', etc.) are ignored.
                    if pathData[i].find(',') >= 0:
                        currentCoordinates = pathData[i].split(',')

                        # Compute the X and Y coordinates
                        # Note that we need to flip the SVG y values (where 0 is at the top)
                        x = int(round(float(currentCoordinates[0]) * mul))
                        y = int(round((height - float(currentCoordinates[1])) * mul))

                        # DRAW vector type (Z). Usually we want type 0 (line)...
                        vecType = 0
                        # ...except for the first coordinate which is type 2 (fill)
                        if flagFirst:
                            vecType = 2 
                            flagFirst = False

                        # Add X, Y, Z to outputString
                        outputString += str(x) + ' ' + str(y) + ' ' + str(vecType) + '\n'

        # Finally we want to jump back to origin
        outputString += "0 0 1"

        # Display the coordinates in a popup window
        sys.stderr.write(outputString)

# Create effect instance and apply it.
effect = TemplateEffect()
effect.affect()
