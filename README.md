# Change-Log-Tool

### Controls:
-  Right click - Edits selected cell / Opens Context menu for selected cell
-  [+] - Adds a row
-  [-] - Removes selected row

### Features:
- Stores Changelogs location and name
- More to be added soon.... 
   -   Changelog explorer
   -   Maybe (but seems very much like a gimmick (infact it is)): Changelog compatability perceptron (bassically a perceptron which looks through all your   other changelogs and sees if they match or if theres problems with them - such as a different format)
   -   Settings menu
   -   Mergelog (merges all changelogs into a single file - with option to delete whats been merged or to keep it)
   -   Maybe: Custom file type (which would be read by a custom editor built within this app - however this largely increases the scope so will be left for later)

### Dev:
- Requires:
   - PYQT5 module
   - OS module
   - Datetime module 
   - heapq module
   - glob module
   - yaml module (not the new one [ruamel.yaml] (yes i use the old one - mwaahahahhaha))
   - random module
   - math module
   - Permission to read/write to folders and files
