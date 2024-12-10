from matplotlib.transforms import Bbox
import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation
import textwrap
from matplotlib.patches import Rectangle
from settings import OUTPUT_DATA_DIR
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Set default font for the entire plot
plt.rcParams['font.family'] = 'DejaVu Sans'

def plot_absolute_bar_plot(data_combined, years, custom_cmap, plot_title, continent):
    print("plot_absolute_bar_plot")

    figsize = (8, 5)
    fig, axs = plt.subplots(figsize=figsize)

    # Set the background color of the figure to white
    fig.patch.set_facecolor('white')

    # Define the fixed levels for color distribution
    levels = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]    
    
    norm_pm = mcolors.BoundaryNorm(boundaries=levels, ncolors=custom_cmap.N)
    colors_pm = custom_cmap(norm_pm(data_combined))

    # Bars representing the absolute values
    bars_pm = axs.bar(years, data_combined, color=colors_pm, edgecolor='none', width=1)
    axs.set_xlim(years.min(), years.max()+0.5) # KP_Change
    print(" years.max()", years.max())

    # Setting the colorbar
    sm_pm = plt.cm.ScalarMappable(cmap=custom_cmap, norm=norm_pm)
    sm_pm.set_array([])  # required for matplotlib 3.1 and later versions

    # Remove top x-axis and right y-axis
    axs.spines['top'].set_visible(False)
    axs.spines['right'].set_visible(False)
    axs.spines['bottom'].set_visible(False)
    axs.spines['left'].set_visible(False)

    # Add the title text to the upper-left corner with larger font
    axs.text(0.05, 1.08, plot_title, ha='left', va='bottom', fontsize=14, fontweight='bold', transform=axs.transAxes)
    axs.text(0.05, 1.02, 'Air pollution (PM2.5) concentrations from 1850 to 2022 (µg/m\u00B3)', ha='left', va='center', fontsize=12, fontweight='normal',
             transform=axs.transAxes)

    # Set y-axis limits to ensure bars are representative of values
    axs.set_ylim(0, 120.0)  # Force y-axis to start at zero
    
    # Set color of the tick labels on the plot
    axs.tick_params(axis='both', colors='black')

    # Add a solid line at zero position of y-axis
    axs.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

    # Add line for guideline
    axs.axhline(y=5, color='dimgrey', linestyle='--', linewidth=2.0)

    axs.axhline(y=50, color='dimgrey', linestyle='--', linewidth=2.0)

    # Add text "WHO Guideline" above the horizontal line at y=5 
    limit_text = axs.text(years.min() + 10.0, 7.0, "WHO Guideline",
                          ha='left', va='bottom', fontsize=12, fontweight='normal', 
                          color='black', bbox=dict(facecolor='white', alpha=0.8, 
                          edgecolor='none'))

    # Add text "WHO Guideline" above the horizontal line at y=5 
    limit_text = axs.text(years.min() + 10.0, 52, "Very Poor Air Quality",
                          ha='left', va='bottom', fontsize=12, fontweight='normal', 
                          color='black', bbox=dict(facecolor='white', alpha=0.8, 
                          edgecolor='none'))
    
    # Add the label at the bottom left
    axs.text(0.05, 0.945, 'airqualitystripes.info', ha='left', va='center', fontsize=10, color='black',
             transform=axs.transAxes, bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))
    
    # Save the plot
    plt.savefig(OUTPUT_DATA_DIR + plot_title+'_'+continent+'_absolute_bar_plot.png', dpi=400, bbox_inches='tight', pad_inches=0.05)  # Adjust DPI
    plt.show()
    plt.close()




def plot_aq_stripes_withline(data_combined, years, custom_cmap, plot_title, continent):
    print("plot_aq_stripes_withline")

    # Define the color for labels and borders
    label_color = 'black'

    figsize = (8, 5)
    fig, ax1 = plt.subplots(figsize=figsize)

    fig.patch.set_facecolor('white')

    # Define the fixed levels for color distribution
    levels = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]    

    norm_pm = mcolors.BoundaryNorm(boundaries=levels, ncolors=custom_cmap.N)
    colors_pm = custom_cmap(norm_pm(data_combined))

    bars_pm_stripes = ax1.bar(years, 1, color=colors_pm, edgecolor='none', width=1)

    # Create a second y-axis for the line plot
    ax2 = ax1.twinx()
    ax2.plot(years, data_combined, color='white', linewidth=4.0)

    # Configure the primary y-axis for the bars
    ax1.set_ylim(0, 1)
    ax1.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)  # Suppress ticks and labels
    ax1.yaxis.label.set_color(label_color)    

    # Configure the secondary y-axis for the line plot
    ax2.set_ylim(0, 120.0)  # Force y-axis to start at zero    
    ax2.tick_params(axis='y', which='both', left=True, right=False, labelleft=True, labelright=False, colors=label_color)  # Display ticks on the left
    ax2.yaxis.label.set_color(label_color)
    
    # Set the limits for the x-axis
    ax1.set_xlim(years.min(), years.max())
    
    sm_pm_stripes = plt.cm.ScalarMappable(cmap=custom_cmap, norm=norm_pm)
    sm_pm_stripes.set_array([])

    cbar_pm_stripes = plt.colorbar(sm_pm_stripes, orientation='vertical', pad=0.02, ax=ax1, aspect=10)
    
    cbar_pm_stripes.set_label('Annual Mean PM2.5 Concentration (µg/m\u00B3)', fontsize=11, \
                              labelpad=20, rotation=270, color=label_color)
    cbar_pm_stripes.outline.set_edgecolor(label_color)

    cbar_pm_stripes.ax.yaxis.set_tick_params(labelsize=11, pad=5, colors=label_color)

    # Force the color bar to label every section
    cbar_pm_stripes.set_ticks(levels)
    cbar_pm_stripes.set_ticklabels(levels)

    # Force the color bar to label every section except the highest
    cbar_pm_stripes.set_ticks(levels)
    tick_labels = [str(level) if level != max(levels) else '' for level in levels]
    cbar_pm_stripes.set_ticklabels(tick_labels)

    # Remove the tick marker from the top
    cbar_ax = cbar_pm_stripes.ax
    cbar_ax.yaxis.set_ticks_position('right')  # Ensure ticks are only on the left
    cbar_ax.yaxis.set_tick_params(width=0)  # Remove the tick markers
    
    # Add horizontal lines (black markers) at specific levels
    cbar_ax = cbar_pm_stripes.ax
    levels_to_mark = [5, 15, 30, 50, 70]  # Example levels where lines should be drawn
    colorbar_height = cbar_ax.get_position().bounds[3]  # Get colorbar height
    for level in levels_to_mark:
        # Draw a white line slightly thicker than the grey line
        cbar_ax.axhline(y=level, color='white', linestyle='solid', linewidth=2, xmin=0, xmax=2)
        # Draw the grey line on top
##        cbar_ax.axhline(y=level, color='grey', linestyle='-', linewidth=2, xmin=0, xmax=1)

    # Update the figure canvas
    fig.canvas.draw()

    ax1.spines['bottom'].set_color(label_color)
    ax1.spines['top'].set_color(label_color)
    ax1.spines['left'].set_color(label_color)
    ax1.spines['right'].set_color(label_color)

#    ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True, colors=label_color)
    ax1.tick_params(axis='y', colors=label_color)

    ax2.spines['bottom'].set_color(label_color)
    ax2.spines['top'].set_color(label_color)
    ax2.spines['left'].set_color(label_color)
    ax2.spines['right'].set_color(label_color)

    ax1.text(0.03, 0.89, plot_title, ha='left', va='bottom', fontsize=20, fontweight='normal', transform=ax1.transAxes,
             color='black', bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))

    ax1.text(0.03, 0.81, 'Air pollution (PM2.5) concentrations from 1850 to 2022', ha='left', va='bottom', fontsize=10, fontweight='normal', transform=ax1.transAxes, color='black', bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))    
    

    # Add the label at the bottom left
    ax1.text(0.03, 0.75, 'airqualitystripes.info', ha='left', va='center', fontsize=8, color='black',
             transform=ax1.transAxes, bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))
    
    
    plt.savefig(OUTPUT_DATA_DIR + plot_title+'_'+continent+'_aq_stripes_withline.png', dpi=400, bbox_inches='tight', pad_inches=0.05)
    plt.show()
    plt.close()

def plot_aq_stripes_withline_withindicativecolourbar(data_combined, years, custom_cmap, plot_title, continent, uncertainty_classification, data_ratio):
    print("plot_aq_stripes_withline_withindicativecolourbar")

    # Define the color for labels and borders
    label_color = 'black'

    figsize = (8, 5)
    fig, ax1 = plt.subplots(figsize=figsize)

    fig.patch.set_facecolor('white')

    # Define the fixed levels for color distribution
    # levels = [0, 5, 10, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105]
    # levels = [0, 5, 10, 15, 20, 25, 35, 45, 55, 65, 75, 85, 95, 105]    
    # levels = [0, 5, 10, 15, 20, 25, 35, 45, 55, 65, 80, 95]    
    levels = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]    

    norm_pm = mcolors.BoundaryNorm(boundaries=levels, ncolors=custom_cmap.N)
    colors_pm = custom_cmap(norm_pm(data_combined))

    bars_pm_stripes = ax1.bar(years, 1, color=colors_pm, edgecolor='none', width=1)

    # Create a second y-axis for the line plot
    ax2 = ax1.twinx()
    ax2.plot(years, data_combined, color='white', linewidth=4.0)

    # Configure the primary y-axis for the bars
    ax1.set_ylim(0, 1)
    ax1.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)  # Suppress ticks and labels
    ax1.yaxis.label.set_color(label_color)    

    # Configure the secondary y-axis for the line plot
    ax2.set_ylim(0, 120.0)  # Force y-axis to start at zero    
    ax2.tick_params(axis='y', which='both', left=True, right=False, labelleft=True, labelright=False, colors="white")  # Display ticks on the left
    ax2.yaxis.label.set_color(label_color)
    
    # Set the limits for the x-axis
    ax1.set_xlim(years.min(), years.max())
    sm_pm_stripes2 = plt.cm.ScalarMappable(cmap=custom_cmap, norm=norm_pm)
    sm_pm_stripes2.set_array([])
    
    # Custom labels and ticks
    ticks =  [0,   2.5,       5,   10,       20,     40,   50,    61,      65,  88, 83, 85, 90, 80, 70, 60, 30, 15,100]
    labels = ["", "Very Good","","Fair", "Moderate","Poor","", "Very Poor","","Extremely", "Poor","","","","","", "","",""]

    cbar_pm_stripes2 = plt.colorbar(sm_pm_stripes2, orientation='vertical', pad=0.02, ax=ax1, aspect=10)
    
    cbar_pm_stripes2.ax.yaxis.set_tick_params(color="white")
    cbar_pm_stripes2.outline.set_edgecolor(label_color)
    cbar_pm_stripes2.ax.yaxis.set_tick_params(size=0, labelsize=11, pad=5, colors=label_color)
    cbar_pm_stripes2.set_ticks(ticks)
    cbar_pm_stripes2.set_ticklabels([labels[ticks.index(tick)] for tick in ticks])

    # Add horizontal lines (black markers) at specific levels
    cbar_ax = cbar_pm_stripes2.ax
    levels_to_mark = [5, 15, 30, 50, 70]  # Example levels where lines should be drawn
    colorbar_height = cbar_ax.get_position().bounds[3]  # Get colorbar height
    for level in levels_to_mark:
        # Draw a white line slightly thicker than the grey line
        cbar_ax.axhline(y=level, color='white', linestyle='solid', linewidth=2, xmin=0, xmax=2)
        # Draw the grey line on top
##        cbar_ax.axhline(y=level, color='grey', linestyle='-', linewidth=2, xmin=0, xmax=1)
        

    ax1.spines['bottom'].set_color(label_color)
    ax1.spines['top'].set_color(label_color)
    ax1.spines['left'].set_color(label_color)
    ax1.spines['right'].set_color(label_color)

    # ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True, colors=label_color)
    # ax1.tick_params(axis='y', colors=label_color)

    ax2.spines['bottom'].set_color(label_color)
    ax2.spines['top'].set_color(label_color)
    ax2.spines['left'].set_color(label_color)
    ax2.spines['right'].set_color(label_color)

    ax1.text(0.03, 0.89, plot_title, ha='left', va='bottom', fontsize=20, fontweight='normal', transform=ax1.transAxes,
             color='black', bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))

    ax1.text(0.03, 0.81, 'Air pollution (PM2.5) concentrations', ha='left', va='bottom', fontsize=10, fontweight='normal', transform=ax1.transAxes, color='black', bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))    

    ax1.text(0.03, 0.73, 'from 1850 to 2022', ha='left', va='bottom', fontsize=10, fontweight='normal', transform=ax1.transAxes, color='black', bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))    
    
    # ax1.text(0.03, 0.01, 'airqualitystripes.info', ha='left', va='bottom', fontsize=10, fontweight='normal', transform=ax1.transAxes, color='black')    

    # Add the label at the bottom left
    ax1.text(0.03, 0.67, 'airqualitystripes.info', ha='left', va='center', fontsize=8, color='black',
             transform=ax1.transAxes, bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))  

#    # Add the uncertainty classification label below the first one
#    ax1.text(0.03, 0.59, f'{uncertainty_classification}, data_ratio = {data_ratio:.1f}', ha='left', va='center', fontsize=8, \
#             color='black',
#             transform=ax1.transAxes, bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))

    plt.savefig(OUTPUT_DATA_DIR + plot_title+'_'+continent+'_aq_stripes_withline_withindicativebar.png', dpi=400, bbox_inches='tight', pad_inches=0.05)
    plt.show()
    plt.close()
















def plot_aq_stripes_withline_withindicativecolourbar_socialmedia(data_combined, years, custom_cmap, plot_title, continent):
    print("plot_aq_stripes_withline_socialmedia")

    # Define the color for labels and borders
    label_color = 'black'

    figsize = (3.6, 4.5)
    fig, ax1 = plt.subplots(figsize=figsize)
    
    fig.patch.set_facecolor('white')
   # Adjust the layout to reduce white space on the left
    plt.subplots_adjust(left=0.0, right=0.9, top=0.9, bottom=0.1)  # Adjust the `left` parameter to reduce left margin    

    # Define the fixed levels for color distribution
    levels = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]    

    norm_pm = mcolors.BoundaryNorm(boundaries=levels, ncolors=custom_cmap.N)
    colors_pm = custom_cmap(norm_pm(data_combined))

    bars_pm_stripes = ax1.bar(years, 1, color=colors_pm, edgecolor='none', width=1)

    # Create a second y-axis for the line plot
    ax2 = ax1.twinx()
    ax2.plot(years, data_combined, color='white', linewidth=2.0)

    # Configure the primary y-axis for the bars
    ax1.set_ylim(0, 1)
    ax1.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)  # Suppress ticks and labels
    ax1.yaxis.label.set_color(label_color)    

    # Configure the secondary y-axis for the line plot
    ax2.set_ylim(0, 120.0)  # Force y-axis to start at zero    
    ax2.tick_params(axis='y', which='both', left=True, right=False, labelleft=True, labelright=False, colors="white")  # Display ticks on the left
    ax2.yaxis.label.set_color(label_color)
    
    # Set the limits for the x-axis
    ax1.set_xlim(years.min(), years.max())
    sm_pm_stripes2 = plt.cm.ScalarMappable(cmap=custom_cmap, norm=norm_pm)
    sm_pm_stripes2.set_array([])
    
    # Custom labels and ticks
    ticks =  [0,   2.5,       5,   10,       20,     40,   50,    61,      65,  88, 83, 85, 90, 80, 70, 60, 30, 15,100]
    labels = ["", "Very Good","","Fair", "Moderate","Poor","", "Very Poor","","Extremely", "Poor","","","","","", "","",""]

    cbar_pm_stripes2 = plt.colorbar(sm_pm_stripes2, orientation='vertical', pad=0.02, ax=ax1, aspect=15)  # Adjust the aspect ratio to make it narrower
    ###cbar_pm_stripes2 = plt.colorbar(sm_pm_stripes2, orientation='vertical', pad=0.02, ax=ax1, aspect=10)
    
    cbar_pm_stripes2.ax.yaxis.set_tick_params(color="white")
    cbar_pm_stripes2.outline.set_edgecolor(label_color)
    cbar_pm_stripes2.ax.yaxis.set_tick_params(size=0, labelsize=10, pad=5, colors=label_color)
    cbar_pm_stripes2.set_ticks(ticks)
    cbar_pm_stripes2.set_ticklabels([labels[ticks.index(tick)] for tick in ticks])

    # Add horizontal lines (black markers) at specific levels
    cbar_ax = cbar_pm_stripes2.ax
    levels_to_mark = [5, 15, 30, 50, 70]  # Example levels where lines should be drawn
    colorbar_height = cbar_ax.get_position().bounds[3]  # Get colorbar height
    for level in levels_to_mark:
        # Draw a white line slightly thicker than the grey line
        cbar_ax.axhline(y=level, color='white', linestyle='solid', linewidth=2, xmin=0, xmax=2)
        # Draw the grey line on top
##        cbar_ax.axhline(y=level, color='grey', linestyle='-', linewidth=2, xmin=0, xmax=1)
        

    ax1.spines['bottom'].set_color(label_color)
    ax1.spines['top'].set_color(label_color)
    ax1.spines['left'].set_color(label_color)
    ax1.spines['right'].set_color(label_color)

    # ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True, colors=label_color)
    # ax1.tick_params(axis='y', colors=label_color)

    ax2.spines['bottom'].set_color(label_color)
    ax2.spines['top'].set_color(label_color)
    ax2.spines['left'].set_color(label_color)
    ax2.spines['right'].set_color(label_color)

    ax1.text(0.03, 1.02, plot_title, ha='left', va='bottom', fontsize=13, fontweight='normal', transform=ax1.transAxes,
             color='black', bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))

    ax1.text(0.04, 0.92, 'Air pollution (PM2.5) from 1850 to 2022', ha='left', va='bottom', fontsize=9, fontweight='normal', transform=ax1.transAxes, color='black', bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))    

    # ax1.text(0.03, 0.90, 'from 1850 to 2022', ha='left', va='bottom', fontsize=9, fontweight='normal', transform=ax1.transAxes, color='black', bbox=dict(facecolor='white', alpha=0.9, edgecolor='none'))    

    # Add the label at the bottom left
    ax1.text(0.04, 0.86, 'airqualitystripes.info', ha='left', va='center', fontsize=8, color='black',
             transform=ax1.transAxes, bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))
    
    plt.savefig(OUTPUT_DATA_DIR + plot_title+'_'+continent+'_aq_stripes_withline_withindicativebar_socialmedia.jpeg', dpi=400, bbox_inches='tight', pad_inches=0.03)
    plt.show()
    plt.close()



import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

def plot_aq_stripes_no_colorbar_with_text(data_combined, years, custom_cmap, plot_title, continent):
    print("plot_aq_stripes_no_colorbar_with_text")

    # Define the color for labels and borders
    label_color = 'black'

    figsize = (8, 5)
    fig, axs = plt.subplots(figsize=figsize)

    fig.patch.set_facecolor('white')

    # Define the fixed levels for color distribution
    # levels = [0, 5, 10, 15, 20, 25, 35, 45, 55, 65, 75, 85, 95, 105]
    # levels = [0, 5, 10, 15, 20, 25, 35, 45, 55, 65, 80, 95]    
    # levels = [0, 5, 10, 15, 20, 25, 35, 45, 55, 65, 80, 95]    
    levels = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]        
    
    norm_pm = mcolors.BoundaryNorm(boundaries=levels, ncolors=custom_cmap.N)
    colors_pm = custom_cmap(norm_pm(data_combined))

    bars_pm_stripes = axs.bar(years, 1, color=colors_pm, edgecolor='none', width=1)

    axs.set_xlim(years.min(), years.max()+0.5) # KP_Change
    axs.set_ylim(0, 1)

    axs.spines['bottom'].set_color(label_color)
    axs.spines['top'].set_color(label_color)
    axs.spines['left'].set_color(label_color)
    axs.spines['right'].set_color(label_color)

    # axs.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=True, colors=label_color)
    axs.tick_params(axis='y', colors='white')

    axs.patch.set_edgecolor(label_color)
    fig.patch.set_edgecolor(label_color)

    axs.text(0.03, 0.89, plot_title, ha='left', va='bottom', fontsize=20, fontweight='normal', transform=axs.transAxes,
             color='black', bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))

    axs.text(0.03, 0.81, 'Air pollution (PM2.5) concentrations from 1850 to 2022', ha='left', va='bottom', fontsize=10, fontweight='normal', transform=axs.transAxes,
             color='black', bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))

    sm_pm_stripes2 = plt.cm.ScalarMappable(cmap=custom_cmap, norm=norm_pm)
    sm_pm_stripes2.set_array([])
    
    # Custom labels and ticks
    ticks =  [0,   2.5,       5,   10,       20,     40,   50,    61,      65,  88, 83, 85, 90, 80, 70, 60, 30, 15,100]
    labels = ["", "Very Good","","Fair", "Moderate","Poor","", "Very Poor","","Extremely", "Poor","","","","","", "","",""]

    cbar_pm_stripes2 = plt.colorbar(sm_pm_stripes2, orientation='vertical', pad=0.02, ax=axs, aspect=10)
    
    cbar_pm_stripes2.ax.yaxis.set_tick_params(color="white")
    cbar_pm_stripes2.outline.set_edgecolor(label_color)
    cbar_pm_stripes2.ax.yaxis.set_tick_params(size=0, labelsize=11, pad=5, colors=label_color)
    cbar_pm_stripes2.set_ticks(ticks)
    cbar_pm_stripes2.set_ticklabels([labels[ticks.index(tick)] for tick in ticks])

    # Add horizontal lines (black markers) at specific levels
    cbar_ax = cbar_pm_stripes2.ax
    levels_to_mark = [5, 15, 30, 50, 70]  # Example levels where lines should be drawn
    colorbar_height = cbar_ax.get_position().bounds[3]  # Get colorbar height
    for level in levels_to_mark:
        # Draw a white line slightly thicker than the grey line
        cbar_ax.axhline(y=level, color='white', linestyle='solid', linewidth=2, xmin=0, xmax=2)
        # Draw the grey line on top
##        cbar_ax.axhline(y=level, color='grey', linestyle='-', linewidth=2, xmin=0, xmax=1)

    # Add the label at the bottom left
    axs.text(0.75, 0.05, 'airqualitystripes.info', ha='left', va='center', fontsize=8, color='black',
             transform=axs.transAxes, bbox=dict(facecolor='white', alpha=0.9, edgecolor='none'))

    plt.savefig(OUTPUT_DATA_DIR + plot_title + '_' + continent + '_aq_stripes_no_colorbar_with_text.png', dpi=400, bbox_inches='tight', pad_inches=0.05)
    plt.show()
    plt.close()



def plot_aq_stripes_noline_notext(data_combined, years, custom_cmap, plot_title, continent):
    print("plot_aq_stripes_noline_notext")

    figsize = (8, 5)
    fig, ax1 = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor('white')

    levels = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]    
    norm_pm = mcolors.BoundaryNorm(boundaries=levels, ncolors=custom_cmap.N)
    colors_pm = custom_cmap(norm_pm(data_combined))

    ax1.bar(years, 1, color=colors_pm, edgecolor='none', width=1)

    ax2 = ax1.twinx()

    # Suppress all ticks and labels on both axes
    ax1.axis('off')
    ax2.axis('off')

    # Set the limits for the x-axis
    ax1.set_xlim(years.min(), years.max())

    ax1.text(0.75, 0.05, 'airqualitystripes.info', ha='left', va='center', fontsize=10, color='black',
             transform=ax1.transAxes, bbox=dict(facecolor='white', alpha=0.9, edgecolor='none'))    

    # Save the figure
    plt.savefig(OUTPUT_DATA_DIR + plot_title + '_' + continent + '_aq_stripes_noline_notext.png', dpi=400, bbox_inches='tight', pad_inches=0.05)
    plt.show()
    plt.close()








def plot_summary_statistics(data_combined, years, custom_cmap, plot_title, continent):
    
    # Calculate the number of years with concentrations < 5 over the full time series
    total_years = len(years)
    years_below_5 = np.sum(data_combined < 5)
    years_above_5 = np.sum(data_combined > 5)
    percentage_years_above_5 = (years_above_5 / total_years) * 100

    # Calculate the highest concentration and the year it occurred
    max_concentration = np.max(data_combined)
    max_concentration_year = years[np.argmax(data_combined)]

    # Calculate the annual mean concentration for the year 2022 (assuming it's the last year in the dataset)
    year_2022_index = np.where(years == 2022)[0][0]
    annual_mean_2022 = np.mean(data_combined[year_2022_index])
    
    print("plot_postcards_empty")

    figsize = (8, 5)  # Keep the same figsize as the original function
    fig, axs = plt.subplots(figsize=figsize)

    fig.patch.set_facecolor('white')

    # Define the fixed levels for color distribution
    # levels = [0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 0.]
    # levels = [0, 5, 10, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105]
    # levels = [0, 5, 10, 15, 20, 25, 35, 45, 55, 65, 75, 85, 95, 105]
    # levels = [0, 5, 10, 15, 20, 25, 35, 45, 55, 65, 80, 95]
    levels = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]    

    norm_pm = mcolors.BoundaryNorm(boundaries=levels, ncolors=custom_cmap.N)
    colors_pm = custom_cmap(norm_pm(data_combined))

    # Adjust the width and remove edgecolor to eliminate white lines
    bars_pm_stripes = axs.bar(years, 1, color=colors_pm, edgecolor='none', width=1.0)

    axs.set_xlim(years.min(), years.max()+0.5) # KP_Change
    axs.set_ylim(0, 1)

    # Adding white rectangles to cover the top 6/8ths and bottom 1/8th
    # Top rectangle (6/8ths (2/3) of the height)
    top_rect = Rectangle((years.min(), 1/6), width=years.max()+0.5 - years.min(), height=5/6, 
                         transform=axs.get_xaxis_transform(), color='white', zorder=2)
    axs.add_patch(top_rect)

    # Set the frame color to white
    axs.spines['top'].set_color('white')
    axs.spines['bottom'].set_color('white')
    axs.spines['left'].set_color('white')
    axs.spines['right'].set_color('white')

    # Set tick parameters color
    axs.tick_params(axis='x', colors='#722a1c')
    axs.tick_params(axis='y', colors='white')  # Set y-axis ticks to white

    # Set x-tick labels color
    for label in axs.get_xticklabels():
        label.set_color('#722a1c')
    
    # Set y-tick labels color
    for label in axs.get_yticklabels():
        label.set_color('white')

    axs.text(years.min() + 2, 0.88, plot_title, ha='left', va='bottom', fontsize=24, fontweight='normal', color='black', fontfamily='DejaVu Sans')
    axs.text(years.min() + 2, 0.81, "Summary of annual mean PM2.5 air pollution concentration from 1850-2021", ha='left', va='bottom', fontsize=10, fontweight='normal', color='black', fontfamily='DejaVu Sans')

    # Add summary statistics text 1 (left justified)
    summary_text = (
        f"years where PM2.5 concentrations were\n"
        f"higher than the World Health Organisation\n"
        f"guideline of 5 µg/m\u00B3.\n"
    )
    axs.text(years.min() + 60, 0.73, summary_text, ha='left', va='top', fontsize=12, fontweight='normal', color='dimgrey')
    axs.text(years.min() + 10, 0.73, f"{percentage_years_above_5:.0f}%", ha='left', va='top', fontsize=32, fontweight='bold', color='dimgrey')

    # Add summary statistics text 2 (right justified)
    summary_text_2 = (
        f"The highest concentration\n"
        f"(µg/m\u00B3, occurred in {max_concentration_year})."
    )
    axs.text(years.min() + 60, 0.53, summary_text_2, ha='left', va='top', fontsize=12, fontweight='normal', color='dimgrey')
    axs.text(years.min() + 20, 0.53, f"{max_concentration:.0f}", ha='left', va='top', fontsize=32, fontweight='bold', color='dimgrey')

    # Add annual mean concentration text (left justified)
    annual_mean_text = (
        f"Annual mean concentration\n"
        f"µg/m\u00B3 in 2022\n"
    )

    axs.text(years.min() + 60, 0.34, annual_mean_text, ha='left', va='top', fontsize=12, fontweight='normal', color='dimgrey')
    axs.text(years.min() + 20, 0.34, f"{annual_mean_2022:.0f}", ha='left', va='top', fontsize=32, fontweight='bold', color='dimgrey')

    # Add the label at the bottom left
    axs.text(0.8, 0.04, 'airqualitystripes.info', ha='left', va='center', fontsize=8, color='black',
             transform=axs.transAxes, bbox=dict(facecolor='white', alpha=0.9, edgecolor='none'))    

    plt.savefig(OUTPUT_DATA_DIR + plot_title+'_'+continent+'_summary_statistics.png', dpi=400, bbox_inches='tight', pad_inches=0.05)
    plt.show()
    plt.close()



def plot_aq_stripes_just_line(data_combined, years, custom_cmap, plot_title, continent):
    print("plot_aq_stripes_withline_no_colorbar")

    # Set the figure background transparent
    fig.patch.set_alpha(0)

    # Define the color for labels and borders
    label_color = 'black'

    figsize = (8, 5)
    fig, ax1 = plt.subplots(figsize=figsize)

    fig.patch.set_facecolor('white')

    # Define the fixed levels for color distribution
    levels = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100]    

    norm_pm = mcolors.BoundaryNorm(boundaries=levels, ncolors=custom_cmap.N)
    colors_pm = "white"

    bars_pm_stripes = ax1.bar(years, 1, color=colors_pm, edgecolor='none', width=1)

    # Create a second y-axis for the line plot
    ax2 = ax1.twinx()
    # Plot the white line with a black outline
    #ax2.plot(years, data_combined, color='white', linewidth=4.0, zorder=2)
    
    # Add a black outline to the white line
    ax2.plot(years, data_combined, color='black', linewidth=6.0, zorder=1)  # Black outline
    ax2.plot(years, data_combined, color='white', linewidth=4.0, zorder=2)  # White line

    
    ax2.plot(years, data_combined, color='black', linewidth=1.5, zorder=1)

    # Configure the primary y-axis for the bars
    ax1.set_ylim(0, 1)
    ax1.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)  # Suppress ticks and labels
    ax1.yaxis.label.set_color(label_color)    

    # Configure the secondary y-axis for the line plot
    ax2.set_ylim(0, 120.0)  # Force y-axis to start at zero    
    ax2.tick_params(axis='y', which='both', left=True, right=False, labelleft=True, labelright=False, colors="black")  # Display ticks on the left
    ax2.yaxis.label.set_color(label_color)
    
    # Set the limits for the x-axis
    ax1.set_xlim(years.min(), years.max())

    # Customize axes appearance
    ax1.spines['bottom'].set_color("white")
    ax1.spines['top'].set_color("white")
    ax1.spines['left'].set_color("white")
    ax1.spines['right'].set_color("white")

    ax2.spines['bottom'].set_color("white")
    ax2.spines['top'].set_color("white")
    ax2.spines['left'].set_color("white")
    ax2.spines['right'].set_color("white")

    # Add title and labels
    ax1.text(0.03, 0.89, plot_title, ha='left', va='bottom', fontsize=20, fontweight='normal', transform=ax1.transAxes,
             color='black', bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))

    ax1.text(0.03, 0.81, 'Air pollution (PM2.5) concentrations', ha='left', va='bottom', fontsize=10, fontweight='normal', transform=ax1.transAxes, color='black', bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))    

    ax1.text(0.03, 0.73, 'from 1850 to 2022', ha='left', va='bottom', fontsize=10, fontweight='normal', transform=ax1.transAxes, color='black', bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))    

    # Add the label at the bottom left
    ax1.text(0.03, 0.67, 'airqualitystripes.info', ha='left', va='center', fontsize=8, color='black',
             transform=ax1.transAxes, bbox=dict(facecolor='white', alpha=1.0, edgecolor='none'))    
    
    plt.savefig(OUTPUT_DATA_DIR + plot_title+'_'+continent+'_aq_stripes_justline.png', dpi=400, bbox_inches='tight', pad_inches=0.05, transparent=True)
    plt.show()
    plt.close()



