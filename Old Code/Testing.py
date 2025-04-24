import requests

#Initialising Manual Variables
solarLong = ""
localTime = ""
earthYear = ""
earthMonth = ""
earthDay = ""
earthHour = ""
earthMinute = ""
earthSecond = ""
marsYear = ""
sols = ""
julianDay = ""

#Initialising Less Important Website Defaulted Variables
spacecraft = "none"
minValue = ""
maxValue = ""
projAlt = ""
projLong = ""
projLat = ""
markerLat = ""
markerLong = ""
localTimeIsFixed = "off"
dustScenario = "1" #default is climatology ave solar, check manual code below to see other codes
isHighRes = "1"
averagingType = "off"
figureFormat = "80" #PNG value
isLogValues = "off"
colormapType = "jet"
mapType = "cyl"
transparency = ""
isWind = "off"


#Do you want to manually try
manualInput = False

if manualInput == False:
        ###variables###
    var1 = "solzenang" #Solar zenith angle (deg)
    var2 = "fluxsurf_dn_sw" #Incident solar flux on horizontal surface (W/m2)
    var3 = "tauref" #Daily mean dust column visible optical depth
    var4 = "none"

        ###date###
    #if using earth date set datetype = 0, if mars set datetype = 1
    datetype = 1
    if datetype == 0:
        #if using earth time:
        localTime = ""
        earthYear = ""
        earthMonth = ""
        earthDay = ""
        earthHour = ""
        earthMinute = ""
        earthSecond = ""
        julianDay = requests.get(f'https://aa.usno.navy.mil/api/juliandate?date={earthYear}-{earthMonth}-{earthDay}&time={earthHour}:{earthMinute}:{earthSecond}').json()["data"][0]["jd"]
        sols = (julianDay-2442765.667)*(86400/88775.245)
        marsYear = 12
        while sols >= 668.6:
            sols -= 668.6
            marsYear += 1
        while sols <= 668.6:
            sols += 668.6
            marsYear -= 1
    elif datetype == 1:
        #if using mars time
        solarLong = "15"
        localTime = "all"

        ###spaital coordinates###
    marsLat = "all"
    marsLong = "all"
    marsAlt = "10."
    altType = "3" #sets altitude unit to be meters above surface, check manual code below for the other numbers for different units

else:
    ###VARIABLE(S) TO DISPLAY OR DOWNLOAD###
    variables_url = "https://www-mars.lmd.jussieu.fr/mcd_python/listvar.js"
    variables = requests.get(variables_url).text.splitlines()

    for var in variables:
        varnames = [var[var.find(">")+1:var.rfind("<")] for var in variables[1:-1]]
        varactual = [var[var.find('"')+1:var.rfind('"')] for var in variables[1:-1]]

    max_len = max(len(item) for item in varnames)
    print("Variable:".ljust(max_len),"Input:\n")
    for a, b in zip(varnames, varactual):
        print(a.ljust(max_len), b)

    while True:
        var1 = input("\nSelect first variable:\n")
        if var1 not in varactual and var1 != 't':
            if input("Invalid option\nTry again (type '1') or End Script (type '2')?\n") == '2':
                quit
            else:
                continue
        var2 = input("Select second variable or leave blank:\n")
        if var2 == "":
            var2 = "none"
            break
        elif var2 not in varactual and var1 != 't':
            if input("Invalid option\nTry again (type '1') or End Script (type '2')?\n") == '2':
                quit
            else:
                continue
        var3 = input("Select third variable or leave blank:\n")
        if var3 == "":
            var3 = "none"
            break
        elif var3 not in varactual and var1 != 't':
            if input("Invalid option\nTry again (type '1') or End Script (type '2')?\n") == '2':
                quit
            else:
                continue
        var4 = input("Select fourth variable or leave blank:\n")
        if var4 == "":
            var4 = "none"
            break
        elif var4 not in varactual and var1 != 't':
            if input("Invalid option\nTry again (type '1') or End Script (type '2')?\n") == '2':
                quit
            else:
                continue
        break

    ###Spacecraft landing site and date presets###
    if input("Use preset location and date based on spacecraft or current time at equator? (y/n):\n").strip().lower() == "n":
        ###TIME COORDINATES###
        print("Use Earth Date or Mars Date?")
        datetype = int(input("Type 0 for Earth Date and 1 for Mars Date:\n"))
        if datetype == 0:
            earthYear = input("Input year:\n")
            earthMonth = input("Input month (number):\n")
            earthDay = input("Input day:\n")
            earthHour = input("Input hour:\n")
            earthMinute = input("Input minute:\n")
            earthSecond = input("Input second:\n")
            julianDay = requests.get(f'https://aa.usno.navy.mil/api/juliandate?date={earthYear}-{earthMonth}-{earthDay}&time={earthHour}:{earthMinute}:{earthSecond}').json()["data"][0]["jd"]
            sols = (julianDay-2442765.667)*(86400/88775.245)
            marsYear = 12
            while sols >= 668.6:
                sols -= 668.6
                marsYear += 1
            while sols <= 668.6:
                sols += 668.6
                marsYear -= 1
        else:
            print("For these two variables, either write a value, a range of 2 values separated by a '+', or 'all'")
            solarLong = input("Input Solar Longitude (Ls):\n")
            localTime = input("Input Local Time: \n")

        ###SPATIAL COORDINATES###
        print("If you selected Mars Date and have put a range of values, then you can only put 1 value for these next 3 variables")
        print("If not, then for >2< of the next >3< variables you can write a value, a range of 2 values separated by a '+', or 'all'")
        marsLat = input("Input Martian Latitude:\n")
        marsLong = input("Input Martian Longitude:\n")
        print("Before selecting a value or range of values for Martian Altitude, select the distinction:")
        Distinctions = ['m from Mars center','m above "sea level"','m above surface','Pa (pressure level)']
        max_len = max(len(item) for item in Distinctions)
        print("Distinction:".ljust(max_len),"Input:\n")
        for a, b in zip(Distinctions, [1,2,3,4]):
            print(a.ljust(max_len), b)
        altType = input("\nInput number:\n")
        marsAlt = input("Now input Martian Altitude:\n")
    else:
        #selecting craft
        while True:
            print("Select option:")
            spacecraftList = ['equation','Zhurong','Perseverance','Insight','Curiosity','Phoenix','Opportunity','Spirit','Pathfinder','Viking 1','Viking 2']
            print(o for o in spacecraftList)
            spacecraft = input("").strip()
            if spacecraft not in spacecraftList:
                spacecraft = spacecraft[0].upper + spacecraft[1:]
            if spacecraft not in spacecraftList:
                print("Invalid option")
                if input("Try again or end script? (type 1 or 2 respectively)") == "2":
                    exit
            else:
                break

    ###CUSTOMIZE DATA REQUEST###
    localTimeIsFixed = "on" if input("Should the local time be fixed everywhere? (y/n)\n").strip().lower() == "y" else "off"
    dustScenarioList = ['climatology ave solar','climatology min solar','climatology max solar','dust storm min solar','dust storm ave solar','dust storm max solar','warm (dusty, max solar)','cold (low dust, min solar)',
                        'Martian Year 24','Martian Year 25','Martian Year 26','Martian Year 27','Martian Year 28','Martian Year 29','Martian Year 30','Martian Year 31','Martian Year 32','Martian Year 33','Martian Year 34','Martian Year 35']
    dustScenarioInputs = ['1','2','3','4','5','6','7','8','24','25','26','27','28','29','30','31','32','33','34','35']
    while True:
        print("Choose a Dust/EUV Scenario")
        max_len = max(len(item) for item in dustScenarioList)
        print("Scenario:".ljust(max_len),"Input:\n")
        for a, b in zip(dustScenarioList, dustScenarioInputs):
            print(a.ljust(max_len), b)
        dustScenario = input("Input:\n")
        if dustScenario not in dustScenarioInputs:
            print("Invalid Input")
            if input("Try again or end script? (type 1 or 2 respectively)") == "2":
                exit
        else:
            break

    isHighRes = "1" if input("Turn on high-resolution topography? (y/n)\n").strip().lower() == "y" else "0"
    AveragingList = ['off','zonal','diurnal']
    print("Pick an Averaging Type")
    print("\n".join(f"{a}" for a in AveragingList))
    averagingType = input("Input:\n").strip().lower()

    ###CUSTOMIZE FIGURES
    figureFormatList = ['PNG','PNG hi-res','EPS']
    figureFormatInputs = ['80','160','eps']
    while True:
        print("Choose a Figure Format:")
        max_len = max(len(item) for item in figureFormatList)
        print("Scenario:".ljust(max_len),"Input:\n")
        for a, b in zip(figureFormatList, figureFormatInputs):
            print(a.ljust(max_len), b)
        figureFormat = input("Input:\n")
        if figureFormat not in figureFormatInputs:
            print("Invalid Input")
            if input("Try again or end script? (type 1 or 2 respectively)") == "2":
                exit
        else:
            break
    isLogValues = "on" if input("Is your map 1D and you want to use the log of the values? (y/n)?\n").strip().lower() == "y" else "off"
    if isLogValues != "on":
        if input("Is your map 2D (y/n)?\n").strip().lower() == "y":
            colormapTypeList = ['blue green yellow red','grey','blue','yellow orange red','rainbow','black red yellow','blue white red','red white blue']
            colormapTypeInputs = ['jet','Greys','Blues','YlOrRd','spectral','hot','RdBu_r','RdBu']
            while True:
                print("Choose a colormap format:")
                max_len = max(len(item) for item in colormapTypeList)
                print("Scenario:".ljust(max_len),"Input:\n")
                for a, b in zip(colormapTypeList, colormapTypeInputs):
                    print(a.ljust(max_len), b)
                colormapType = input("Input (case sensitive):\n")
                if colormapType not in colormapTypeInputs:
                    print("Invalid Input")
                    if input("Try again or end script? (type 1 or 2 respectively)") == "2":
                        exit
                else:
                    break
            if input("Do you want to set a range of values? (y/n)\n").strip().lower() == "y":
                minValue = input("Set the minimum value:\n")
                maxValue = input("Set the maximum value:\n")
            mapTypeList = ['Flat','Sphere','North Pole','SouthPole']
            mapTypeInputs = ['cyl','nsper','npstere','spstere']
            while True:
                print("Choose a map format:")
                max_len = max(len(item) for item in mapTypeList)
                print("Scenario:".ljust(max_len),"Input:\n")
                for a, b in zip(mapTypeList, mapTypeInputs):
                    print(a.ljust(max_len), b)
                mapType = input("Input (case sensitive):\n")
                if mapType not in mapTypeInputs:
                    print("Invalid Input")
                    if input("Try again or end script? (type 1 or 2 respectively)") == "2":
                        exit
                else:
                    break
            if mapType == 'nsper':
                projAlt = input('From what Altitude do you want to view the map? (in km):\n')
                projLong = input('From what Longitude do you want to view the map?:\n')
                projLat = input('From what Latitude do you want to view the map?:\n')
            elif mapType == 'npstere':
                projLat = input("View map from 90 to what degrees North?\n")
            elif mapType == 'spstere':
                projLat = input("View map from -90 to what degrees North?\n")
            transparency = input("What % transparency do you want the map (leave blank to leave unaffected)\n")
            if transparency == 0:
                transparency = ""
            isWind = "on" if input("Do you want to include wind vectors? (y/n)\n").strip().lower() == 'y' else 'off'
            if input("Do you want to add a marker to a point in the map? (y/n)").strip().lower() == 'y':
                markerLat = input("Input Latitude:\n")
                markerLong = input("Input Longitude:\n")

base_url=f'https://www-mars.lmd.jussieu.fr/mcd_python/cgi-bin/mcdcgi.py?var1={var1}&var2={var2}&var3={var3}&var4={var4}&datekeyhtml={datetype}&ls={solarLong}&localtime={localTime}&year={earthYear}&month={earthMonth}&day={earthDay}&hours={earthHour}&minutes={earthMinute}&seconds={earthSecond}&julian={julianDay}&martianyear={marsYear}&sol={sols}&latitude={marsLat}&longitude={marsLong}&altitude={marsAlt}&zkey={altType}&spacecraft={spacecraft}&isfixedlt={localTimeIsFixed}&dust={dustScenario}&hrkey={isHighRes}&averaging={averagingType}&dpi={figureFormat}&islog={isLogValues}&colorm={colormapType}&minval={minValue}&maxval={maxValue}&proj={mapType}&palt={projAlt}&plon={projLong}&plat={projLat}&trans={transparency}&iswind={isWind}&latpoint={markerLat}&lonpoint={markerLong}'

print("Options Complete\nHere is your link:")
print(base_url)
print("\n\nOr your data\n")

response = requests.get(base_url)
data_url = r'https://www-mars.lmd.jussieu.fr/mcd_python'+response.text[response.text.find(r"/txt"):response.text.find(">Click")-1]
print(data_url)

data = requests.get(data_url, stream=True)
with open(f'mars data.txt',"wb") as file:
    for chunk in data.iter_content(chunk_size=8192):
        file.write(chunk)