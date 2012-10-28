# .obj to binary file format converter

Converts a .obj file to a more easily readable binary file format using Python.

## Examples
1. Just drag and drop multiple .obj files onto the python file.

2. From command line
```
objConveter.py file1.obj file2.obj
```

## Issues
* Only works if there's one group in the .obj file. Otherwise, issues _will_ happen.
* Displays a warning for group lines. This warning is harmless and can be ignored.
* Can only have a maximum of 65535 vertices in the .obj file. Having more will result in struct.error.
* No material support

## .model file format
```
4 Bytes: Number of vertex positions (#vp)
(#vp * 4 * 3) Bytes: Vertex position definitions

4 Bytes: Number of vertex normals (#vn)
(#vn * 4 * 3) Bytes: Vertex normal definitions

4 Bytes: Number of vertex texture coordinates (#vt)
(#vt * 4 * 2) Bytes: Vertex texture coordinate definitions

4 Bytes: Number of faces (#f)
(#f * 2) Bytes: Vertex position indices
(#f * 2) Bytes: Vertex texture coordinate indices
(#f * 2) Bytes: Vertex normal indices
```