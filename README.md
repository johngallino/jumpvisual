# Jumpvisual Dispatch Protocol
JumpVisual provides real estate photography services to real estate agencies in New Jersey, New York and Connecticut. This is a python application designed to help dispatch staff photographers to jobs in their preferred areas.

The main program is jumpvisualdb.exe, located in the 'dist 'directory.

In the upper half of the program, the dispatcher can view every photographer's profile information which includes their contact info and services provided. In the lower half, the dispatcher can search for any town in NY, NJ or CT and immediately see who covers that town. Because some town names are repeated (ex. there are three 'Washington Townships' in New Jersey), a check is put in place for that.

Photographer information can be easily added, deleted or edited from within the main program. When onboarding a new photographer, coverage area is first narrowed down by state(s), then counties, and finally cities.

All information is retained in the jump.db database file. The software uses SQLite, with a many-to-many relationship between photographers and towns.


![Screenshot of JumpVisual Dispatch Protocol](https://github.com/johngallino/jumpvisual/blob/master/screenshot1.jpg)
![Screenshot of JumpVisual Dispatch Protocol](https://github.com/johngallino/jumpvisual/blob/master/screenshot2.jpg)
![Screenshot of JumpVisual Dispatch Protocol](https://github.com/johngallino/jumpvisual/blob/master/screenshot3.jpg)
![Screenshot of JumpVisual Dispatch Protocol](https://github.com/johngallino/jumpvisual/blob/master/screenshot4.jpg)
