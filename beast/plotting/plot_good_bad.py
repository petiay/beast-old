#!/usr/bin/env python
"""
Show good/bad visualizations for BEAST results
"""

from __future__ import print_function

import matplotlib.pyplot as plt
from astropy.table import Table
from matplotlib.colors import LogNorm
from matplotlib import rc

# local imports
from beastplotlib import (fancify_colname, initialize_parser,
                          plot_generic, set_params)

def make_good_bad_plots(statsfile, xparam='logT', yparam='logL',
                        suffix='Exp', figsize=(15,10)):
    '''Makes a set of 4 diagnostic 2D histograms for BEAST output.

    Parameters
    ----------
    statsfile : str, file-like, list, pathlib.Path object
        File with BEAST output; see astropy.io.ascii.read docs for full 
        description of allowed input types.
    xparam: str, optional
        Parameter (column) name
        Default to 'logT'
    yparam: str, optional
        Parameter (column) name
        Default to 'logL'
    suffix : str, optional
        Column type ('Exp', 'Best', 'p16', 'p50', 'p84').
        Defaults to 'Exp'.
    figsize : tuple of ints, optional
        Size of figure to return in inches (width, height).
        Defaults to (10, 5.5).

    Returns
    -------
    fig : matplotlib figure object
        Figure with diagnostic plots
    '''
    stats = Table.read(statsfile)

    base_cnames = [xparam, yparam]
    cnames = ['{}_{}'.format(n, suffix) for n in base_cnames]
    plot_pairs = [[cnames[0], cnames[1]],
                  ['RA', 'DEC']]
    chicut = 100.0
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    ax = axes.ravel()
    for i, pair in enumerate(plot_pairs):
        j = 2*i
        plot_generic(stats, pair[0], pair[1], fig, ax[j],
                     thresh_col='chi2min', thresh=chicut, thresh_op='less',
                     plot_kwargs={'norm':LogNorm()})
        plot_generic(stats, pair[0], pair[1], fig, ax[j+1], 
                     thresh_col='chi2min', thresh=chicut, thresh_op='greater',
                     plot_kwargs={'norm':LogNorm()})
    fig.tight_layout()
    return fig

if __name__ == '__main__':
    parser = initialize_parser()
    parser.add_argument('filename', type=str,
                        help='Path to FITS file with output stats')
    suffixes = ['Exp', 'Best', 'p50']
    parser.add_argument('--suffix', action='store', default='Exp',
                        choices=suffixes,
                        help='Choose column type to plot. \
                        Must be one of: "{}"'.format('", "'.join(suffixes))
                        )
    params = ['logA','M_ini','Z','Av','Rv','f_A','logT','logL']
    parser.add_argument('--xparam', action='store', default='logT',
                        choices=params,
                        help='Choose column for xaxis \
                        Must be one of: "{}"'.format('", "'.join(params))
                        )
    parser.add_argument('--yparam', action='store', default='logL',
                        choices=params,
                        help='Choose column for yaxis \
                        Must be one of: "{}"'.format('", "'.join(params))
                        )
    args = parser.parse_args()
    if args.tex:
        plt.rc({'usetex':True})
    basename = args.filename.replace('.fits', '_diagnostics')

    set_params(lw=2, fontsize=16, usetex=False)
    fig = make_good_bad_plots(args.filename, suffix=args.suffix,
                              xparam=args.xparam, yparam=args.yparam)

    if args.savefig:
        fig.savefig('{}.{}'.format(basename, args.savefig))
    else:
        plt.show()