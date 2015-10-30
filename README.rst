===============================
Pysis
===============================

.. image:: https://badge.fury.io/py/pysis.svg
    :target: http://badge.fury.io/py/pysis

.. image:: https://travis-ci.org/wtolson/pysis.svg?branch=master
        :target: https://travis-ci.org/wtolson/pysis

.. image:: https://pypip.in/d/pysis/badge.png
        :target: https://pypi.python.org/pypi/pysis


Toolkit for using USGS Isis in Python.

* Free software: BSD license
* Documentation: http://pysis.readthedocs.org.


How to install
--------------

At the command line::

    $ easy_install pysis

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv pysis
    $ pip install pysis


Dependencies
~~~~~~~~~~~~

For working with ISIS commands, you must firts have `USGS ISIS 3`_ installed on
your machine. See the ISIS 3 `installation guide`_ for further instructions.
Remember to set your environmental variables (see step 4 of USGS ISIS guide) so
Pysis knows where your installation is.


Quickstart Guide
----------------

How to write ISIS 3 code in python using Pysis.

Using ISIS 3 at the command line you might want to run the following basic
commands (examples for the MDIS camera on the MESSENGER mission)::

    mdis2isis from=filename.IMG to=filename.cub
    spiceinit from=filename.cub
    mdiscal from=filename.cub to=filename.cal.cub

using Pysis the syntax is::

    from pysis.isis import mdis2isis, spiceinit, mdiscal
    from pysis.util import file_variations

    def calibrate_mids(img_name):
        (cub_name, cal_name) = file_variations(img_name, ['.cub', '.cal.cub'])

        mdis2isis(from_=img_name, to=cub_name)
        spiceinit(from_=cub_name)
        mdiscal(from_=cub_name, to=cal_name)

You will notice that we use the keyword `from_` when we call a command  because
`from` is a reserved word in python.


Numerical and String Arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here is an example of the maptemplate and cam2map commands in Pysis::

    from pysis import isis

    isis.maptemplate(map='MDIS_eqr.map', projection='equirectangular',
                     clon=0.0, clat=0.0, resopt='mpp', resolution=1000,
                     rngopt='user', minlat=-10.0, maxlat=10.0, minlon=-10.0,
                     maxlon=10.0)

    isis.cam2map(from_=cal_name, to=proj_name, pixres='map',
                 map='MDIS_eqr.map',defaultrange='map')


Getting values from ISIS commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pysis commands will return the command's STDOUT as a byte string. If the command
returns a nonzero exit code, a `ProcessError` will be thrown. This example
command uses `getkey` to receive values from the label of an ISIS cube::

    from pysis.isis import getkey

    value = getkey(from_='W1467351325_4.map.cal.cub',
                   keyword='minimumringradius', grp='mapping')


Catching ProcessingErrors
~~~~~~~~~~~~~~~~~~~~~~~~~

Pysis supports catching `ISIS` processing errors like so::

    from pysis.exceptions import ProcessError
    from pysis.isis import hi2sis
    
    try:
        hi2isis(from_=filein, to=fileout)
    except ProcessError as e:
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        
Multiprocessing Isis Commands with IsisPool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pysis has built-in support to make multiprocessing isis commands simple. To run
the above MDIS calibration script for multiple images in multiple processes we
could rewrite the function as so::

    from pysis import IsisPool
    from pysis.util import ImageName

    def calibrate_mdis(images):
        images = [ImageName(filename) for filename in images]

        with IsisPool() as isis_pool:
            for filename in images:
                isis_pool.mdis2isis(from_=filename.IMG, to=filename.cub)

        with IsisPool() as isis_pool:
            for filename in images:
                isis_pool.spiceinit(from_=filename.cub)

        with IsisPool() as isis_pool:
            for filename in images:
                isis_pool.mdiscal(from_=filename.cub, to=filename.cal.cub)

When using IsisPool we can't determine which order commands will be executed in
so we much run each command for all the files as a group before moving to the
next command and creating a new IsisPool.


.. _USGS ISIS 3: http://isis.astrogeology.usgs.gov/
.. _installation guide: http://isis.astrogeology.usgs.gov/documents/InstallGuide/
