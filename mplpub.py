from matplotlib.tight_layout import (get_renderer, get_tight_layout_figure,
                            get_subplotspec_list)
                                   
def horizontal_center(fig, pad=0.1):
    """
    import mplpub
    import matplotlib.pyplot as plt
    
    plt.ion()
    
    fig = plt.figure()
    plt.plot([1, 2, 3], [1, 4, 9])
    plt.ylabel('y axis')
    fig.set_size_inches(4, 1)
    mplpub.horizontal_center(fig)
    fig.savefig('plot.png')
    
    """
    adjust_kwargs = get_tight_layout_figure(fig, fig.axes,
        get_subplotspec_list(fig.axes), get_renderer(fig), pad=pad)
    
    adjust_kwargs['right'] = 1 - adjust_kwargs['left']
    
    fig.subplots_adjust(**adjust_kwargs)
    

def tight_layout(ax, pad=0.1):
    """Apply matplotlib's tight_layout but with plot contents centered.

    After setting the figure size, you can use this to automatically adjust the
    bounds of the plotting area (technically the bounds of the `Axes` object
    within the `Figure`) such that:

        1. figure whitespace is minimal without pushing axis labels, titles,
           etc. outside the figure
        2. plotted content is centered within the figure

    This is useful when setting the size of a figure to a document's full
    column width then adjusting so that the plot appears centered rather than
    the [y-axis label, tick labels, plot area] as a whole is centered.

    Parameters
    ----------
    ax : Axes
        The matplotlib axes object to center horizontally within the figure.
    pad : float
        Padding between the edge of the figure and the axis labels, as a
        multiple of font size.

    Examples
    --------
    Plot some data and save it as a PNG. The center of the x axis will be
    centered within the figure.

    >>> import mplpub
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    >>> ax.plot([1, 2, 3], [1, 4, 9])
    >>> ax.set_ylabel('y axis')
    >>> fig.set_size_inches(4, 1)
    >>> mplpub.tight_layout(ax)
    >>> fig.savefig('plot.png')
    """
    fig = ax.get_figure()
    fig.tight_layout(pad=pad)
    bbox = ax.get_position()
    bbox.x1 = 1 - bbox.x0
    ax.set_position(bbox)
