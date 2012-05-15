# Pysis
A robust toolkit for using [USGS ISIS 3](http://isis.astrogeology.usgs.gov/) in Python.

## How to install
First you must have [USGS ISIS 3](http://isis.astrogeology.usgs.gov/) installed on your machine. Click [here](http://isis.astrogeology.usgs.gov/documents/InstallGuide/index.html) for the ISIS 3 installation guide. Remember to set your environmental variables (see step 4 of USGS ISIS guide). Then, download the Pysis files from github. Run the setup.py script to install the Pysis packages.

## Quickstart Guide
How to write ISIS 3 code in python using Pysis.

Using ISIS 3 at the command line you might want to run the following basic commands (examples for the MDIS camera on the MESSENGER mission):

`mdis2isis from=filename.IMG to=filename.cub
 spiceinit from=filename.cub
 mdiscal from=filename.cub to=filename.cal.cub`

 using Pysis the syntax is:

`from pysis.commands import isis
 from pysis.util import file_variations`

to import the packages, then

`(cub_name, cal_name) = file_variations(img_name, ['.cub', '.cal.cub'])`

to set the desired filename variaitons, and then

`isis.mdis2isis(from_=img_name, to=cub_name)
 isis.spiceinit(from_=cub_name)
 isis.mdiscal(from_=cub_name, to=cal_name)`

In python function form, this short set of commands can be written as:

`def basic_img_proc(img_name):
    (cub_name, cal_name) = file_variations(img_name, ['.cub', '.cal.cub'])
    isis.mdis2isis(from_=img_name, to=cub_name, target='MERCURY')
    isis.spiceinit(from_=cub_name)
    isis.mdiscal(from_=cub_name, to=cal_name)`

where the function is passed the string image_name and returns nothing.
   
### Numerical and String Arguments

Here is an example of the maptemplate and cam2map commands in Pysis:

`isis.maptemplate(map='MDIS_eqr.map', projection='equirectangular', clon=0.0, clat=0.0, resopt='mpp', resolution=1000, rngopt='user', minlat=-10.0, maxlat=10.0, minlon=-10.0, maxlon=10.0)`

`isis.cam2map(from_=cal_name, to=proj_name, pixres='map', map='MDIS_eqr.map', defaultrange='map')`

where proj_name is set by:

`(cub_name, cal_name, proj_name) = file_variations(img_name, ['.cub', '.cal.cub', '.proj.cub'])`