import matplotlib, warnings
from matplotlib.tight_layout import (get_renderer, get_tight_layout_figure,
                            get_subplotspec_list)

from matplotlib.font_manager import FontProperties
rcParams = matplotlib.rcParams
golden_ratio = 1.61803398875

from matplotlib.transforms import TransformedBbox

def vertical_aspect(fig, aspect, ax_idx=0, pad=1.08, suptitle_text_idx=0):
    """Adjust figure height and vertical spacing so a sub-plot plotting area has
    a specified aspect ratio and the overall figure has top/bottom margins from
    tight_layout.

    Parameters
    ----------
    fig : Figure
        The matplotlib figure object to be updated
    aspect : float
        The aspect ratio (W:H) desired for the subplot of ax_idx
    ax_idx : int
        The index (of fig.axes) for the axes to have the desired aspect ratio
    pad : float
        Padding between the edge of the figure and the axis labels, as a
        multiple of font size.
    suptitle_text_idx : int
        The index (of fig.texts) of the fig.suptitle to try to account for
    
    Returns
    -------
    i : int or float
        The number of iterations to converge (be within one pixel by DPI) of the
        desired aspect ratio or if it does not converge, the current aspect 
        ratio of the fig.axes[ax_idx]
    
    Examples
    --------
    Plot some data and save it as a PNG. The height
    
    >>> import mplpub
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.plot([1, 2, 3], [1, 4, 9])
    >>> plt.ylabel('y axis')
    >>> fig.set_size_inches(4, 1)
    >>> mplpub.vertical_aspect(fig, mplpub.golden_ratio)
    >>> fig.savefig('plot.png')
    
    Plays well with subplots
    
    >>> import mplpub
    >>> import matplotlib.pyplot as plt
    >>> plt.ion()
    >>> fig = plt.figure()
    >>> for spec in ((1,2,1), (2,2,2), (2,2,4)):
    >>>     plt.subplot(*spec)
    >>>     plt.plot([1, 2, 3], [1, 4, 9])
    >>>     plt.ylabel('y axis')
    >>> fig.set_size_inches(8, 8)
    >>> fig.suptitle("super title")
    >>> print("center iter",mplpub.horizontal_center(fig))
    
    The aspect ratio of any subplot can be set
    
    >>> print("vert iter",mplpub.vertical_aspect(fig, 1, 1))
    >>> print("vert iter",mplpub.vertical_aspect(fig, 0, 0.5))
    
    """
    ax = fig.axes[ax_idx]
    new_h = 0
    
    nrows = get_subplotspec_list(fig.axes)[ax_idx].get_geometry()[0]
    
    suptitle = None
    try:
        suptitle = fig.texts[suptitle_text_idx]
    except:
        pass
    
    suptitle_height = 0
    suptitle_pad = 0
    
    for i in range(11):
        adjust_kwargs = get_tight_layout_figure(fig, fig.axes,
            get_subplotspec_list(fig.axes), get_renderer(fig), pad=pad)
            
        w, h = fig.get_size_inches()

        if suptitle is not None:
            suptitle_height = TransformedBbox(suptitle.get_window_extent(get_renderer(fig)),fig.transFigure.inverted()).height
            suptitle_pad = pad * FontProperties(
                   size=rcParams["font.size"]).get_size_in_points() / 144
            
        fig.subplots_adjust(top=adjust_kwargs['top']-suptitle_height-suptitle_pad/h, 
            bottom=adjust_kwargs['bottom'],
            hspace=adjust_kwargs.get('hspace',None))
            
        bbox = ax.get_position()
        
        current_aspect = ((bbox.x1 - bbox.x0)*w)/((bbox.y1 - bbox.y0)*h)
        if abs(current_aspect - aspect)*w * fig.get_dpi()*3.14159 < 1:
            return i
        
        hspace = adjust_kwargs.get('hspace',0)
        new_h = ( bbox.width*w*(nrows + hspace*(nrows-1) + suptitle_pad)/aspect
                + (adjust_kwargs['bottom'] + 1 - adjust_kwargs['top'] + suptitle_height)*h)
        
        fig.set_size_inches((w, new_h))

    warnings.warn("vertical_aspect did not converge")
    return current_aspect

def horizontal_center(fig, pad=1.08):
    """Apply matplotlib's tight_layout to the left margin while keeping the plot
    contents centered.

    This is useful when setting the size of a figure to a document's full
    column width then adjusting so that the plot appears centered rather than
    the [y-axis label, tick labels, plot area] as a whole is centered.

    Parameters
    ----------
    fig : Figure
        The matplotlib figure object, the content of which will be centered
    pad : float
        Padding between the edge of the figure and the axis labels, as a
        multiple of font size.
        
    Returns
    -------
    i : int or None
        The number of iterations to converge (the computed margins don't change
        between iterations) or None if it does not converge.
        
    Examples
    --------
    Plot some data and save it as a PNG. The center of the x axis will be
    centered within the figure.
    
    >>> import mplpub
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.plot([1, 2, 3], [1, 4, 9])
    >>> plt.ylabel('y axis')
    >>> fig.set_size_inches(4, 1)
    >>> mplpub.horizontal_center(fig)
    >>> fig.savefig('plot.png')
    """
    for i in range(11):
        adjust_kwargs = get_tight_layout_figure(fig, fig.axes,
            get_subplotspec_list(fig.axes), get_renderer(fig), pad=pad)
        
        
        if ((adjust_kwargs['left'] - fig.subplotpars.left)==0 and
            (adjust_kwargs['left'] + fig.subplotpars.right)==1):
            return i
        
        fig.subplots_adjust(left=adjust_kwargs['left'], 
                            right=1-adjust_kwargs['left'],
                            wspace=adjust_kwargs.get('wspace',None))
    warnings.warn("horizontal_center did not converge")
    