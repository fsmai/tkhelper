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
    # le 'toplevel widget' -> la fenetre de l'appli
    root = tk.Tk()
    # on habille la fenetre
    build_graphcalc(root)
    # on lance le tout
    root.mainloop()


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
    _refresh_plot = refresh_plot(plot, xexpr, yexpr)
    draw = ttk.Button(content, text="Draw", command=_refresh_plot)
    # le bouton pour nettoyer le dessin
    clear = ttk.Button(content, text="Clear", command=clear_plot(plot))

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
def refresh_plot(plot, xexpr, yexpr):
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
def clear_plot(plot):
    a = plot.figure.add_subplot(111)
    a.clear()
    plot.canvas.draw()  # imperatif sinon rien ne se passe


if __name__ == '__main__':
    main()
