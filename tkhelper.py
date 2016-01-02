""" helper module for tkinter

The module provides:

- the alias 'tk' and 'ttk' for the tkinter and ttk modules for python 2 and 3.

- the decorator 'command' to easily build factories of commands.

- the Plot class to help the integration of matplotlib with tkinter.


Note: forget pack() and use grid() to place the element in the window.

"""

__all__ = ['tk', 'ttk', 'command']

import functools

try:
    # Python 2
    import Tkinter as tk
    import ttk
except ImportError:
    # Python 3
    import tkinter as tk
    from tkinter import ttk

try:
    import matplotlib
    matplotlib.use("TkAgg")  # before importing matplotlib.backends
    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2TkAgg
    )
    import matplotlib.figure
except ImportError:
    matplotlib = None


def command(func=None, **kwargs):
    """ decorator to convert a function in command factory.

    command(func) -> wrapper(event=None)
    command(event=False)(func) -> wrapper(event=None)

    Exemples:

    >>> @command
    ... def action(arg1, arg2):
    ...     # do things
    ...     return
    ...
    >>> ttk.Button(frame, text='Ok', command=action(val1, val2))
    >>> my_widget.bind('<Return>', action(val1, val2))

    >>> @command(event=True)
    ... def action(event, arg1, arg2):
    ...     # do things
    ...     return
    ...
    >>> my_widget.bind('<Return>', action(val1, val2))

    """
    if func is None:
        return lambda f: command(f, **kwargs)
    event_arg = kwargs.pop('event', False)
    if kwargs:
        raise TypeError("%s() got an unexpected keyword argument %r"
                        % (func.__name__, kwargs.keys()[0]))

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if event_arg:
            def call(event=None):
                return func(event, *args, **kwargs)
        else:
            def call(event=None):
                return func(*args, **kwargs)
        return call
    return wrapper


class Plot(object):
    """ Plot(parent_frame)

    Create the canvas, toolbar and matplotlib figure to define a plot.

    The 3 attributes are:

        plot.figure -> matplotlib.figure.Figure

        plot.canvas -> FigureCanvasTkAgg (matplotlib)
                       plot.canvas.get_tk_widget() to have a tk widget

        plot.toolbar -> Frame
                        the frame containing the toolbar
                        usefull to place the toolbar

        plot.tbr_mpl -> NavigationToolbar2TkAgg (matplotlib)
                        the actual toolbar from matplotlib
                        use plot.toolbar unless you have a good reason.

    Note: Why 'toolbar' and 'tbr_mpl' ?

        NavigationToolbar2TkAgg is a tk widget that uses the pack() method
        to set its position.
        We should now prefer the grid() method. But grid() and pack()
        do not interact very well.
        A solution is to bring the widget alone in a frame.
        Then one can use grid() on the frame.

    """
    def __init__(self, frame):
        self.figure = matplotlib.figure.Figure()
        self.canvas = FigureCanvasTkAgg(self.figure, frame)
        self.toolbar = ttk.Frame(frame)
        self.tbr_mpl = NavigationToolbar2TkAgg(self.canvas, self.toolbar)


if matplotlib:
    __all__.append('Plot')
else:
    del Plot
