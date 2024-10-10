<h2>deed virtual drive (WIP) </h2> 

Create, manage, and visualize subst drives easily.


![image](https://github.com/user-attachments/assets/214d2b75-07fa-4046-951a-27ca24032a1e)



License:
---
GNU General Public License (GPL)

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.   

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.   

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.   


pyinstaller spec generation command:
```
pyinstaller --paths env\Lib\site-packages deed_virtual_drive_ui.py --onedir --windowed --hidden-import "PySide6.QtXml" --hidden-import "PySide6.QtUiTools" --add-data rsrc:rsrc\image --add-data ui:rsrc\ui --add-data style:rsrc\style --name "deed virtual drive" 
```