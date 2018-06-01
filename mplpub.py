import matplotlib, warnings
from matplotlib.tight_layout import (get_renderer, get_tight_layout_figure,
                            get_subplotspec_list)
from matplotlib.font_manager import FontProperties
from matplotlib.transforms import TransformedBbox

rcParams = matplotlib.rcParams
golden_ratio = 1.61803398875

def wrap_suptitle(fig, suptitle_words=[], pad=1.08, **kwargs):
    """Add a wrapped suptitle so the width does not extend into the padding of
    the figure. 
    
    Parameters
    ----------
    fig : Figure
        The matplotlib figure object to be updated
    suptitle_text : list of strings
        A list of word strings that that should not be put on separate lines
    pad : float
        Padding between the edge of the figure and the axis labels, as a
        multiple of font size
    **kwargs : dict
        Additional keyword args to be passed to suptitle
        
    Returns
    -------
    suptitle : matplotlib.text.Text
        Passes return title from suptitle
    
    >>> import mplpub
    >>> import matplotlib.pyplot as plt
    >>> plt.ion()
    >>> fig = plt.figure()
    >>> for spec in ((1,2,1), (2,2,2), (2,2,4)):
    >>>     plt.subplot(*spec)
    >>>     plt.plot([1, 2, 3], [1, 4, 9])
    >>>     plt.ylabel('y axis')
    >>> fig.set_size_inches(4,4)
    >>> t = "This is a really long string that I'd rather have wrapped so that"\
    >>> " it doesn't go outside of the figure, but if it's long enough it will"\
    >>> " go off the top or bottom!"
    >>> fig.suptitle(t.split(" "))

    """
    w, h = fig.get_size_inches()
    max_width = 1 - 2 * pad * FontProperties(
            size=rcParams["font.size"]).get_size_in_points() / (144 * w)
    words_in_lines = [suptitle_words]
    iter_count = 0
    iter_max = len(suptitle_words)
    for iter_count in range(iter_max):
        this_line = words_in_lines[-1]
        words_in_this_line = len(this_line)
        for word_idx_iter in range(words_in_this_line):
            split_index = words_in_this_line-word_idx_iter
            line_text = " ".join(this_line[0:split_index])
            suptitle_line = fig.suptitle(line_text, **kwargs)
            suptitle_line_width = TransformedBbox(
                    suptitle_line.get_window_extent(get_renderer(fig)),
                    fig.transFigure.inverted()
                ).width
            if suptitle_line_width <= max_width:
                break
        next_line = this_line[split_index:]
        words_in_lines = words_in_lines[:-1] + [this_line[:split_index]]
        if len(next_line):
            words_in_lines += [next_line]
        else:
            break
    suptitle_text = "\n".join([" ".join(line) for line in words_in_lines])
    return fig.suptitle(suptitle_text, **kwargs)

def vertical_aspect(fig, aspect, ax_idx=0, pad=1.08,
                    nonoverlapping_extra_artists=[],
                    overlapping_extra_artists=[]):
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
        multiple of font size
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
    w, h = fig.get_size_inches()

    nrows = get_subplotspec_list(fig.axes)[ax_idx].get_geometry()[0]

    pad_inches = pad * FontProperties(
        size=rcParams["font.size"]).get_size_in_points() / 144

    non_overlapping_inches = {'top': 0, 'bottom': 0}
    hspace = fig.subplotpars.hspace
    for artist in nonoverlapping_extra_artists:
        artist_bbox = TransformedBbox(
            artist.get_window_extent(get_renderer(fig)),
            fig.transFigure.inverted()
        )
        if artist_bbox.ymax < 0.5:
            side = 'bottom'
        else:
            side = 'top'
        non_overlapping_inches[side] += artist_bbox.height*h + pad_inches

    for i in range(11):
        overlapping_maxy = 0
        overlapping_miny = 1
        for artist in overlapping_extra_artists:
            artist_bbox = TransformedBbox(
                artist.get_window_extent(get_renderer(fig)),
                fig.transFigure.inverted()
            )
            if artist_bbox.ymax > overlapping_maxy:
                overlapping_maxy = artist_bbox.ymax
            if artist_bbox.ymin < overlapping_miny:
                overlapping_miny = artist_bbox.ymin
                
        if overlapping_maxy > (1 - pad_inches/h):
            overlapping_top_adjust_inches = overlapping_maxy*h - (h - pad_inches) 
        else:
            overlapping_top_adjust_inches = 0
        if overlapping_miny < pad_inches/h:
            overlapping_bottom_adjust_inches = pad_inches - overlapping_miny*h
        else:
            overlapping_bottom_adjust_inches = 0

        bbox = ax.get_position()        
        current_aspect = ((bbox.x1 - bbox.x0)*w)/((bbox.y1 - bbox.y0)*h)
        aspect_diff = abs(current_aspect - aspect)*w * fig.get_dpi()
        if ((aspect_diff*3.14159<1) and
           (not overlapping_top_adjust_inches) and 
           (not overlapping_bottom_adjust_inches)):
            return i

        old_h = h

        adjust_kwargs = get_tight_layout_figure(fig, fig.axes,
            get_subplotspec_list(fig.axes), get_renderer(fig), pad=pad,
            rect = (0, (non_overlapping_inches['bottom'] +
                    overlapping_bottom_adjust_inches)/h, 1, 1-(non_overlapping_inches['top'] +
                 overlapping_top_adjust_inches)/h)
            )
        
        tight_top_inches = (1-adjust_kwargs['top'])*old_h
        tight_bottom_inches = adjust_kwargs['bottom']*old_h

        hspace = adjust_kwargs.get('hspace',0)
        h = ( bbox.width*w*(nrows + hspace*(nrows-1))/aspect +
                (adjust_kwargs['bottom'] + 1 - adjust_kwargs['top'])*old_h +
                overlapping_top_adjust_inches + 
                overlapping_bottom_adjust_inches +
                non_overlapping_inches['top'] +
                non_overlapping_inches['bottom'])

        fig.set_size_inches((w, h))

        fig.subplots_adjust(
            top=1-(tight_top_inches)/h,
            bottom=(tight_bottom_inches)/h,
            hspace=adjust_kwargs.get('hspace',None)
        )

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
        multiple of font size
        
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
    