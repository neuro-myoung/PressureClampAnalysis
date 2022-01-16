import cufflinks as cf
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import plotly.express as px

def plot_sweeps(df):
    """
    This function will plot a dataframe of sweeps using plotly with hidden axis.

    Arguments: 
    df - a dataframe with columns tp, p, ti, i, and sweep

    Returns:
    fig - a plotly figure object
    """

    fig = make_subplots(rows=2, cols=1,  row_width=[0.6, 0.3])
    
    for name, sweep in df.groupby('sweep'):
        
        fig.add_trace(
            go.Scatter(mode='lines', name=name, x=sweep.tp, y=sweep.p, marker=dict(color='#800000'),
                hovertemplate='x: %{x}<br>' + 'y: %{y}<br>'),
            row=1, col=1)
            
        fig.add_trace(
            go.Scatter(mode='lines', name=name, x=sweep.ti, y=sweep.i, marker=dict(color='black'),
                hovertemplate='x: %{x}<br>' + 'y: %{y}<br>'),
            row=2, col=1)

    fig.update_layout(
        height=400,
        width=600,
        template='none',
        xaxis_showticklabels=False,
        xaxis_showgrid=False,
        yaxis_showticklabels=False,
        yaxis_showgrid=False,
        xaxis2_showticklabels=False,
        xaxis2_showgrid=False,
        yaxis2_showticklabels=False,
        yaxis2_showgrid=False,
        showlegend=False,
        hovermode='closest')

    fig.update_xaxes(matches='x')

    return(fig)

def plot_sweeps_stacked(df):
    """
    This function will plot a dataframe of sweeps using plotly with hidden axis.

    Arguments: 
    df - a dataframe with columns tp, p, ti, i, and sweep

    Returns:
    fig - a plotly figure object
    """
    nsweeps = len(np.unique(df.sweep))

    fig = make_subplots(rows=nsweeps + 1, cols=1,  row_width=[1/(nsweeps + 1) for i in range(nsweeps + 1)])
    
    for name, sweep in df.groupby('sweep'):
        
        fig.add_trace(
            go.Scatter(mode='lines', name=name, x=sweep.tp, y=sweep.p, marker=dict(color='#800000'),
                hovertemplate='x: %{x}<br>' + 'y: %{y}<br>'),
            row=1, col=1)
            
        fig.add_trace(
            go.Scatter(mode='lines', name=name, x=sweep.ti, y=sweep.i, marker=dict(color='black'),
                hovertemplate='x: %{x}<br>' + 'y: %{y}<br>'),
            row= int(np.unique(sweep.sweep)) + 1, col=1)

    fig.update_layout(
        height=800,
        width=800,
        template='none',
        showlegend=False,
        hovermode='closest')

    fig.update_xaxes(matches='x')

    return(fig)

def add_scalebars(df, fig, locs):
    """
    This function will add scalebars to a plot.

    Arguments: 
    df - a pandas dataframe with columns p, ti, tp, and i.
    fig - a plotly figure object..
    locs - a dictionary with the axis names as keys and scalebar limits as values.

    Returns:
    fig - a plotly figure object
    """

    try:
        if all(value == 0 for value in locs['p']) == False:
            pscale = dict(type="line", 
                        x0=locs['t'][0],
                        x1=locs['t'][0], 
                        y0=locs['p'][0], 
                        y1=locs['p'][1],
                        line=dict(color="black",
                                    width=2))

            fig.add_shape(pscale, row=1, col=1)

        if all(value == 0 for value in locs['i']) == False:
            iscale = dict(type="line", 
                        x0=locs['t'][0], 
                        x1=locs['t'][0], 
                        y0=locs['i'][0], 
                        y1=locs['i'][1],
                        line=dict(color="black",
                                    width=2))

            fig.add_shape(iscale, row=2, col=1)
            
        if all(value == 0 for value in locs['t']) == False:
            tscale = dict(type="line", 
                        x0=locs['t'][0], 
                        x1=locs['t'][1], 
                        y0=locs['i'][0], 
                        y1=locs['i'][0],
                        line=dict(color="black",
                                    width=2))
            
            fig.add_shape(tscale, row=2, col=1)
    except (KeyError, TypeError):
        print("Values must be entered as space separated integers.")   
    return(fig) 

def plot_summary(df, yval):
    """
    This function will plot a dataframe of summary statistics as a function of stimulus intensity.

    Arguments: 
    df - a pandas dataframe with columns pressure, param, and normalized_param.
    
    Returns:
    fig - a plotly figure object.
    """

    fig = go.Figure()
    
    fig.add_trace(
        go.Scatter(mode='markers',
                   name='p50', 
                   marker_color='#FF3300', 
                   marker_line_width = 1,
                   marker_size = 5,
                   x=df['pressure'], 
                   y=df[yval],
                   hovertemplate='x: %{x}<br>' + 'y: %{y}<br>'
                   )
    )

    fig.update_xaxes(title_text='Pressure (-mm Hg)')
    fig.update_yaxes(title_text='I/Imax')

    fig.update_layout(
        height=400,
        width=400,
        template='simple_white',
        showlegend=False,
        hovermode='closest')


    return(fig)

def fit_layer(df, fig, fit):
    """
    This function plots fit data over an existing plot.

    Arguments: 
    df - a pandas dataframe with columns pressure, param, and normalized_param.
    fig - a plotly figure object.
    fit - the fit parameters for a sigmoid fit.
    
    Returns:
    df - a plotly figure object.
    """

    xfine = np.linspace(min(df.pressure),max(df.pressure), 100)
    fig.add_trace(
    go.Scatter(mode='lines',
               name='fit', 
               marker_color='black', 
               marker_line_width = 1,
               x=xfine, 
               y=sigmoid_fit(xfine, *fit),
               hovertemplate='x: %{x}<br>' + 'y: %{y}<br>'
               )
    )

    return(fig)

def frequency_histogram(df, nbins, ngauss = 2):
    range_x = np.max(df.i) - np.min(df.i)
    #bin_width = 2*iqr(df.i)*len(df.i)**(-1/3) ## Freedman and Diaconis method
    #nbins = round(range_x/bin_width)
    bin_width = range_x/nbins
    [y, x]=np.histogram(df.i, nbins, density=True)
    test = ngauss_guesses(x, y, ngauss)

    fig = go.Figure([go.Bar(x=x[0:-1]+0.5*bin_width, y=y, marker_color = "black")])
    
    fig.update_xaxes(title_text='Current (pA)')
    fig.update_yaxes(title_text='Density')

    fig.update_layout(
        height=600,
        width=600,
        template='simple_white',
        showlegend=False,
        hovermode='closest')

    if ngauss == 3:
        popt, pcov = curve_fit(triple_gauss_fit, x[0:-1]+0.5*bin_width, y, p0=test)
        xfine = np.linspace(min(df.i), max(df.i), 500)

        fig.add_trace(
            go.Scatter(mode='lines',
                name='fit',
                marker_color='orange',
                marker_line_width = 1,
                fill = 'tozeroy',
                x=xfine,
                y=single_gauss_fit(xfine, *popt[[0,3,6]]),
                hovertemplate='x: %{x}<br>' + 'y: %{y}<br>'
            )
        )

        fig.add_trace(
            go.Scatter(mode='lines',
                name='fit',
                marker_color='purple',
                marker_line_width = 1,
                fill = 'tozeroy',
                x=xfine,
                y=single_gauss_fit(xfine, *popt[[1,4,7]]),
                hovertemplate='x: %{x}<br>' + 'y: %{y}<br>'
            )
        )

        fig.add_trace(
            go.Scatter(mode='lines',
                name='fit',
                marker_color='red',
                marker_line_width = 1,
                fill = 'tozeroy',
                x=xfine,
                y=single_gauss_fit(xfine, *popt[[2,5,8]]),
                hovertemplate='x: %{x}<br>' + 'y: %{y}<br>'
            )
        )

    else:
        popt, pcov = curve_fit(double_gauss_fit, x[0:-1]+0.5*bin_width, y, p0=test)
        xfine = np.linspace(min(df.i), max(df.i), 500)

        fig.add_trace(
            go.Scatter(mode='lines',
                name='fit',
                marker_color='orange',
                marker_line_width = 1,
                fill = 'tozeroy',
                x=xfine,
                y=single_gauss_fit(xfine, *popt[[0,2,4]]),
                hovertemplate='x: %{x}<br>' + 'y: %{y}<br>'
            )
        )

        fig.add_trace(
            go.Scatter(mode='lines',
                name='fit',
                marker_color='purple',
                marker_line_width = 1,
                fill = 'tozeroy',
                x=xfine,
                y=single_gauss_fit(xfine, *popt[[1,3,5]]),
                hovertemplate='x: %{x}<br>' + 'y: %{y}<br>'
            )
        )

    return(fig, popt, pcov)