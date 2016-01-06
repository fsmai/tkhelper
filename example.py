""" un exemple de gui avec tkinter

A noter:
1) on peut structurer le code :
    pas un script avec tout au meme niveau
    pas de variables globales
2) utiliser grid() plutot que pack()
"""


import numpy
from tkhelper import tk, ttk, Plot, command


def main():
    root = tk.Tk()
    root.title('example')
    fill_notebook(
        root,
        ('graphcal', build_graphcalc),
        ('sinus', build_sin)
    )
    root.mainloop()


def fill_notebook(root, *builders):
    notebook = ttk.Notebook(root)
    for name, build in builders:
        f = ttk.Frame(notebook)
        notebook.add(f, text=name)
        build(f)
    notebook.grid(row=0, column=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)


###########################################################
###########################################################
def build_graphcalc(root):
    ## Pour recuperer les valeurs des champs
    xexpr = tk.StringVar()
    yexpr = tk.StringVar()
    # default value at start
    xexpr.set('linspace(0, 1)')
    yexpr.set('sin(2*pi*x)')

    ## declaration de tous les objets de la fenetre
    # le cadre qui va tout contenir
    content = ttk.Frame(root)
    # les champs a remplir avec leur labels
    xlbl = ttk.Label(content, text="x = ")
    ylbl = ttk.Label(content, text="y = ")
    xentry = ttk.Entry(content, textvariable=xexpr)
    yentry = ttk.Entry(content, textvariable=yexpr)
    # notre plot
    plot = Plot(content)
    # le bouton pour faire le dessin
    _refresh_plot = refresh_graphcalc(plot, xexpr, yexpr)
    draw = ttk.Button(content, text="Draw", command=_refresh_plot)
    # le bouton pour nettoyer le dessin
    clear = ttk.Button(content, text="Clear", command=clear_graphcalc(plot))

    ## mise en place des objets dans la fenetre
    # on place tout sur un quadrillage de la fenetre
    # sticky pour controler ou se placer dans chaque case
    content.grid(column=0, row=0, sticky='nsew')
    clear.grid(column=0, row=0, sticky='se')
    draw.grid(column=1, row=0, sticky='sw')
    plot.toolbar.grid(column=2, row=0, sticky='sw')
    plot_canvas_widget = plot.canvas.get_tk_widget()
    plot_canvas_widget.grid(column=2, row=1, rowspan=2, sticky='nsew')
    xlbl.grid(column=0, row=1, sticky='e')
    xentry.grid(column=1, row=1, sticky='we')
    ylbl.grid(column=0, row=2, sticky='e')
    yentry.grid(column=1, row=2, sticky='we')
    # on place des poids sur les cases pour indiquer comment les deformer
    # quand la fenetre change de taille
    # par defaut le poid est 0 (case fixe)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    content.columnconfigure(2, weight=1)
    content.rowconfigure(1, weight=1)
    content.rowconfigure(2, weight=1)


@command
def refresh_graphcalc(plot, xexpr, yexpr):
    ## traite les infos
    globals_ = dict(vars(numpy))
    exec('__x = %s' % xexpr.get(), globals_)
    exec('__y = lambda x: %s' % yexpr.get(), globals_)
    x = numpy.array(globals_['__x'])
    fy = globals_['__y']
    y = fy(x)

    ## maj du plot
    a = plot.figure.add_subplot(111)
    a.plot(x, y, label=yexpr.get())
    a.legend(loc='best')
    plot.canvas.draw()  # imperatif sinon rien ne se passe


@command
def clear_graphcalc(plot):
    a = plot.figure.add_subplot(111)
    a.clear()
    plot.canvas.draw()  # imperatif sinon rien ne se passe


###########################################################
###########################################################
def build_sin(root):

    freq_max = tk.StringVar()
    freq_min = tk.StringVar()

    freq_min.set('1')
    freq_max.set('3')

    x = numpy.linspace(0, 1, 100)

    content = ttk.Frame(root)

    plot = Plot(content)

    frequency = ttk.Frame(content)
    freq_max_entry = ttk.Entry(frequency, width=6, textvariable=freq_max)
    freq_min_entry = ttk.Entry(frequency, width=6, textvariable=freq_min)
    freq_scale = ttk.Scale(frequency, from_=0., to=1.)
    command = refresh_sin(freq_scale, freq_min, freq_max, plot, x)
    command()  # first draw
    freq_scale.configure(command=command)

    validate_float(freq_min_entry)
    validate_float(freq_max_entry)

    content.grid(column=0, row=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    #
    frequency.grid(column=0, row=1, sticky='new')
    plot.canvas.get_tk_widget().grid(column=0, row=0, sticky='nsew')
    content.columnconfigure(0, weight=1)
    content.rowconfigure(0, weight=1)
    #
    freq_min_entry.grid(row=0, column=0, sticky='e')
    freq_scale.grid(row=0, column=1, sticky='ew')
    freq_max_entry.grid(row=0, column=2, sticky='w')
    frequency.columnconfigure(1, weight=1)


@command(event=True)
def refresh_sin(event, scale, freq_min, freq_max, plot, x):

    try:
        fmin = float(freq_min.get())
        fmax = float(freq_max.get())
    except ValueError:
        return

    scale = float(scale.get())

    freq = fmin + scale * (fmax - fmin)

    a = plot.figure.add_subplot(111)
    a.clear()
    y = numpy.sin(freq * 2 * numpy.pi * x)
    a.plot(x, y, label='freq = %.3g' % freq)
    a.legend(loc='upper right')
    plot.canvas.draw()


def validate_float(entry):
    def on_validate(text):
        try:
            float(text)
        except ValueError:
            color = 'red'
        else:
            color = 'black'
        entry.configure(foreground=color)
        return True

    vcmd = (entry.register(on_validate), '%P')
    entry.configure(validate='key', validatecommand=vcmd)


###########################################################
###########################################################
if __name__ == '__main__':
    main()

    ## building only one app is done by:
    # root = tk.Tk()
    # build_graphcalc(root)
    # root.mainloop()
