# Change-Log-Tool

Note: alot of issues and missing features still remain - if anyone can provide better documentation for this under **Features** or **Controls** it would be vastly appreciated

### Controls:
-  Right click - selects entire row (unused)
-  Left click - Edit selected cell
-  [+] - Adds a row
-  [-] - Removes selected row

### Features:
- Stores paths of changelog directories alongside a name
- Allows creation of a changelog for every day
- Allows quick context menu for editing previous changelog and current day's changelog (Will be updated with changelog view soon and maybe even an entire editor)
- Mergelog 
   - Copies all files into a single one
   - Creates any missing files in directory
   - Can be updated
   - All changelogs in directory can be deleted once Mergelog is updated/created

### To add:
Check Issues!

### Works on:
- Windows: Yes!
- Mac: Needs testing!
- Linux: Uknown!

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
