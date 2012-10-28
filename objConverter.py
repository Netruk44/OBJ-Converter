import sys     # exit, argv
import struct  # pack

# NOTE: Change this for whatever architecture will be reading
#       the output file.
BIG_ENDIAN = True

# NOTE: Change this if you don't want to use the .model file
#       extension
FILE_EXTENSION = ".model"

# For use in outputting error messages and exiting.
def Error(errorMsg):
  print "ERROR: " + str(errorMsg)
  sys.exit(1)

# Functions used for adding onto the data lists.
  
def AppendVert(vertList, line):
  positions = line.split(' ')
  
  if len(positions) != 3:
    print "INFO: " + str(positions)
    Error("Malformed Vertex Position: '%s'" % line)
    
  positions = [float(x) for x in positions]
    
  vertList.append(tuple(positions))
  
def AppendNorm(normList, line):
  normals = line.split(' ')
  
  if len(normals) != 3:
    print "INFO: " + str(normals)
    Error("Malformed Vertex Normal: '%s'" % line)
    
  normals = [float(x) for x in normals]
    
  normList.append(tuple(normals))
  
def AppendTC(texCoordList, line):
  UV = line.split(' ')
  
  # Even though most UVs have two dimensions, it's possible
  # to have a 3D texture.
  if len(UV) != 3:
    print "INFO: " + str(UV)
    Error("Malformed Texture Coordinate: '%s'" % line)
    
  UV = [float(x) for x in UV]
    
  texCoordList.append(tuple(UV))
  
def AppendFace(faceList, line):
  triInfo = line.split(' ')
  
  if len(triInfo) != 3:
    Error("Malformed Face Definition: '%s'" % line)
    
  # "1/1/1" to ("1", "1", "1")
  triInfo = [tuple(x.split('/')) for x in triInfo]
  
  # str to int
  for i in xrange(3):
    triInfo[i] = tuple([int(x) for x in triInfo[i]])
    
  faceList.append(tuple(triInfo[0]))
  faceList.append(tuple(triInfo[1]))
  faceList.append(tuple(triInfo[2]))
  
def AppendComment(_1, _2):
  # It's a comment. Ignore it.
  pass

def ConvertModel(filename):
  verts = []
  norms = []
  texCoords = []
  faces = []
  
  # Read the file into a text buffer
  file = open(filename)
  fileText = file.read()
  file.close()
  del file
  
  # Interpret the file
  # Define the things that could be at the start of the line
  ActionDict = {
    'v' : (AppendVert, verts),
    'vn': (AppendNorm, norms),
    'vt': (AppendTC, texCoords),
    'f' : (AppendFace, faces),
    '#' : (AppendComment, None),
  }
  
  for line in fileText.split('\n'):
    line = line.strip() # Strip whitespace from line
    
    # Check if line was all whitespace
    if len(line) == 0:
      continue
      
    # Read the first token in the string
    firstSpace = line.find(' ')
    firstToken = ""
    restOfString = ""
    
    # Was there more than one token?
    if firstSpace != -1:
      firstToken = line[:firstSpace]
      restOfString = line[firstSpace + 1:].strip()
    else:
      firstToken = line
    
    # Make sure the token is a known one.
    if firstToken not in ActionDict:
      print "WARNING: Token '" + firstToken + "' was unknown! Skipping..."
      print "INFO: Unknown Line was: '" + line + "'"
      continue
      
    # Token is known. Read the data.
    ListAppender, List = ActionDict[firstToken]
    
    ListAppender(List, restOfString)
    
    
  # Write out the file
  endianType = ">" if BIG_ENDIAN else "<"
  
  outFilename = filename
  outFilename = outFilename[:outFilename.rfind('.')]
  outFilename += FILE_EXTENSION
  out = open(outFilename, 'wb')
  
  # Write vertex positions
  out.write(struct.pack(endianType + "I", len(verts)))
  for v in verts:
    x, y, z = v
    out.write(struct.pack(endianType + "f", x))
    out.write(struct.pack(endianType + "f", y))
    out.write(struct.pack(endianType + "f", z))
    
  # Write vertex normals
  out.write(struct.pack(">I", len(norms)))
  for n in norms:
    x, y, z = n
    out.write(struct.pack(endianType + "f", x))
    out.write(struct.pack(endianType + "f", y))
    out.write(struct.pack(endianType + "f", z))
    
  # Write Tex Coords
  out.write(struct.pack(endianType + "I", len(texCoords)))
  for uv in texCoords:
    x, y, z = uv
    out.write(struct.pack(endianType + "f", x))
    out.write(struct.pack(endianType + "f", y))
    
  # Write Faces
  posIdx = [x[0] for x in faces]
  uvIdx = [x[1] for x in faces]
  nrmIdx = [x[2] for x in faces]
  
  out.write(struct.pack(endianType + "I", len(faces)))
  
  # Subtract 1 from each element, since .obj is 1-indexed and not 0-indexed
  for p in posIdx:
    out.write(struct.pack(endianType + "H", p-1))
    
  for uv in uvIdx:
    out.write(struct.pack(endianType + "H", uv-1))
    
  for nrm in nrmIdx:
    out.write(struct.pack(endianType + "H", nrm-1))
    
  out.close()
  
def PrintUsage():
  print ".obj Converter"
  print ""
  print "Usage:"
  print "objConverter.py file1.obj [file2.obj ... ]"

if __name__ == "__main__":
  # Check to see if command line was supplied
  if len(sys.argv) == 1:
    PrintUsage()
    sys.exit(1)
    
  for file in sys.argv[1:]:
    ConvertModel(file)