import requests
import os
import pandas as pd
from scipy.io import savemat
import numpy as np

### ADJUST VARIABLES HERE ###
def extract_data(solarLong,localTime):
    ###variables###
    var1 = "solzenang" #Solar zenith angle (deg)
    var2 = "fluxsurf_dn_sw" #Incident solar flux on horizontal surface (W/m2)
    var3 = "tauref" #Daily mean dust column visible optical depth
    var4 = "t" #Temperature (K)

    ###spaital coordinates###
    marsLat = "all"
    marsLong = "all"
    marsAlt = "10."
    altType = "3" #sets altitude unit to be meters above surface

    base_url=f'https://www-mars.lmd.jussieu.fr/mcd_python/cgi-bin/mcdcgi.py?var1={var1}&var2={var2}&var3={var3}&var4={var4}&datekeyhtml={datetype}&ls={solarLong}&localtime={localTime}&year={earthYear}&month={earthMonth}&day={earthDay}&hours={earthHour}&minutes={earthMinute}&seconds={earthSecond}&julian={julianDay}&martianyear={marsYear}&sol={sols}&latitude={marsLat}&longitude={marsLong}&altitude={marsAlt}&zkey={altType}&spacecraft={spacecraft}&isfixedlt={localTimeIsFixed}&dust={dustScenario}&hrkey={isHighRes}&averaging={averagingType}&dpi={figureFormat}&islog={isLogValues}&colorm={colormapType}&minval={minValue}&maxval={maxValue}&proj={mapType}&palt={projAlt}&plon={projLong}&plat={projLat}&trans={transparency}&iswind={isWind}&latpoint={markerLat}&lonpoint={markerLong}'

    response = requests.get(base_url, timeout=10)
    data_url = r'https://www-mars.lmd.jussieu.fr/mcd_python'+response.text[response.text.find(r"/txt"):response.text.find(">Click")-1]
    
    return data_url

def convert_data(data_url, dfs):
    content = requests.get(data_url).text

    # Initialize a list to hold DataFrames for each dataset
    dataset_blocks = content.split('MCD_v6.1 with climatology average solar scenario.')
    # Iterate over the dataset blocks

    varnum = 0
    for block in dataset_blocks[1:]:
        # Clean any extra whitespace or empty lines
        block = block.strip()
        # Extract the variable name from the first block (this will be in the metadata)
        for lines in block.splitlines():
            if 'Columns 2+ are ' in lines:
                variable_name = ''.join([a.capitalize() for a in lines[lines.find('Columns 2+ are ')+15:].strip().split(' ')]) if "(" not in lines else ''.join([a.capitalize() for a in lines[lines.find('Columns 2+ are ')+15:lines.find("(")].strip().split(' ')])
        
        # Split the dataset into lines
        lines = block.splitlines()[9:]
        # Process the data lines
        data = []
        longitude = []
        latitude = lines[0].split()[2:]
        for line in lines[2:]:
            # Skip the separator lines
            if '----' in line or '||' not in line:
                continue
            # Split each line by spaces
            parts = line.split()
            longitude.append(parts[0])
            values = parts[2:] if '#' not in parts else parts[2:parts.find('#')]
            data.append(values)

        # Create a DataFrame from the data
        df = pd.DataFrame(data, columns=latitude, index=longitude)
        
        #Append dataframe to dataframelist for 3D array
        if variable_name in dfs:
            dfs[variable_name].append(df)
        else:
            dfs.update({variable_name:[df]})
        varnum += 1

    return dfs

def main():
    download_directory = ''
    download_directory = download_directory if download_directory != '' else os.getcwd() #I just copy pasted this from the savemat line, idk why its not happy
    array_dict = {}
    array_4d_dict = {}
    for solarLong in range(15,360+15,30): #range doesn't include target
        #Setup dict of lists of df for each hour
        dfs = {}
        for localTime in range(0,25):
            data_url = extract_data(solarLong, localTime)
            dfs = convert_data(data_url, dfs)
            print(f"Collected data for {solarLong}_{localTime}")
        # Stack them into a 3D array: shape will be (hours, longitude, latitude)
        for var in dfs:
            array = np.stack([df.values for df in dfs[var]])
            if var in array_dict:
                array_dict[var].append(array)
            else:
                array_dict.update({var:[array]})
    # Stack them into a 4D array: shape will be (solarLong, hours, longitude, latitude)
    for var in array_dict:
        array_4d = np.stack([array_3d for array_3d in array_dict[var]])
        array_4d_dict.update({var:np.float64(array_4d)})
    #Make directory
    os.makedirs(download_directory, exist_ok=True)

    #Save All Data in single matlab file
    savemat(download_directory, array_4d_dict)
    print("Complete")

# Variable Name:                                           Input:

# Temperature (K)                                          t
# Pressure (Pa)                                            p
# Density (kg/m3)                                          rho
# W-E wind component (m/s)                                 u
# S-N wind component (m/s)                                 v
# Horizontal wind speed (m/s)                              wind
# Radial distance from planet center (m)                   zradius
# Altitude above areoid (Mars geoid) (m)                   zareoid
# Altitude above local surface (m)                         zsurface
# Orographic height (m) (surface altitude above areoid)    oroheight
# GCM orography (m)                                        oro_gcm
# Local slope inclination (deg) (HR mode only)             theta_s
# Local slope orientation (deg) (HR mode only)             psi_s
# Sun-Mars distance (in Astronomical Unit AU)              marsau
# Ls, solar longitude of Mars (deg)                        ls
# LST:Local true solar time (hrs)                          loctime
# LMT:Local mean time (hrs) at sought longitude            lmeantime
# Universal solar time (LST at lon=0) (hrs)                utime
# Solar zenith angle (deg)                                 solzenang
# Surface temperature (K)                                  tsurf
# Surface pressure (Pa)                                    ps
# GCM surface pressure (Pa)                                ps_gcm
# Potential temperature (K) (reference pressure=610Pa)     potential_temp
# Downward vertical wind component (m/s)                   w_l
# Zonal slope wind component (m/s) (HR mode only)          zonal_slope_wind
# Meridional slope wind component (m/s) (HR mode only)     merid_slope_wind
# Surface pressure RMS day to day variations (Pa)          rmsps
# Surface temperature RMS day to day variations (K)        rmstsurf
# Atmospheric pressure RMS day to day variations (Pa)      altrmsp
# Density RMS day to day variations (kg/m^3)               rmsrho
# Temperature RMS day to day variations (K)                rmst
# Zonal wind RMS day to day variations (m/s)               rmsu
# Meridional wind RMS day to day variations (m/s)          rmsv
# Vertical wind RMS day to day variations (m/s)            rmsw
# Incident solar flux at top of the atmosphere (W/m2)      fluxtop_dn_sw
# solar flux reflected to space (W/m2)                     fluxtop_up_sw
# Incident solar flux on horizontal surface (W/m2)         fluxsurf_dn_sw
# Incident solar flux on local slope (W/m2) (HR mode only) fluxsurf_dn_sw_hr
# Reflected solar flux on horizontal surface (W/m2)        fluxsurf_up_sw
# thermal IR flux to space (W/m2)                          fluxtop_lw
# thermal IR flux on surface (W/m2)                        fluxsurf_lw
# GCM surface roughness length z0 (m)                      z_0
# GCM surface thermal inertia                              thermal_inertia
# GCM surface bare ground albedo                           ground_albedo
# Monthly mean dust column visible optical depth           dod
# Daily mean dust column visible optical depth             tauref
# Dust mass mixing ratio (kg/kg)                           dust_mmr
# Dust effective radius (m)                                dust_reff
# Daily mean dust deposition rate (kg m-2 s-1)             dust_dep
# Monthly mean surface CO2 ice layer (kg/m2)               co2ice
# Monthly mean surface H2O layer (kg/m2)                   surf_h2o_ice
# GCM perennial surface water ice (0 or 1)                 water_cap
# Water vapor column (kg/m2)                               col_h2ovapor
# Water vapor vol. mixing ratio (mol/mol)                  vmr_h2o
# Water ice column (kg/m2)                                 col_h2oice
# Water ice mixing ratio (mol/mol)                         vmr_h2oice
# Water ice effective radius (m)                           h2oice_reff
# Convective Planetary Boundary Layer (PBL) height (m)     zmax
# Max. upward convective wind within the PBL (m/s)         wstar_up
# Max. downward convective wind within the PBL (m/s)       wstar_dn
# Convective vertical wind variance at level z (m2/s2)     vvv
# Convective eddy vertical heat flux at level z (m/s/K)    vhf
# Surface wind stress (kg/m/s2)                            surfstress
# Surface sensible heat flux (W/m2)                        sensib_flux
# Air heat capacity Cp (J kg-1 K-1)                        Cp
# Ratio of specific heats Cp/Cv                            gamma
# Molecular gas constant R (J K-1 kg-1)                    Rgas
# Air viscosity estimation (N s m-2)                       viscosity
# Scale height H(p) (m)                                    pscaleheight
# [CO2] volume mixing ratio (mol/mol)                      vmr_co2
# [N2] volume mixing ratio  (mol/mol)                      vmr_n2
# [Ar] volume mixing ratio  (mol/mol)                      vmr_ar
# [CO] volume mixing ratio  (mol/mol)                      vmr_co
# [O] volume mixing ratio   (mol/mol)                      vmr_o
# [O2] volume mixing ratio  (mol/mol)                      vmr_o2
# [O3] volume mixing ratio  (mol/mol)                      vmr_o3
# [H] volume mixing ratio   (mol/mol)                      vmr_h
# [H2] volume mixing ratio  (mol/mol)                      vmr_h2
# [He] volume mixing ratio  (mol/mol)                      vmr_he
# CO2 column (kg/m2)                                       col_co2
# N2 column  (kg/m2)                                       col_n2
# Ar column  (kg/m2)                                       col_ar
# CO column  (kg/m2)                                       col_co
# O column   (kg/m2)                                       col_o
# O2 column  (kg/m2)                                       col_o2
# O3 column  (kg/m2)                                       col_o3
# H column   (kg/m2)                                       col_h
# H2 column  (kg/m2)                                       col_h2
# He column  (kg/m2)                                       col_he
# Electron number density (particules/cm3)                 vmr_elec
# Total electonic content (TEC) (particules/m2)            col_elec

#Initialising Variables
datetype = 1
earthYear = ""
earthMonth = ""
earthDay = ""
earthHour = ""
earthMinute = ""
earthSecond = ""
marsYear = ""
sols = ""
julianDay = ""
spacecraft = "none"
minValue = ""
maxValue = ""
projAlt = ""
projLong = ""
projLat = ""
markerLat = ""
markerLong = ""
localTimeIsFixed = "off"
dustScenario = "1" 
isHighRes = "1"
averagingType = "off"
figureFormat = "80" 
isLogValues = "off"
colormapType = "jet"
mapType = "cyl"
transparency = ""
isWind = "off"

if __name__ == "__main__":
    main()