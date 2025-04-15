import numpy as numpy
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import geopandas as gpd
import os
import urllib.request
import zipfile
from cartopy.feature import GSHHSFeature
from mpl_toolkits.axes_grid1 import make_axes_locatable
import cmocean
from matplotlib.patches import Rectangle
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D
from matplotlib.tri import Triangulation

print(f"NumPy version: {numpy.__version__}")

def read_gr3_file(filename):
    try:
        with open(filename, 'r') as f:
            _ = f.readline()  # Discard first line (comment)
            ne, np = map(int, f.readline().split())

            nodes = numpy.empty((np, 3))
            for i in range(np):
                nodes[i] = list(map(float, f.readline().split()[1:4]))

            elements = []
            for _ in range(ne):
                elements.append(list(map(lambda x: int(x) - 1, f.readline().split()[2:])))

        print(f"Number of nodes: {np}")
        print(f"Number of elements: {ne}")
        return nodes, elements
    except Exception as e:
        print(f"Error reading file: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def read_hurricane_track(filename):
    """Read hurricane track data from a text file with lat,lon coordinates."""
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            track_data = numpy.array([list(map(float, line.strip().split())) for line in lines])
        print(f"Read {len(track_data)} hurricane track points")
        return track_data
    except Exception as e:
        print(f"Error reading hurricane track file: {e}")
        import traceback
        traceback.print_exc()
        return None

def download_coastline_data():
    url = "https://naciscdn.org/naturalearth/1m/physical/ne_1m_coastline.zip"
    zip_path = "ne_1m_coastline.zip"
    shapefile_path = "ne_1m_coastline.shp"

    if not os.path.exists(shapefile_path):
        print("Downloading coastline data...")
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall()
        os.remove(zip_path)
    return shapefile_path

def download_gadm_data():
    url = "https://geodata.ucdavis.edu/gadm/gadm4.1/shp/gadm41_USA_shp.zip"
    zip_path = "gadm41_USA_shp.zip"
    shapefile_path = "gadm41_USA_1.shp"

    if not os.path.exists(shapefile_path):
        print("Downloading GADM data...")
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall()
        os.remove(zip_path)
    return shapefile_path

def plot_gr3_with_hurricane_track(nodes, elements, hurricane_track, output_file):
    if nodes is None or elements is None or hurricane_track is None:
        print("Cannot plot: invalid input data")
        return

    print("Preparing improved plot...")
    
    # Create figure with a better size ratio
    fig = plt.figure(figsize=(24, 16))
    
    # Main zoomed-in axis
    ax_main = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax_main.set_extent([-75.85, -75.5, 36.0, 36.45], crs=ccrs.PlateCarree())
    ax_main.set_facecolor('#D6EAF8')  # Lighter blue for better contrast
    
    # Add land features with better coloring
    land = GSHHSFeature(scale='full', levels=[1], facecolor='#F5DEB3', edgecolor='#8B4513')
    ax_main.add_feature(land)
    
    # Inset map in better position - ZOOMED IN ON US EAST COAST
    ax_inset = fig.add_axes([0.72, 0.30, 0.3, 0.4], projection=ccrs.PlateCarree())
    # More zoomed in view focusing on US East Coast
    # ax_inset.set_extent([-82, -67, 27.5, 42.5], crs=ccrs.PlateCarree())  # Zoomed in to East Coast
    ax_inset.set_extent([-77, -69.5, 30.0, 40.0], crs=ccrs.PlateCarree())  # Zoomed in to East Coast

    ax_inset.set_facecolor('#D6EAF8')
    ax_inset.add_feature(land)
    #ax_inset.set_title('Hurricane Sandy Track', fontsize=16)
    
    # Add Duck domain box on the inset map
    duck_box = Rectangle(
        xy=[-75.85, 36.0],
        width=0.35,
        height=0.45,
        linewidth=2,
        edgecolor='blue',
        facecolor='none',
        transform=ccrs.PlateCarree(),
        zorder=10
    )
    ax_inset.add_patch(duck_box)
    
    # Add frame to the inset map for better visual separation
    ax_inset.spines['geo'].set_edgecolor('black')
    ax_inset.spines['geo'].set_linewidth(1.5)
    
    # Plot hurricane track with arrow markers showing direction
    track_lats = hurricane_track[:, 0]
    track_lons = hurricane_track[:, 1]
    
    # Add arrow indicating track direction
    arrow_indices = np.linspace(0, len(track_lons)-1, 5).astype(int)
    
    ax_inset.plot(track_lons, track_lats, 'r-', linewidth=2.5, transform=ccrs.PlateCarree())
    ax_inset.plot(track_lons[0], track_lats[0], 'go', markersize=8, transform=ccrs.PlateCarree())
    ax_inset.plot(track_lons[-1], track_lats[-1], 'ro', markersize=8, transform=ccrs.PlateCarree())
    
    # Add direction arrows along track
    #for i in arrow_indices[1:]:
    #    if i < len(track_lons) - 1:  # Ensure index is valid
    #        ax_inset.annotate('',
    #            xytext=(track_lons[i-1], track_lats[i-1]),
    #            xy=(track_lons[i], track_lats[i]),
    #            arrowprops=dict(arrowstyle='->', color='red', lw=2),
    #            transform=ccrs.PlateCarree())
    #
    # Add legend for track
#    start_point = Line2D([], [], color='green', marker='o', linestyle='None', markersize=8, label='Track Start')
#    end_point = Line2D([], [], color='red', marker='o', linestyle='None', markersize=8, label='Track End')
    track_line = Line2D([], [], color='red', linewidth=2.5, label='Track of Hurricane Sandy')
    ax_inset.legend(handles=[track_line], loc='lower right', fontsize=12, frameon=True)
    
    # Connect inset to main plot with proper arrow
    arrow = FancyArrowPatch(
        (0.88, 0.65),  # Start (inset box)
        (0.70, 0.48),  # End (main panel)
        transform=fig.transFigure,
        connectionstyle="arc3,rad=-0.2",
        arrowstyle='simple',  # Changed to simple arrow style which is more visible
        linewidth=2,
        color='blue',
        mutation_scale=20,  # Make the arrow head larger
        zorder=20
    )
    #fig.add_artist(arrow)
    
    # Add grid lines to inset
    gl_inset = ax_inset.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl_inset.top_labels = False
    gl_inset.right_labels = False
    gl_inset.xformatter = LONGITUDE_FORMATTER
    gl_inset.yformatter = LATITUDE_FORMATTER
    
    # Create improved line segments for grid elements - MAIN PLOT
    segs = []
    depths = []
    for element in elements:
        points = nodes[element, :2]
        depth_avg = np.mean(nodes[element, 2])
        segs.append(np.concatenate([points, points[[0]]]))
        depths.append(depth_avg)
    
    # Vary line width based on depth for main plot
    depths = np.array(depths)
    norm = plt.Normalize(0, 30)
    linewidths = 0.8 - 0.5 * norm(depths)  # Thicker lines in shallow water
    
    line_segments = LineCollection(segs, linewidths=linewidths, colors='navy', alpha=0.5, transform=ccrs.PlateCarree())
    ax_main.add_collection(line_segments)
    
    # Add the mesh to the inset map too - INSET PLOT (thinner lines)
    inset_line_segments = LineCollection(segs, linewidths=0.2, colors='navy', alpha=0.3, transform=ccrs.PlateCarree())
    ax_inset.add_collection(inset_line_segments)
    
    # Create triangulation for improved bathymetry
    tri = Triangulation(nodes[:, 0], nodes[:, 1], elements)
    
    # Use cmocean colormap for better depth visualization
    levels = np.linspace(0, 30, 31)
    cmap = cmocean.cm.deep_r  # reversed deep colormap
    
    contourf = ax_main.tricontourf(tri, nodes[:, 2], levels=levels, cmap=cmap, alpha=0.9, 
                                  transform=ccrs.PlateCarree(), extend='max')
    
    # Add colorbar with better positioning
    cax = fig.add_axes([0.31, 0.03, 0.4, 0.03])
    cbar = fig.colorbar(contourf, cax=cax, orientation='horizontal')
    cbar.set_label('Depth (m)', fontsize=20)
    cbar.ax.tick_params(labelsize=18)
    
    # Add grid lines to main plot
    gl_main = ax_main.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl_main.xlabel_style = {'size': 16}
    gl_main.ylabel_style = {'size': 16}
    gl_main.top_labels = False
    gl_main.right_labels = False
    gl_main.xformatter = LONGITUDE_FORMATTER
    gl_main.yformatter = LATITUDE_FORMATTER
    
    # Add observation stations with labels
    stations = [
        (-75.7504837, 36.1863092, "Station 1"),
        (-75.7465300, 36.1873300, "Station 2"),
        (-75.7432300, 36.1881840, "Station 3"),
        (-75.7140500, 36.1998830, "Station 4"),
        (-75.5913333, 36.2548333, "Station 5"),
    ]
    
    # Plot stations with improved markers
    for lon, lat, name in stations:
        ax_main.plot(lon, lat, marker='^', color='red', markersize=10, 
                   markeredgecolor='black', markeredgewidth=1.5,
                   transform=ccrs.PlateCarree())
        
        # Improved label placement with offsets
        #if name == "Station 5":  # Rightmost station
        #    ax_main.text(lon-0.01, lat+0.01, name, fontsize=12, color='black',
        #               transform=ccrs.PlateCarree(), ha='right', 
        #               bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
        #elif name in ["Station 1", "Station 2"]:  # Very close stations, adjust positioning
        #    offset_y = 0.01 if name == "Station 1" else -0.01
        #    ax_main.text(lon+0.01, lat+offset_y, name, fontsize=12, color='black',
        #               transform=ccrs.PlateCarree(), ha='left', 
        #               bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
        #else:
         #   ax_main.text(lon+0.01, lat+0.01, name, fontsize=12, color='black',
         #              transform=ccrs.PlateCarree(), ha='left', 
         #              bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
    
    # Add a legend for observation stations
    legend_marker = Line2D([], [], color='red', marker='^', linestyle='None',
                         markersize=10, markeredgecolor='black', markeredgewidth=1.5,
                         label='Observation Stations')
    ax_main.legend(handles=[legend_marker], loc='upper right', fontsize=14, frameon=True)
    
    # Add Duck, NC label
    #ax_main.text(-75.75, 36.185, "Duck, NC", fontsize=18, color='black',
    #           transform=ccrs.PlateCarree(), ha='center', va='center',
    #           bbox=dict(facecolor='white', alpha=0.7, boxstyle='round'))
    
    # Add improved north arrow
    north_arrow = FancyArrowPatch(
        (0.95, 0.2),  # Arrow start position
        (0.95, 0.3),  # Arrow end position
        transform=fig.transFigure,
        arrowstyle='-|>',
        linewidth=2,
        color='black',
        mutation_scale=20
    )
#    fig.add_artist(north_arrow)
#    fig.text(0.95, 0.32, 'N', fontsize=16, ha='center', fontweight='bold')
    
    # Add improved title
    ax_main.set_title('', 
                     fontsize=22, pad=20)
    
    print(f"Saving improved plot to {output_file}...")
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print("Plot saved successfully.")

# Usage
if __name__ == "__main__":
    grid_filename = 'hgrid.gr3'
    track_filename = 'track_file_nine.txt'
    output_file = 'schism_grid_with_track_bathy_improved_v2.png'

    print(f"Reading grid file: {grid_filename}")
    nodes, elements = read_gr3_file(grid_filename)
    
    print(f"Reading hurricane track file: {track_filename}")
    hurricane_track = read_hurricane_track(track_filename)
    
    if nodes is not None and elements is not None and hurricane_track is not None:
        plot_gr3_with_hurricane_track(nodes, elements, hurricane_track, output_file)
    else:
        print("Failed to read input files. Please check the file paths and formats.")
