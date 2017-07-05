from matplotlib.tight_layout import (get_renderer, get_tight_layout_figure,
                            get_subplotspec_list)
import warnings
golden_ratio = 1/1.61803398875

def vertical_aspect(fig, aspect, ax_idx=0, pad=0.1):
    """
    import mplpub
    import matplotlib.pyplot as plt
    
    plt.ion()
    
    fig = plt.figure()
    plt.plot([1, 2, 3], [1, 4, 9])
    plt.ylabel('y axis')
    fig.set_size_inches(4, 1)
    mplpub.vertical_aspect(fig, mplpub.golden_ratio)
    fig.savefig('plot.png')
    
    """
    ax = fig.axes[ax_idx]
    new_h = 0
    
    for i in range(11):
        adjust_kwargs = get_tight_layout_figure(fig, fig.axes,
            get_subplotspec_list(fig.axes), get_renderer(fig), pad=pad)
        
        bbox = ax.get_position()
        
        w, h = fig.get_size_inches()
        
        new_h = ((bbox.x1 - bbox.x0)*w*aspect + 
            ((bbox.y0 + adjust_kwargs['top']) - 
             (bbox.y1 + adjust_kwargs['bottom']))*h)
        
        fig.set_size_inches((w, new_h))
        
        adjust_kwargs = get_tight_layout_figure(fig, fig.axes,
            get_subplotspec_list(fig.axes), get_renderer(fig), pad=pad)
        
        fig.subplots_adjust(top=adjust_kwargs['top'], 
            bottom=adjust_kwargs['bottom'],
            hspace=adjust_kwargs.get('hspace',None))
        
        if (new_h-h)==0:
            return i
    warnings.warn("vertical_aspect did not converge")

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
    for i in range(11):
        adjust_kwargs = get_tight_layout_figure(fig, fig.axes,
            get_subplotspec_list(fig.axes), get_renderer(fig), pad=pad)
        
        
        if ((adjust_kwargs['left'] - fig.subplotpars.left)==0 and
            (adjust_kwargs['right'] - fig.subplotpars.right)==0):
            return i
        
        fig.subplots_adjust(left=adjust_kwargs['left'], 
                            right=1-adjust_kwargs['left'],
                            wspace=adjust_kwargs.get('wspace',None))
    warnings.warn("horizontal_center did not converge")
    

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
