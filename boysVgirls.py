#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 20:09:29 2020

@author: Serhii Bahdasariants
"""

import pandas as pd
from scipy.stats import ttest_ind

pointpos_male = -1
pointpos_female = +1

data = pd.read_csv('/Users/labmate/Python_projects/EXP682_stats/exph682_data.csv')

# H01: There is no gender bias in accuracy of throwing a ball with dominant hand. 

nMaleDom   = data.nRate[(data.sGender == 'Male') & (data.bDominant == 1)]   # male dominant hand
nFemaleDom = data.nRate[(data.sGender == 'Female') & (data.bDominant == 1)] # female dominant hand

[t_dom, p_dom] = ttest_ind(nMaleDom, nFemaleDom)

# H02: There is no gender bias in accuracy of throwing a ball with non-dominant hand. 

nMaleNondom   = data.nRate[(data.sGender == 'Male') & (data.bDominant == 0)]   # male non-dominant hand
nFemaleNondom = data.nRate[(data.sGender == 'Female') & (data.bDominant == 0)] # female non-dominant hand

[t_nondom, p_nondom] = ttest_ind(nMaleNondom, nFemaleNondom)

# H03: There is no gender bias in accuracy of overhand ball throwing. 

nMaleOver   = data.nRate[(data.sGender == 'Male') & (data.bOverhand == 1)]   # male overhand
nFemaleOver = data.nRate[(data.sGender == 'Female') & (data.bOverhand == 1)] # female overhand

[t_over, p_over] = ttest_ind(nMaleOver, nFemaleOver)


# H04: There is no gender bias in accuracy of underhand ball throwing. 

nMaleUnder  = data.nRate[(data.sGender == 'Male') & (data.bOverhand == 0)]   # male under
nFemaleUnder = data.nRate[(data.sGender == 'Female') & (data.bOverhand == 0)] # female under

[t_under, p_under] = ttest_ind(nMaleUnder, nFemaleUnder)

from statsmodels.stats.multitest import multipletests
[reject, p_corrected, alphacSidak, alphacBonf] = multipletests([p_dom,p_nondom,p_over,p_under], alpha=0.05, method='bonferroni')

#PLOT THE DATA

# DOMINANT HAND-------------------------------------------------------------
import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(go.Violin(y = data.nRate[(data['bDominant'] == 1)&(data.sGender == 'Male')],
                        x = data.bDominant[(data['bDominant'] == 1)&(data.sGender == 'Male')],
                        legendgroup = 'Dominant hand',name = 'Male',
                        side = 'negative', line_color = 'black',pointpos=pointpos_male))


fig.add_trace(go.Violin(y = data.nRate[(data['bDominant'] == 1)&(data.sGender == 'Female')],
                        x = data.bDominant[(data['bDominant'] == 1)&(data.sGender == 'Female')],
                        legendgroup = 'Dominant hand',name = 'Female',
                        side = 'positive', line_color = 'orangered',pointpos=pointpos_female))

fig.update_traces(meanline_visible=True)
fig.update_layout(violingap=0)

fig.update_traces(meanline_visible=True,
                  points='all', # show all points
                  jitter=0.5,  # add some jitter on points for better visibility
                  scalemode='count') #scale violin plot area with total count

fig.update_layout(
    autosize=False,
    width=500,
    height=600,
    )
# NON-DOMINANT HAND--------------------------------------------------------

fig.add_trace(go.Violin(y = data.nRate[(data['bDominant'] == 0)&(data.sGender == 'Male')],
                        x = data.bDominant[(data['bDominant'] == 0)&(data.sGender == 'Male')],
                        legendgroup = 'Nondominant hand',name = 'Male',
                        side = 'negative', line_color = 'black',pointpos=pointpos_male))


fig.add_trace(go.Violin(y = data.nRate[(data['bDominant'] == 0)&(data.sGender == 'Female')],
                        x = data.bDominant[(data['bDominant'] == 0)&(data.sGender == 'Female')],
                        legendgroup = 'Non-dominant hand',name = 'Female',
                        side = 'positive', line_color = 'orangered',pointpos=pointpos_female))

fig.update_traces(meanline_visible=True)
fig.update_layout(violingap=0)

fig.update_traces(meanline_visible=True,
                  points='all', # show all points
                  jitter=0.5,  # add some jitter on points for better visibility
                  scalemode='count') #scale violin plot area with total count

fig.update_layout(
    autosize=False,
    width=600,
    height=600,
    )

fig.update_layout(
    title="",
    xaxis_title="",
    yaxis_title="Hit Rate",
    font=dict(
        family="Helvetica Neue, monospace",
        size=12,
        color="#7f7f7f"
    )
)

fig.show()

# OVERHAND-------------------------------------------------------------
fig = go.Figure()

fig.add_trace(go.Violin(y = data.nRate[(data['bOverhand'] == 1)&(data.sGender == 'Male')],
                        x = data.bOverhand[(data['bOverhand'] == 1)&(data.sGender == 'Male')],
                        legendgroup = 'Overhand',name = 'Male',
                        side = 'negative', line_color = 'black',pointpos=pointpos_male))


fig.add_trace(go.Violin(y = data.nRate[(data['bOverhand'] == 1)&(data.sGender == 'Female')],
                        x = data.bOverhand[(data['bOverhand'] == 1)&(data.sGender == 'Female')],
                        legendgroup = 'Overhand',name = 'Female',
                        side = 'positive', line_color = 'orangered',pointpos=pointpos_female))

fig.update_traces(meanline_visible=True)
fig.update_layout(violingap=0)

fig.update_traces(meanline_visible=True,
                  points='all', # show all points
                  jitter=0.5,  # add some jitter on points for better visibility
                  scalemode='count') #scale violin plot area with total count

fig.update_layout(
    autosize=False,
    width=500,
    height=600,
    )
# UNDERHAND--------------------------------------------------------

fig.add_trace(go.Violin(y = data.nRate[(data['bOverhand'] == 0)&(data.sGender == 'Male')],
                        x = data.bOverhand[(data['bOverhand'] == 0)&(data.sGender == 'Male')],
                        legendgroup = 'Underhand',name = 'Male',
                        side = 'negative', line_color = 'black',pointpos=pointpos_male))


fig.add_trace(go.Violin(y = data.nRate[(data['bOverhand'] == 0)&(data.sGender == 'Female')],
                        x = data.bOverhand[(data['bOverhand'] == 0)&(data.sGender == 'Female')],
                        legendgroup = 'Underhand',name = 'Female',
                        side = 'positive', line_color = 'orangered',pointpos=pointpos_female))

fig.update_traces(meanline_visible=True)
fig.update_layout(violingap=0)

fig.update_traces(meanline_visible=True,
                  points='all', # show all points
                  jitter=0.5,  # add some jitter on points for better visibility
                  scalemode='count') #scale violin plot area with total count

fig.update_layout(
    autosize=False,
    width=600,
    height=600,
    )

fig.update_layout(
    title="",
    xaxis_title="",
    yaxis_title="Hit Rate",
    font=dict(
        family="Helvetica Neue, monospace",
        size=12,
        color="#7f7f7f"
    )
)

fig.show()