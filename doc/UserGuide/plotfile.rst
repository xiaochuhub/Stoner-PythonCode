*************
Plotting Data
*************
.. currentmodule:: Stoner.plot

Data plotting and visualisation is handled by the :py:class:`PlotMixin` sub-class of :py:class:`Stoner.Core.DataFile`.
The purpose of the methods detailed here is to provide quick and convenient ways to plot data rather than providing
publication ready figures. The :py:class:`PlotMixin` is included as apart of the Data class::

Quick Plots
===========

The :py:class:`PlotMixin` class is intended to help you make plots that look reasonably good with as little hassle as possible.
In common with many graph plotting programmes, it has a concept of declaring columns of data to be used for 'x', 'y' axes and
for containing error bars. This is done with the :py:attr:`DataFile.setas` attribute (see :ref:`setas` for full details). Once this is done, the plotting
methods will use these to try to make a sensible plot.::

   p.setas="xye"
   p.setas=["x","y","e"]
   print(p.setas)


Once the columns are identified, the :py:meth:`PlotMixin.plot` method can be used to do the actual plotting. This is simply a wrapper that insepects the
available columns and calls either :py:meth:`PlotMixin.plot_xy` or :py:meth:`PlotMixin.plot_xyz` as appropriate. All keyword arguments to :
py:meth:`PlotMixin.plot` are passed on to the actual plotting method.

Types of Plot
=============

:py:meth:`PlotMixin.plot` will try to make the msot sensible choice of plot depending on which columns you have specified and
the number of axes represetned.

    * x-y, x-y+-e, x-y-e-y-e etc. data will default to a 2D scatter plot with error bars
    * x-y-z data will be converted to a grid and plotted as a 3D surface plot.
    * x-y-u-v (i.e. 2D vectro fields) and x-y-u-v-w (3D vectros on a 2D plane) will be plotted as a colour image
        where the colour is mapped to hue-saturation-luminescence scale. The hue gives the in plane ange while the luminescene gives
        the out of plane component of the vector field.
    * x-y-z-u-v-w data (i.e. 3D vector field on a 3D grid) is represented as a 3D quiver plot with coloured quivers (using the same H-S-L
        colour space mapping as above) assuming mayavi is importable.

An alternative plot type for data with errorbars in :py:func:`plotutils.errorfill`. This uses a shaded line as an
alternative to the error bars, where the shading of the line varies from intense to transparent the further one
gets from the mean value. For 3D x-y-z plotting there is a :py:meth:`PlotMixin.contour_xyz` and a :py:meth:`PlotMixin.image_plot`
methods available. These give contonour plots and 2D colour map plots respectively.

Plotting 2D data
----------------

*x-y* plots are produced by the :py:meth:`PlotMixin.plot_xy` method::

   p.plot_xy(column_x, column_y)
   p.plot_xy(column_x, [y1,y2])
   p.plot_xy(x,y,'ro')
   p.plot_xy(x,[y1,y2],['ro','b-'])
   p.plot_xy(x,y,title='My Plot')
   p.plot_xy(x,y,figure=2)
   p.plot_xy(x,y,plotter=pyplot.semilogy)

The examples above demonstrate several use cases of the :py:meth:`PlotMixin.plot_xy` method. The first parameter is always
the x column that contains the data, the second is the y-data either as a single column or list of columns.
The third parameter is the style of the plot (lines, points, colours etc) and can either be a list if the y-column data
is a list or a single string. Finally additional parameters can be given to specify a title and to control which figure
is used for the plot. All matplotlib keyword parameters can be specified as additional keyword arguments and are passed
through to the relevant plotting function. The final example illustrates a convenient way to produce log-linear and log-log
plots. By default, :py:meth:`PlotMixin.plot_xy` uses the **pyplot.plot** function to produce linear scaler plots. There
are a number of useful plotter functions that will work like this

*   [pyplot.semilogx,pyplot.semilogy] These two plotting functions will produce log-linear plots, with semilogx making
    the x-axes the log one and semilogy the y-axis.
*   [pyplot.loglog] Liek the semi-log plots, this will produce a log-log plot.
*   [pyplot.errorbar] this particularly useful plotting function will draw error bars. The values for the error bars are
    passed as keyword arguments, *xerr* or *yerr*. In standard matplotlib, these can be numpy arrays or constants.
    :py:meth:`PlotMixin.plot_xy` extends this by intercepting these arguements and offering some short cuts::

         p.plot_xy(x,y,plotter=errorbar,yerr='dResistance',xerr=[5,'dTemp+'])

    This is equivalent to doing something like::

         p.plot_xy(x,y,plotter=errorbar,yerr=p.column('dResistance'),xerr=[p.column(5),p.column('dTemp+')])

    If you actually want to pass a constant to the *x/yerr* keywords you should use a float rather than an integer.

The X and Y axis label will be set from the column headers.


Plotting 3D Data
----------------

A number of the measurement rigs will produce data in the form of rows of $x,y,z$ values. Often it is desirable to plot
these on a surface plot or 3D plot. The :py:meth:`PlotMixin.plot_xyz` method can be used for this.

.. plot:: samples/3D_plot.py
   :include-source:

.. plot:: samples/colormap_plot.py
   :include-source:

By default the :py:meth:`PlotMixin.plot_xyz` will produce a 3D surface plot with the z-axis coded with a rainbow colour-map
(specifically, the matplotlib provided *matplotlib.cm.jet* colour-map. This can be overriden with the *cmap* keyword
parameter. If a simple 2D surface plot is required, then the *plotter* parameter should be set to a suitable function
such as **pyplot.pcolor**.

Like :py:meth:`PlotMixin.plot_xy`, a *figure* parameter can be used to control the figure being used and any additional
keywords are passed through to the plotting function. The axes labels are set from the corresponding column labels.

Another option is a contour plot based on ``(x,y,z)`` data points. This can be done with the :py:meth:`PlotMixin.contour_xyz`
method.

.. plot:: samples/contour_plot.py
   :include-source:

Both :py:meth:`PlotMixin.plot_xyz` and :py:meth:`PlotMixin.contour_xyz` make use of a call to :py:meth:`PlotMixin.griddata`
which is a utility method of the :py:class:`PlotMixin` -- essentially this is just a pass through method to the underlying
*scipy.interpolate.griddata** function. The shape of the grid is determined through a combination of the *xlim*, *ylim*
and *shape* arguments.::

    X,Y,Z=p.griddata(xcol,ycol,zcol,shape=(100,100))
    X,Y,Z=p.griddata(xcol,ycol,zcol,xlim=(-10,10,100),ylim=(-10,10,100))

If a *xlim* or *ylim* arguments are provided and are two tuples, then they set the maximum and minimum values of the relevant axis.
If they are three tuples, then the third argument is the number of points along that axis and overrides any setting in the *shape*
parameter. If the *xlim* or *ylim* parameters are not presents, then the maximum and minimum values of the relevant axis are used.
If no *shape* information is provided, the default is to make the shape a square of sidelength given by the square root of the
number of points.

 Alternatively, if your data is already in the form of a matrix, you can use the :py:meth:`PlotMixin.plot_matrix` method.

.. plot:: samples/matrix_plot.py
   :include-source:

The first example just uses all the default values, in which case the matrix is assumed to run from the 2nd column in the
file to the last and over all of the rows. The x values for each row are found from the contents of the first column, and
the y values for each column are found from the column headers interpreted as a floating pint number. The colourmap defaults
to the built in 'jet' theme. The x axis label is set to be the column header for the first column, the y axis label is set
either from the meta data item 'ylabel or to 'Y Data'. Likewise the z axis label is set from the corresponding metadata
item or defaults to 'Z Data;. In the second form these parameters are all set explicitly. The *xvals* parameter can be
either a column index (integer or sring) or a list, tuple or numpy array. The *yvals* parameter can be either a row number
(integer) or list,tuple or numpy array. Other parameters (including *plotter*, *figure* etc) work as for the
:py:meth:`PlotMixin.plot_xyz` method. The *rectang* parameter is used to select only part of the data array to use as the matrix.
It may be 2-tuple in which case it specifies just the origin as (row,column) or a 4-tuple in which case the third and forth
elements are the number of rows and columns to include. If *xvals* or *yvals* specify particular column or rows then the
origin of the matrix is moved to be one column further over and one row further down (ie the matrix is to the right and
below the columns and rows used to generate the x and y data values). The final example illustrates how to generate a
new 2D surface plot in a new window using default matrix setup.

Plotting Vector Fields
----------------------

For these purposes a vector field is a set of points $(x,y,z)$ at which a 3D vector $(u,v,w)$ is defined. Often vector
fields are visualised by using quiver plots, where a small arrow points in the direction of the vector and whose length
is proportional to the magnitude. This can also be suplemented by colour information - in one scheme a hue-saturation-luminence
space is used, where hue described a direction in the x-y plane, the luminence describes the vertical component and the
saturation, the relative magnitude. This is a common scheme in micro-magnetics, so is supported in the Stoner package.
Following the naming convention above, the :py:meth:`PlotMixin.plot_xyzuvw` method handles these plots.::

    p.plot_xyzuvw(xcol,ycol,zcol,ucol,vcol,wcol)
    p.plot_xyzuvw(xcol,ycol,zcol,ucol,vcol,wcol,colors="color_data")
    p.plot_xyzuvw(xcol,ycol,zcol,ucol,vcol,wcol,colors=np.random(len(p))
    p.plot_xyzuvw(xcol,ycol,zcol,ucol,vcol,wcol,mode='arrow')
    p.plot_xyzuvw(xcol,ycol,zcol,ucol,vcol,wcol,mode='arrow',colors=True,scale_factor=1.0)
    p.plot_xyzuvw(xcol,ycol,zcol,ucol,vcol,wcol,plotter=myplotfunc)

The :py:meth:`PlotMixin.plot_xyzuvw` method uses a default vector field plot function that is based on mayavi from
Enthought. The import is done when the plot is required to speed loading times for the :py:mod:`Stoner.plot` when
2D plotting only is required. If the mayavi package is not available, then matplotlib's 3D quiver plot is used as a fall back.

The first example above will result in a plot using flat arroiws coloured according to the vector magnitude. The second
examnple will instead color them using the specified column from the data. The third example demonstrates passing in
a separate list of colour data. In both of these cases the relative magnitude of the colors data is mapped to a colour map
(which can be given via a colormap keyword parameter).

The next example demonstrates changing the glyph used for each data point - in this case to a 3D arrow, but "cone" is also
a common choice. In the fifth example, the *colors* keyword is set to *True*. This signals the plotting function to colour
the individual pints with the H-S-L colour space as described above. The other keyword parameter, scale_factor is
passed through (as indeed are any other keyword parameters) to the underlying mayavi.mlab functions. The final example
demonstrates the use of the *plotter* keyword, analogous to the 2D and 3D examples to switch the actual plotting function.

As the mayavi.mlab quiver3d plotting function doesn't support a title, and axes labels by default, these are not used by
default in this function.

As usual, the default operation should still produce reasonable graphs.

.. plot:: samples/Vectorfield.py
   :include-source:



Very Quick Plotting
===================

For convenience, a :py:meth:`PlotMixin.plot` method is defined that will try to work out the necessary details. In combination
with the :py:attr:`Stoner.Core.DataFile.setas` attribute it allows very quick plots to be constructed.

.. plot:: samples/single_plot.py
   :include-source:


Getting More Control on the Figure
==================================

It is useful to be able to get access to the matplotlib figure that is used for each :py:class:`PlotMixin` instance. The
:py:attr:`PlotMixin.fig` attribute can do this, thus allowing plots from multiple :py:class:`PlotMixin` instances to be
combined in a single figure.::

    p1.plot_xy(0,1,'r-')
    p2.plot_xy(0,1,'bo',figure=p1.fig)

Likewise the :py:attr:`PlotMixin.axes` attribute returns the current axes object of the current figure in use by the :py:class:`PlotMixin`
instance.

There's a couple of extra methods that just pass through to the pyplot equivalents::

    p.draw()
    p.show()

Setting Axes Labels, Plot Titles and Legends
--------------------------------------------

:py:class:`PlotMixin` provides some useful attributes for setting specific aspects of the figures. Any
*get_* and *set_* method of :py:class:`pyplot.Axes` can be read or written as a :py:class:`PlotMixin` attribute.
Internally this is implemented by calling the corresponding method on the current axes of the :py:class:`PlotMixin`'s
figure. When setting the attribute, lists and tuples will be assumed to contain positional arguments and dictionaries
keyword arguments. If you want to pass a single tuple, list or dictionary, then you should wrap it in a single
element tuple.

Particualrly useful attributes include:

-   :py:attr:`PlotMixin.xlabel`, :py:attr:`PlotMixin.ylabel` will set the x and y axes labels
-   :py:attr:`PlotMixin.title` will set the plot title
-   :py:attr:`PlotMixin.xlim`, :py:attr:`PlotMixin.ylim` will accept a tuple to set the x- and y-axes limits.
-   :py:attr:`PlotMixin.labels` sets a list of strings that are the preferred name for each column. This is to
        allow the plotting routines to provide a default name for an axis label that can be different from the
        name of the column used for indexing purposes. If the label for a column is not set, then the column
        header is used instead. If a column header is changed, then the :py:attr:`PlotMixin.labels` attribute will
        be overwritten.

In addition, you can read any method of :py:class:`pyplot.Axes` as an attribute of :py:class:`PlotMixin`. This allows
one to call the methods directly on the PlotMixin instance without needing to extract a reference to the current
axes.::

    p.xlabel="My X Axis"
    p.set_xlabel("My X Axis")

are both equivalent, but the latter form allows access to the full keyword arguments of the x axis label control.

Plotting on Second Y (or X) Axes
================================

To plot a second curve using the same x axis, but a different y axis scale, the :py:meth:`PlotMixin.y2` method is
provided. This produces a second axes object with a common x-axis, but independent y-axis on the right of the plot.

.. plot:: samples/double_y_plot.py
   :include-source:

There is an equivalent :py:meth:`PlotMixin.x2` method to create a second set of axes with a common y scale but different x scales.

To work out which set of axes you are current working with the :py:attr:`PlotMixin.ax` attribute can be read or set.::

    p.plot_xy(0,1)
    p.y2()
    p.plot_xy(0,2)
    p.ax=0 # Set back to first x,y1 plot
    p.label="Plot 1"
    p.ax=1 # Set to the second
    p.yabel="Plot 2"


Plot Templates
--------------

.. currentmodule:: Stoner.plot.formats

Frequently one wishes to create many plots that have a similar set of formatting options - for example
in a thesis or to conform to a journal's specifications. The :py:mod:`Stoner.plot.formats` in conjunctions with
the :py:attr:`PlotMixin.template` attribute can help here.

A :py:attr:`PlotMixin.template` template is a set of instructions that controls the default settings for many
aspects of a matplotlib figure's style. In addition the template allows for pyplot formatting commands to be
executed during the process of plotting a figure.

.. plot:: samples/template2.py
   :include-source:

The template can either be set by passing a subclass of :py:class:`Stoner.plot.formats.DefaultPlotStyle` or
a particular instance of such a subclass. This latter option allows you to override the default plot attribute
settings defined by the template class with your own choice - or indeed, to add further style attributes. This
can be done by either calling the template and passing it arguments as keywords, or by settiong attributes directly on the template.
Because the matplotlib *rcParams* dictionary has keys that are not valid Python identifiers, periods in the rcParams keys
are translated as underscores and thus underscores become double underscores. When setting attributes on the template directly,
prefix the translated rcParam key with *template_*.

.. plot:: samples/template.py
   :include-source:

You can also copy the style template from one plot to the next.

    q=Data()
    q.template=p.template

The possible attributes that can be passed over to the template are essentially all the rc parameters for matplotlib
(see :py:func:`matplotlib.pyplot.rcParams`) except that periods '.' are replced with underscores '_' and single underscores
are replaced with double underscores.

Matplotlib makes use of stylesheets - essentially separate files of matplotlibrc entries. The template classes have a stylename
parameter that controls which stylesheet is used. This can be either one of the built in styles (see :py:attr:`matplotlib.pyplot.styles.available`)
or refer to a file on disc. The template will search for the file (named *<stylename>*.mplstyle) in.

    #. the same directory as the template class file is,
    #. a subdirectory called *stylelib* of the directory where the template class file is or,
    #. the stylelib subfolder of the Stoner package directory.

Where a template class is a subclass of the  :py:class:`DefaultPlotStyle`, the stylesheets are inherited in the same order as the
class heirarchy.

Changing the value of Lpy:attr:`DefaultPlotStyle.stylename` will force the tempalte to recalculate the stylesheet heirarchy, refidning
the paths to the stylesheets. You can also do any in-place modifications to the template stylesheet list (e.g. appending or extending it).

Further customisation is possible by creating a subclass of :py:class:`DefaultPlotStyle` and overriding the
:py:meth:`DefaultPlotStyle.customise` method and :py:meth:`DefaultPlotStyle.customise_axes` method.

The seaborn paclage offers many options for producing visually appealing plots with a higher level abstraction of the matplotlib api/
The :py:class:`SeabornPlotStyle` template class offers a quick interface to using this. It takes attributes :py:attr:`SeabornPlotStyle.stylename`,
:py:attr:`SeabornPlotStyle.context` and :py:attr:`SeabornPlotStyle.palette` to set the corresponding seaborn settings.


.. currentmodule:: Stoner.plot


Making Multi-plot Figures
-------------------------

Adding an Inset to a Figure
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :py:meth:`PlotMixin.inset` method can be used to creagte an inset in the current figure. Subsequent plots
will be to the inset until a new set of axes are chosen. The :py:class:`pyplot.Axes` instance of the inset is appended to the
:py:attr:`PlotMixin.axes` attribute.

.. plot:: samples/inset_plot.py
   :include-source:

The *loc* parameter specifies the location of the inset, the width and height the size (either as a percentage or
fixed units). There is an optional parent keyword that lets you specify an alternative parent set of axes for the
inset.

    *   *loc* = 1 top-right inset
    *   *loc* = 2 top left inset
    *   *loc* = 3 bottom left inset
    *   *loc* = 4 bottom right inset
    *   *loc* = 5 mid-right inset
    *   *loc* = 6 mid-left inset
    *   *loc* = 7 mid-right inset
    *   *loc* = 8 mid-bottom inset
    *   *loc* = 9 mid-top inset
    *   *loc* = 0 centre inset


Handling More than One Column of Y Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default if :py:meth:`PlotMixin.plot_xy` is given more than one column of y data, it will plot all
of the data on a single y-axis scale. If the y data to be plotted is not of a similar order of mangitude
this can result in a less than helpful plot.

.. plot:: samples/common_y_plot.py
   :include-source:

The :py:meth:`PlotMixin.plot_xy` method (and also the :py:meth:`PlotMixin.plot` method when doing 2D plots) will take
a keyword argument *multiple* that can offer a number of alternatives. If you have just two y columns, or the the
second and subsequent ones can fit on a common scale, then a double-y axis plot might be appropriate.

.. plot:: samples/multiple_y2_plot.py
   :include-source:

Alternatively, if you want the various y plots to form multiple panels with a common x-axis (a *ganged plot*) then
*multiple* can be set of *panels*.

.. plot:: samples/multiple_panels_plot.py
   :include-source:

Finally, you can also simply plot the y data as a grid of independent subplots.

.. plot:: samples/subplot_plot.py
   :include-source: