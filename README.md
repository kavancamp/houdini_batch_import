# Houdini Geometry Import Tool

A Python utility script for SideFX Houdini that batch-imports multiple geometry files, automatically builds a clean SOP network, applies uniform scaling, and merges everything into a single output.
This tool supports Alembic and standard geometry formats and is designed to speed up scene assembly workflows.

## Features

Interactive file selection via Houdini UI
Supports multiple geometry formats:
Alembic (.abc)
FBX / OBJ / BGEO / other Houdini-supported geometry

Automatic SOP network creation:
File / Alembic loader
Unpack (for Alembic)
Transform (scale normalization)
Material node
Merge all inputs
Final OUT null
Consistent scale normalization (0.01) for all imports
Clean node layout and naming

## How It Works
Prompts the user to select one or more geometry files.
Creates a new Geometry container node (tempGeo) under /obj.
For each selected file:
  Alembic files (.abc):
  Alembic SOP
  Unpack SOP
  Transform SOP (scale = 0.01)
  Material SOP
  Other geometry formats:
  File SOP
  Transform SOP (scale = 0.01)
  Material SOP
All geometry is merged into a single Merge SOP.
Outputs everything through a _OUT_ null with display and render flags enabled.


## Usage

1. Open Houdini.
2. Open a Python Shell, Shelf Tool, or Script Editor.
3. Paste and run the script.
4. Select one or more geometry files when prompted.
5. The geometry will be imported and ready for shading or further processing.

Requirements
SideFX Houdini (tested with Python API hou)
Geometry files supported by Houdini


## Notes: 
All imported assets are uniformly scaled to 0.01, which is useful for DCC scale normalization.
Alembic files are automatically unpacked for SOP-level access.
The script assumes file extensions are used to detect Alembic (.abc).

### Possible Improvements
Custom scale control via UI
Automatic material assignment
Per-asset transform controls
Error handling for unsupported file types
Option to import into an existing Geometry node
