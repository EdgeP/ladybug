# Photovoltaics surface
# By Djordje Spasic and Jason Sensibaugh
# djordjedspasic@gmail.com and sensij@yahoo.com
# Ladybug started by Mostapha Sadeghipour Roudsari is licensed
# under a Creative Commons Attribution-ShareAlike 3.0 Unported License.

"""
Use this component to calculate amount of electrical energy that can be produced by a surface
if a certain percentage of it is covered with Photovoltaics.
Component based on NREL PVWatts v1 fixed tilt calculator for crystalline silicon (c-Si) photovoltaics.

Sources:
http://www.nrel.gov/docs/fy14osti/60272.pdf
https://pvpmc.sandia.gov
-
Provided by Ladybug 0.0.59
    
    input:
        _PVsurface: - Input planar Surface (not a polysurface) on which the PV modules will be applied. If you have a polysurface, explode it (using "Deconstruct Brep" component) and then feed its Faces(F) output to _PVsurface. Surface normal should be faced towards the sun.
                    - Or input surface Area, in square meters (example: "100").
                    - Or input PV system size (nameplate DC power rating), in kiloWatts at standard test conditions (example: "4 kw").
        PVsurfacePercent_: The percentage of surface which will be used for PV modules (range 0-100).
                           -
                           If not supplied, default value of 100 (all surface area will be covered in PV modules) is used.
        PVsurfaceTiltAngle_: The angle from horizontal of the inclination of the PVsurface. Example: 0 = horizontal, 90 = vertical. (range 0-180)
                             -
                             If not supplied, but surface inputted into "_PVsurface", PVsurfaceTiltAngle will be calculated from an angle PVsurface closes with XY plane.
                             If not supplied, but surface NOT inputted into "_PVsurface" (instead, a surface area or system size inputed), location's latitude will be used as default value.
        PVsurfaceAzimuthAngle_: The orientation angle (clockwise from the true north) of the PVsurface normal vector. (range 0-360)
                                -
                                If not supplied, but surface inputted into "_PVsurface", PVsurfaceAzimuthAngle will be calculated from an angle PVsurface closes with its north.
                                If not supplied, but surface NOT inputted into "_PVsurface" (instead, a surface area or system size inputed), default value of 180° (south-facing) for locations in the northern hemisphere or 0° (north-facing) for locations in the southern hemisphere, will be used.
        moduleActiveAreaPercent_: Percentage of the module's area excluding module framing and gaps between cells. 
                                  -
                                  If not supplied, default value of 90(%) will be used.
        moduleType_: Module type and mounting configuration:
                    -
                    0 = Glass/cell/glass, Close (flush) roof mount (pv array mounted parallel and relatively close to the plane of the roof (between two and six inches))
                    1 = Glass/cell/polymer sheet, Insulated back (pv curtain wall, pv skylights)
                    2 = Glass/cell/polymer sheet, Open rack (ground mount array, flat/sloped roof array that is tilted, pole-mount solar panels, solar carports, solar canopies)
                    3 = Glass/cell/glass, Open rack (the same as upper "2" type, just with a glass on the back part of the module).
                    -
                    If not supplied, default type: "Glass/cell/glass, Close (flush) roof mount" (0) is used.
        moduleEfficiency_: The ratio of energy output from the PV module to input energy from the sun. It ranges from 0 to 100 (%).
                           Current typical module efficiencies for crystalline silicon modules range from 14-20%
                           -
                           If not defined, default value of 15(%) will be used.
        DCtoACderateFactor_: Factor which accounts for various locations and instances in a PV system where power is lost from DC system nameplate to AC power. It ranges from 0 to 1.
                                    It can be calculated with Ladybug's "DC to AC derate factor" component.
                                    -
                                    If not supplied, default value of 0.85 will be used.
        _location: Input data from Ladybug's "Import epw" "location" output, or create your own location data with Ladybug's "Construct Location" component
        _dryBulbTemperature: Hourly Dry Bulb Temperature (air temperature), in Celsius
        _windSpeed: Hourly Wind Speed, in meters/second
        _directNormalRadiation: Amount of solar radiation received directly from the solar disk on a surface perpendicular to the sun's rays, in Wh/m2
        _diffuseHorizontalRadiation: Amount of solar radiation received from the sky on a horizontal surface, in Wh/m2
        _modelYear: Input model year data from Ladybug's "Import epw" "modelYear" output.
        north_: Input a vector to be used as a true North direction, or a number between 0 and 360 that represents the clockwise degrees off from the Y-axis.
                -
                If not supplied, default North direction will be set to the Y-axis (0 degrees).
        albedo_: Average reflection coefficient of the area surrounding the PV surface. It ranges from 0 for very dark to 1 for bright white or metallic surface. Here are some specific values:
                 -
                 Dry asphalt  0.12
                 Wet Asphalt  0.18
                 Bare soil  0.17
                 Grass  0.20
                 Concrete  0.30
                 Granite  0.32
                 Dry sand  0.35
                 Copper  0.74
                 Wet snow  0.65
                 Fresh snow  0.82
                 Aluminum  0.85
                 -
                 If not supplied default value of 0.20 (Grass) will be used.
        annualHourlyData_: An optional list of hourly data from Ladybug's "Import epw" component (e.g. dryBulbTemperature), which will be used for "conditionalStatement_".
        conditionalStatement_: This input allows users to calculate the Photovoltaics surface component results only for those annualHourlyData_ values which fit specific conditions or criteria. To use this input correctly, hourly data, such as dryBulbTemperature or windSpeed, must be plugged into the "annualHourlyData_" input. The conditional statement input here should be a valid condition statement in Python, such as "a>25" or "b<3" (without the quotation marks).
                               conditionalStatement_ accepts "and" and "or" operators. To visualize the hourly data, English letters should be used as variables, and each letter alphabetically corresponds to each of the lists (in their respective order): "a" always represents the 1st list, "b" always represents the 2nd list, etc.
                               For example, if you have an hourly dryBulbTemperature connected as the first list, and windSpeed connected as the second list (both to the annualHourlyData_ input), and you want to plot the data for the time period when temperature is between 18°C and 23°C, and windSpeed is larger than 3m/s, the conditionalStatement_ should be written as "18<a<23 and b>3" (without the quotation marks).
        _runIt: ...
        
    output:
        readMe!: ...
        ACenergyPerHour: AC power output for each hour during a year, in kWh
        ACenergyPerMonth: Total AC power output for each month, in kWh
        ACenergyPerYear: Total AC power output for a whole year, in kWh
        beamRadiationPerHour: Beam (direct) POA (Plane of array) irradiance for each hour during a year, in kWh/m2
        diffuseRadiationPerHour: Diffuse POA (Plane of array) irradiance for each hour during a year, in kWh/m2
        reflectedRadiationPerHour: Ground reflected POA (Plane of array) irradiance for each hour during a year, in kWh/m2
        totalRadiationPerHour: Total Incident POA (Plane of array) irradiance for each hour during a year, in kWh/m2
        totalRadiationPerMonth: Total Incident POA (Plane of array) irradiance for each month, in kWh/m2
        totalRadiationPerYear: Total Incident POA (Plane of array) irradiance for a whole year, in kWh/m2
        averageDailyRadiationPerMonth: An average incident POA (Plane of array) irradiance per day in each month, in kWh/m2/day
        averageDailyRadiationPerYear: An average incident POA (Plane of array) irradiance per day in a whole year, in kWh/m2/day
        moduleTemperaturePerHour: Module temperature for each hour during year, in °C
        cellTemperaturePerHour: Cell temperature for each hour during year, in °C
        nameplateDCpowerRating: DC rating or system size. In kW
        surfaceArea: Total area of the inputted _PVsurface. In m2
        surfaceActiveArea: Total active area of the inputted _PVsurface. Active area being the _PVsurface area excluding module framing and gaps between cells. In m2
"""

ghenv.Component.Name = "Ladybug_Photovoltaics Surface"
ghenv.Component.NickName = "PhotovoltaicsSurface"
ghenv.Component.Message = "VER 0.0.59\nMAY_26_2015"
ghenv.Component.Category = "Ladybug"
ghenv.Component.SubCategory = "7 | WIP"
#compatibleLBVersion = VER 0.0.59\nMAY_26_2015
try: ghenv.Component.AdditionalHelpFromDocStrings = "1"
except: pass

import Grasshopper.Kernel as gh
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import math
import re


def getLocationData(location):
    
    if location:
        try:
            locationName, latitude, longitude, timeZone, elevation = lb_preparation.decomposeLocation(location)
            validLocationData = True
            printMsg = "ok"
        
        except Exception, e:
            # something is wrong with "_location" input (the input is not from Ladybug 'Import epw' component 'location' ouput)
            latitude = longitude = timeZone = elevation = locationName = None
            validLocationData = False
            printMsg = "Something is wrong with \"_location\" input."
    else:
        latitude = longitude = timeZone = elevation = locationName = None
        validLocationData = False
        printMsg = "Please input \"location\" output from Ladybug \"Import epw\" component."
    
    return latitude, longitude, timeZone, elevation, locationName, validLocationData, printMsg


def PVsurfaceInputData(PVsurface, PVsurfacePercent, unitAreaConversionFactor, DCtoACderateFactor, moduleActiveAreaPercent, moduleType, moduleEfficiency):
    
    if (PVsurface == None):
        PVsurfaceInputType = nameplateDCpowerRating = srfArea = activeArea = PVsurfacePercent = DCtoACderateFactor = moduleActiveAreaPercent = moduleType = moduleEfficiency = None
        validPVsurfaceData = False
        printMsg = "Please input Surface (not polysurface) to \"_PVsurface\".\nOr input surface Area in square meters (example: \"100\").\nOr input Nameplate DC power rating in kiloWatts (example: \"4 kw\")."
        
        return PVsurfaceInputType, nameplateDCpowerRating, srfArea, activeArea, PVsurfacePercent, DCtoACderateFactor, moduleActiveAreaPercent, moduleType, moduleEfficiency, validPVsurfaceData, printMsg
    
    if (PVsurfacePercent == None) or (PVsurfacePercent < 0) or (PVsurfacePercent > 100):
        PVsurfacePercent = 100  # default value 100%
    
    if (DCtoACderateFactor == None) or (DCtoACderateFactor < 0) or (DCtoACderateFactor > 1):
        DCtoACderateFactor = 0.85  # default value (corresponds to 11.42% of PVWatts v5 Total Losses)
    
    if (moduleActiveAreaPercent == None) or (moduleActiveAreaPercent < 0) or (moduleActiveAreaPercent > 100):
        moduleActiveAreaPercent = 90  # default value in %
    
    if (moduleType == None) or (moduleType < 0) or (moduleType > 3):
        moduleType = 0  # Glass/cell/glass, Close (flush) roof mount
    
    if (moduleEfficiency == None) or (moduleEfficiency < 0) or (moduleEfficiency > 100):
        moduleEfficiency = 15  # for crystalline silicon
    
    # check PVsurface input
    obj = rs.coercegeometry(PVsurface)
    
    # input is surface
    if isinstance(obj,Rhino.Geometry.Brep):
        PVsurfaceInputType = "brep"
        facesCount = obj.Faces.Count
        if facesCount > 1:
            # inputted polysurface
            PVsurfaceInputType = nameplateDCpowerRating = srfArea = activeArea = PVsurfacePercent = DCtoACderateFactor = moduleActiveAreaPercent = moduleType = moduleEfficiency = None
            validPVsurfaceData = False
            printMsg = "The brep you supplied to \"_PVsurface\" is a polysurface. Please supply a surface"
            
            return PVsurfaceInputType, nameplateDCpowerRating, srfArea, activeArea, PVsurfacePercent, DCtoACderateFactor, moduleActiveAreaPercent, moduleType, moduleEfficiency, validPVsurfaceData, printMsg
        else:
            # inputted brep with a single surface
            srfArea = Rhino.Geometry.AreaMassProperties.Compute(obj).Area * (PVsurfacePercent/100)  # in m2
            srfArea = srfArea * unitAreaConversionFactor  # in m2
            activeArea = srfArea * (moduleActiveAreaPercent/100)  # in m2
            nameplateDCpowerRating = activeArea * (1 * (moduleEfficiency/100))  # in kW
            validPVsurfaceData = True
            printMsg = "ok"
            
            return PVsurfaceInputType, nameplateDCpowerRating, srfArea, activeArea, PVsurfacePercent, DCtoACderateFactor, moduleActiveAreaPercent, moduleType, moduleEfficiency, validPVsurfaceData, printMsg
    else:
        PVsurfaceInputType = "number"
        try:
            # input is number (pv surface area in m2)
            srfArea = float(PVsurface) * (PVsurfacePercent/100)  # in m2
            srfArea = srfArea * unitAreaConversionFactor  # in m2
            activeArea = srfArea * (moduleActiveAreaPercent/100)  # in m2
            nameplateDCpowerRating = activeArea * (1 * (moduleEfficiency/100))  # in kW
            validPVsurfaceData = True
            printMsg = "ok"
            
            return PVsurfaceInputType, nameplateDCpowerRating, srfArea, activeArea, PVsurfacePercent, DCtoACderateFactor, moduleActiveAreaPercent, moduleType, moduleEfficiency, validPVsurfaceData, printMsg
        except Exception, e:
            pass
        
        # input is string (nameplateDCpowerRating in kW)
        lowerString = PVsurface.lower()
        
        if "kw" in lowerString:
            nameplateDCpowerRating = float(lowerString.replace("kw","")) * (PVsurfacePercent/100)  # in kW
            activeArea = nameplateDCpowerRating / (1 * (moduleEfficiency/100))  # in m2
            srfArea = activeArea * (100/moduleActiveAreaPercent)  # in m2
            validPVsurfaceData = True
            printMsg = "ok"
            
            return PVsurfaceInputType, nameplateDCpowerRating, srfArea, activeArea, PVsurfacePercent, DCtoACderateFactor, moduleActiveAreaPercent, moduleType, moduleEfficiency, validPVsurfaceData, printMsg
        else:
            PVsurfaceInputType = nameplateDCpowerRating = srfArea = activeArea = PVsurfacePercent = DCtoACderateFactor = moduleActiveAreaPercent = moduleType = moduleEfficiency = None
            validPVsurfaceData = False
            printMsg = "Something is wrong with your \"PVsurface\" input data"
            
            return PVsurfaceInputType, nameplateDCpowerRating, srfArea, activeArea, PVsurfacePercent, DCtoACderateFactor, moduleActiveAreaPercent, moduleType, moduleEfficiency, validPVsurfaceData, printMsg


def getWeatherData(dryBulbTemperature, windSpeed, directNormalRadiation, diffuseHorizontalRadiation, modelYear, albedo):
    
    if (len(dryBulbTemperature) == 0) or (dryBulbTemperature[0] is ""):
        Ta = ws = DNI = DHI = yearsHOY = monthsHOY = daysHOY = hoursHOY = HOYs = albedo = None
        validWeatherData = False
        printMsg = "Please input \"_dryBulbTemperature\" from Ladybug \"Import epw\" component."
        return Ta, ws, DNI, DHI, yearsHOY, monthsHOY, daysHOY, hoursHOY, HOYs, albedo, validWeatherData, printMsg
    if (len(windSpeed) == 0) or (windSpeed[0] is ""):
        Ta = ws = DNI = DHI = yearsHOY = monthsHOY = daysHOY = hoursHOY = HOYs = albedo = None
        validWeatherData = False
        printMsg = "Please input \"_windSpeed\" from Ladybug \"Import epw\" component."
        return Ta, ws, DNI, DHI, yearsHOY, monthsHOY, daysHOY, hoursHOY, HOYs, albedo, validWeatherData, printMsg
    if (len(directNormalRadiation) == 0) or (directNormalRadiation[0] is ""):
        Ta = ws = DNI = DHI = yearsHOY = monthsHOY = daysHOY = hoursHOY = HOYs = albedo = None
        validWeatherData = False
        printMsg = "Please input \"_directNormalRadiation\" from Ladybug \"Import epw\" component."
        return Ta, ws, DNI, DHI, yearsHOY, monthsHOY, daysHOY, hoursHOY, HOYs, albedo, validWeatherData, printMsg
    if (len(diffuseHorizontalRadiation) == 0) or (diffuseHorizontalRadiation[0] is ""):
        Ta = ws = DNI = DHI = yearsHOY = monthsHOY = daysHOY = hoursHOY = HOYs = albedo = None
        validWeatherData = False
        printMsg = "Please input \"_diffuseHorizontalRadiation\" from Ladybug \"Import epw\" component."
        return Ta, ws, DNI, DHI, yearsHOY, monthsHOY, daysHOY, hoursHOY, HOYs, albedo, validWeatherData, printMsg
    if (len(modelYear) == 0) or (modelYear[0] is ""):
        Ta = ws = DNI = DHI = yearsHOY = monthsHOY = daysHOY = hoursHOY = HOYs = albedo = None
        validWeatherData = False
        printMsg = "Please input \"_modelYear\" from Ladybug \"Import epw\" component."
        return Ta, ws, DNI, DHI, yearsHOY, monthsHOY, daysHOY, hoursHOY, HOYs, albedo, validWeatherData, printMsg
    if (albedo == None) or (albedo < 0) or (albedo > 1):
        albedo = 0.2  # default
    
    if len(dryBulbTemperature) == 8767:
        Ta = dryBulbTemperature[7:]
    elif len(dryBulbTemperature) == 8760:
        Ta = dryBulbTemperature
    if len(windSpeed) == 8767:
        ws = windSpeed[7:]
    elif len(windSpeed) == 8760:
        ws = windSpeed
    if len(directNormalRadiation) == 8767:
        DNI = directNormalRadiation[7:]
    elif len(directNormalRadiation) == 8760:
        DNI = directNormalRadiation
    if len(diffuseHorizontalRadiation) == 8767:
        DHI = diffuseHorizontalRadiation[7:]
    elif len(diffuseHorizontalRadiation) == 8760:
        DHI = diffuseHorizontalRadiation
    if len(modelYear) == 8767:
        yearsHOY = modelYear[7:]
    elif len(modelYear) == 8760:
        yearsHOY = modelYear
    
    monthsHOY = [1 for i in range(744)] + [2 for i in range(672)] + [3 for i in range(744)] + [4 for i in range(720)] + [5 for i in range(744)] + [6 for i in range(720)] + [7 for i in range(744)] + [8 for i in range(744)] + [9 for i in range(720)] + [10 for i in range(744)] + [11 for i in range(720)] + [12 for i in range(744)]
    
    numberOfDaysMonth = [31,28,31,30,31,30,31,31,30,31,30,31]
    daysHOY = []
    day = 1
    for i,item in enumerate(numberOfDaysMonth):
        for k in range(item):
            for g in range(24):
                daysHOY.append(day)
            day += 1
        day = 1
    
    hoursHOY = []
    hour = 1
    for i in range(365):
        for k in range(24):
            hoursHOY.append(hour)
            hour += 1
        hour = 1
    
    HOYs = range(1,8761)
    
    validWeatherData = True
    printMsg = "ok"
    
    return Ta, ws, DNI, DHI, yearsHOY, monthsHOY, daysHOY, hoursHOY, HOYs, albedo, validWeatherData, printMsg


def checkAnnualHourlyInputData(annualHourlyData):
    
    if annualHourlyData == []:
        annualHourlyDataLists = []
        annualHourlyDataListsEpwNames = []
        validAnnualHourlyData = True
        printMsg = "ok"
        return validAnnualHourlyData, annualHourlyDataLists, annualHourlyDataListsEpwNames, printMsg
    elif len(annualHourlyData) % 8767 != 0:
        annualHourlyDataLists = annualHourlyDataListsEpwNames = None
        validAnnualHourlyData = False
        printMsg = "Your annualHourlyData_ input is not correct. Please input complete 8767 items long list(s) from \"Ladybug_Import epw\" component"
        return annualHourlyDataLists, validAnnualHourlyData, annualHourlyDataListsEpwNames, printMsg
    else:
        annualHourlyDataLists = []
        annualHourlyDataListsEpwNames = []
        startIndex = 0
        endIndex = 8767
        for i in range(int(len(annualHourlyData)/8767)):
            untrimmedList = annualHourlyData[startIndex:endIndex]
            trimmedList = untrimmedList[7:]
            annualHourlyDataListsName = untrimmedList[2]
            annualHourlyDataLists.append(trimmedList)
            annualHourlyDataListsEpwNames.append(annualHourlyDataListsName)
            startIndex += 8767
            endIndex += 8767
        
        validAnnualHourlyData = True
        printMsg = "ok"
        return validAnnualHourlyData, annualHourlyDataLists, annualHourlyDataListsEpwNames, printMsg


def checkConditionalStatement(conditionalStatement, annualHourlyDataLists, annualHourlyDataListsEpwNames, weatherPerHourDataSubLists, addZero):
    
    if conditionalStatement == None and len(annualHourlyDataLists) > 0: # conditionalStatement_ not inputted, annualHourlyData_ inputted
        validConditionalStatement = False
        weatherPerHourDataConditionalStatementSubLists = conditionalStatementForFinalPrint = None
        printMsg = "Please supply \"conditionalStatement_\" for inputted \"annualHourlyData_\" data."
        return validConditionalStatement, weatherPerHourDataConditionalStatementSubLists, conditionalStatementForFinalPrint, printMsg
    elif conditionalStatement == None and len(annualHourlyDataLists) == 0:  # conditionalStatement_ not inputted, annualHourlyData_ not inputted
        conditionalStatement = "True"
    else:  # conditionalStatement_ inputted, annualHourlyData_ not
        if annualHourlyDataLists == []:
            validConditionalStatement = False
            weatherPerHourDataConditionalStatementSubLists = conditionalStatementForFinalPrint = None
            printMsg = "Please supply \"annualHourlyData_\" data for inputted \"conditionalStatement_\"."
            return validConditionalStatement, weatherPerHourDataConditionalStatementSubLists, conditionalStatementForFinalPrint, printMsg
        else:  # both conditionalStatement_ and annualHourlyData_ inputted
            conditionalStatement = conditionalStatement.lower()
            conditionalStatement = re.sub(r"\b([a-z])\b", r"\1[i]", conditionalStatement)
    
    annualHourlyDataListsNames = map(chr, range(97, 123))
    
    # finalPrint conditonal statements for "printOutput" function
    if conditionalStatement != "True":  # conditionalStatement_ not inputted
        # replace conditionalStatement annualHourlyDataListsNames[i] names with annualHourlyDataListsEpwNames:
        conditionalStatementForFinalPrint = conditionalStatement[:]
        for i in range(len(annualHourlyDataLists)):
            conditionalStatementForFinalPrint = conditionalStatementForFinalPrint.replace(annualHourlyDataListsNames[i]+"[i]", annualHourlyDataListsEpwNames[i])
    else:
        conditionalStatementForFinalPrint = "No condition"
    
    annualHourlyDataListsNames = map(chr, range(97, 123))
    numberOfLetters = 0
    
    for letter in annualHourlyDataListsNames:
        changedLetter = letter+"[i]"
        if changedLetter in conditionalStatement:
            numberOfLetters += 1
    if numberOfLetters != len(annualHourlyDataLists):
        validConditionalStatement = False
        weatherPerHourDataConditionalStatementSubLists = conditionalStatementForFinalPrint = None
        printMsg = "The number of a,b,c... variables you supplied in \"conditionalStatement_\" does not correspond to the number of \"annualHourlyData_\" lists you inputted. Please make the numbers of these two equal."
        return validConditionalStatement, weatherPerHourDataConditionalStatementSubLists, conditionalStatementForFinalPrint, printMsg
    else:
        for i in range(len(annualHourlyDataLists)):
            exec("%s = %s" % (annualHourlyDataListsNames[i],annualHourlyDataLists[i]))
        
        try:
            weatherPerHourDataConditionalStatementSubLists = []
            for i in range(len(weatherPerHourDataSubLists)):
                weatherPerHourDataConditionalStatementSubLists.append([])
            for i in range(len(weatherPerHourDataSubLists[0])):
                exec("conditionalSt = %s" % conditionalStatement)
                if addZero == True:  # add 0 if conditionalStatement == False
                    if conditionalSt:
                        for k in range(len(weatherPerHourDataConditionalStatementSubLists)):
                            weatherPerHourDataConditionalStatementSubLists[k].append(weatherPerHourDataSubLists[k][i])
                    else:
                        for k in range(len(weatherPerHourDataConditionalStatementSubLists)):
                            weatherPerHourDataConditionalStatementSubLists[k].append(0)
                else:  # skip the value
                    if conditionalSt:
                        for k in range(len(weatherPerHourDataConditionalStatementSubLists)):
                            weatherPerHourDataConditionalStatementSubLists[k].append(weatherPerHourDataSubLists[k][i])
        except Exception, e:
            validConditionalStatement = False
            weatherPerHourDataConditionalStatementSubLists = conditionalStatementForFinalPrint = None
            printMsg = "Your \"conditionalStatement_\" is incorrect. Please provide a valid conditional statement in Python, such as \"a>25 and b<80\" (without the quotation marks)"
            return validConditionalStatement, weatherPerHourDataConditionalStatementSubLists, conditionalStatementForFinalPrint, printMsg
        
        if len(weatherPerHourDataConditionalStatementSubLists[0]) == 0:
            validConditionalStatement = False
            weatherPerHourDataConditionalStatementSubLists = conditionalStatementForFinalPrint = None
            printMsg = "No \"annualHourlyData_\" coresponds to \"conditionalStatement_\". Please edit your \"conditionalStatement_\""
            return validConditionalStatement, weatherPerHourDataConditionalStatementSubLists, conditionalStatementForFinalPrint, printMsg
        else:
            validConditionalStatement = True
            printMsg = "ok"
            return validConditionalStatement, weatherPerHourDataConditionalStatementSubLists, conditionalStatementForFinalPrint, printMsg


def srfAzimuthAngle(PVsurfaceAzimuthAngle, PVsurfaceInputType, PVsurface, latitude):
    
    # always use "PVsurfaceAzimuthAngle" input, even in case surface has been inputted into the "_PVsurface" input
    if (PVsurfaceAzimuthAngle != None):
        if (PVsurfaceAzimuthAngle < 0) or (PVsurfaceAzimuthAngle > 360):
            if latitude > 0:
                srfAzimuthD = 180  # equator facing for northern hemisphere
            elif latitude < 0:
                srfAzimuthD = 0  # equator facing for southern hemisphere
        else:
            srfAzimuthD = PVsurfaceAzimuthAngle
        surfaceTiltDCalculated = "needs to be calculated"
    
    # nothing inputted into "PVsurfaceAzimuthAngle_" input, calculate the PVsurfaceAzimuthAngle from inputted "_PVsurface" surface
    elif (PVsurfaceAzimuthAngle == None):
        if PVsurfaceInputType == "brep":
            srfAzimuthD, surfaceTiltDCalculated = lb_photovoltaics.srfAzimuthAngle(PVsurface)
            if surfaceTiltDCalculated == None:
                surfaceTiltDCalculated = "needs to be calculated"
        
        # nothing inputted into "PVsurfaceAzimuthAngle_" input, use south orientation (180 for + latitude locations, 0 for - latitude locations)
        elif PVsurfaceInputType == "number":
            if latitude > 0:
                srfAzimuthD = 180  # equator facing for northern hemisphere
            elif latitude < 0:
                srfAzimuthD = 0  # equator facing for southern hemisphere
            surfaceTiltDCalculated = "needs to be calculated"
    
    return srfAzimuthD, surfaceTiltDCalculated


def srfTiltAngle(PVsurfaceTiltAngle, surfaceTiltDCalculated, PVsurfaceInputType, PVsurface, latitude):
    
    # always use "PVsurfaceTiltAngle" input, even in case surface has been inputted into the "_PVsurface" input
    if (PVsurfaceTiltAngle != None):
        
        if (PVsurfaceTiltAngle < 0):
            srfTiltD = 0
        elif (PVsurfaceTiltAngle > 180):
            srfTiltD = 0
        else:
            srfTiltD = PVsurfaceTiltAngle
    
    # nothing inputted into "PVsurfaceTiltAngle_" input, calculate the PVsurfaceTiltAngle from inputted "_PVsurface" surface
    elif (PVsurfaceTiltAngle == None):
        
        # check if srfTildD hasn't already been calculated at srfAzimuthAngle() function
        if (surfaceTiltDCalculated == 0) or (surfaceTiltDCalculated == 90) or (surfaceTiltDCalculated == 180):
            srfTiltD = surfaceTiltDCalculated
        elif surfaceTiltDCalculated == "needs to be calculated":
            if PVsurfaceInputType == "brep":
                srfTiltD = lb_photovoltaics.srfTiltAngle(PVsurface)
            # nothing inputted into "PVsurfaceTiltAngle_" input, use site abs(latitude) for PVsurfaceTiltAngle
            elif PVsurfaceInputType == "number":
                srfTiltD = abs(latitude)
    
    return srfTiltD


def angle2northClockwise(north):
    # temporary function, until "Sunpath" class from Labybug_ladbybug.py starts calculating sun positions counterclockwise
    try:
        northVec =Rhino.Geometry.Vector3d.YAxis
        northVec.Rotate(-math.radians(float(north)),Rhino.Geometry.Vector3d.ZAxis)
        northVec.Unitize()
        return 2*math.pi-math.radians(float(north)), northVec
    except Exception, e:
        try:
            northVec =Rhino.Geometry.Vector3d(north)
            northVec.Unitize()
            return Rhino.Geometry.Vector3d.VectorAngle(Rhino.Geometry.Vector3d.YAxis, northVec, Rhino.Geometry.Plane.WorldXY), northVec
        except Exception, e:
            return 0, Rhino.Geometry.Vector3d.YAxis


def correctSrfAzimuthDforNorth(north, srfAzimuthD):
    # nothing inputted in "north_" - use default value: 0
    if north == None:
        northDeg = 0  # default
        correctedSrfAzimuthD = srfAzimuthD
        validNorth = True
        printMsg = "ok"
    else:
        try:  # check if it's a number
            north = float(north)
            if north < 0 or north > 360:
                correctedSrfAzimuthD = northDeg = None
                validNorth = False
                printMsg = "Please input north angle value from 0 to 360."
                return correctedSrfAzimuthD, validNorth, printMsg
        except Exception, e:  # check if it's a vector
            north.Unitize()
        
        northRad, northVec = angle2northClockwise(north)
        northDeg = 360-math.degrees(northRad)
        correctedSrfAzimuthD = northDeg + srfAzimuthD
        if correctedSrfAzimuthD > 360:
            correctedSrfAzimuthD = correctedSrfAzimuthD - 360
        validNorth = True
        printMsg = "ok"
    
    return correctedSrfAzimuthD, northDeg, validNorth, printMsg


def radiation_ACenergy(latitude, longitude, timeZone, locationName, years, months, days, hours, HOYs, nameplateDCpowerRating, DCtoACderateFactor, srfArea, srfTiltD, srfAzimuthD, moduleType, moduleEfficiency, dryBulbTemperature, windSpeed, directNormalRadiation, diffuseHorizontalRadiation, albedo):
    # solar radiation, AC power output, energy value, module temperature, cell temperature
    ACenergyPerHour = ["key:location/dataType/units/frequency/startsAt/endsAt", locationName, "AC power output", "kWh", "Hourly", (1, 1, 1), (12, 31, 24)]
    totalRadiationPerHour = ["key:location/dataType/units/frequency/startsAt/endsAt", locationName, "Total POA irradiance", "kWh/m2", "Hourly", (1, 1, 1), (12, 31, 24)]
    beamRadiationPerHour = ["key:location/dataType/units/frequency/startsAt/endsAt", locationName, "POA beam irradiance", "kWh/m2", "Hourly", (1, 1, 1), (12, 31, 24)]
    diffuseRadiationPerHour = ["key:location/dataType/units/frequency/startsAt/endsAt", locationName, "POA diffuse irradiance", "kWh/m2", "Hourly", (1, 1, 1), (12, 31, 24)]
    reflectedRadiationPerHour = ["key:location/dataType/units/frequency/startsAt/endsAt", locationName, "POA ground reflected irradiance", "kWh/m2", "Hourly", (1, 1, 1), (12, 31, 24)]
    moduleTemperaturePerHour = ["key:location/dataType/units/frequency/startsAt/endsAt", locationName, "Module temperature", "°C", "Hourly", (1, 1, 1), (12, 31, 24)]
    cellTemperaturePerHour = ["key:location/dataType/units/frequency/startsAt/endsAt", locationName, "Cell temperature", "°C", "Hourly", (1, 1, 1), (12, 31, 24)]
    hoyForMonths = [0, 744, 1416, 2160, 2880, 3624, 4344, 5088, 5832, 6552, 7296, 8016, 8760, 9000]
    numberOfDaysInThatMonth = [31,28,31,30,31,30,31,31,30,31,30,31]
    monthsOfYearHoyEpoa = [[],[],[],[],[],[],[],[],[],[],[],[]]
    monthsOfYearHoyPac = [[],[],[],[],[],[],[],[],[],[],[],[]]
    averageDailyRadiationPerMonth = []
    for i,hoy in enumerate(HOYs):
        sunZenithD, sunAzimuthD, sunAltitudeD = lb_photovoltaics.NRELsunPosition(latitude, longitude, timeZone, years[i], months[i], days[i], hours[i]-1)
        Epoa, Eb, Ed_sky, Eground, AOI_R = lb_photovoltaics.POAirradiance(sunZenithD, sunAzimuthD, srfTiltD, srfAzimuthD, directNormalRadiation[i], diffuseHorizontalRadiation[i], albedo)
        Tm, Tcell, Pac = lb_photovoltaics.pvwatts(nameplateDCpowerRating, DCtoACderateFactor, AOI_R, Epoa, Eb, Ed_sky, Eground, moduleType, dryBulbTemperature[i], windSpeed[i], directNormalRadiation[i], diffuseHorizontalRadiation[i])
        Epoa = Epoa/1000 # to kWh/m2
        Eb = Eb/1000 # to kWh/m2
        Ed_sky = Ed_sky/1000 # to kWh/m2
        Eground = Eground/1000 # to kWh/m2
        ACenergyPerHour.append(Pac)
        totalRadiationPerHour.append(Epoa)
        beamRadiationPerHour.append(Eb)
        diffuseRadiationPerHour.append(Ed_sky)
        reflectedRadiationPerHour.append(Eground)
        moduleTemperaturePerHour.append(Tm)
        cellTemperaturePerHour.append(Tcell)
        for k,item in enumerate(hoyForMonths):
            if hoy >= hoyForMonths[k]+1 and hoy <= hoyForMonths[k+1]:
                monthsOfYearHoyEpoa[k].append(Epoa)
                monthsOfYearHoyPac[k].append(Pac)
    
    monthsOfYearSumEpoa = [sum(monthEpoa) for monthEpoa in monthsOfYearHoyEpoa]  # in kWh/m2
    sumEpoaPerYear = sum(monthsOfYearSumEpoa)  # in kWh/m2
    for g,sumMonthEpoa in enumerate(monthsOfYearSumEpoa):
        MonthPoa = (sumMonthEpoa)/numberOfDaysInThatMonth[g]
        averageDailyRadiationPerMonth.append(MonthPoa)  # in kWh/m2/day
    
    averageDailyRadiationPerYear = sum(averageDailyRadiationPerMonth)/12  # in kWh/m2/day
    
    ACenergyPerMonth = [sum(monthPac) for monthPac in monthsOfYearHoyPac]  # in kWh
    ACenergyPerYear = sum(ACenergyPerMonth)  # in kWh
    
    
    return ACenergyPerHour, ACenergyPerMonth, ACenergyPerYear, beamRadiationPerHour, diffuseRadiationPerHour, reflectedRadiationPerHour, totalRadiationPerHour, monthsOfYearSumEpoa, sumEpoaPerYear, averageDailyRadiationPerMonth, averageDailyRadiationPerYear, moduleTemperaturePerHour, cellTemperaturePerHour


def printOutput(unitAreaConversionFactor, north, latitude, longitude, timeZone, elevation, locationName, albedo, nameplateDCpowerRating, srfArea, activeArea, PVsurfacePercent, DCtoACderateFactor, srfTiltD, srfAzimuthD, moduleActiveAreaPercent, moduleType, moduleEfficiency, conditionalStatementForFinalPrint):
    moduleTypesL = ["Glass/cell/glass Close (flush) roof mount", "Glass/cell/polymer sheet Insulated back", "Glass/cell/polymer sheet Open rack", "Glass/cell/glass Open rack"]
    model = moduleTypesL[moduleType]
    resultsCompletedMsg = "PVsurface component results successfully completed!"
    printOutputMsg = \
    """
Input data:

Location: %s
Latitude: %s
Longitude: %s
Time zone: %s
Elevation: %s
North: %s
Albedo: %s

Surface percentage used for PV modules: %0.2f
Active area Percentage: %0.2f
Surface area (m2): %0.2f
Surface active area (m2): %0.2f
Nameplate DC power rating (kW): %0.2f
Overall DC to AC derate factor: %0.3f
Module type and mounting: %s
Module efficiency: %s
Array type: fixed tilt
Surface azimuth angle: %0.2f
Surface tilt angle: %0.2f

Caclulation based on the following condition:
%s
    """ % (locationName, latitude, longitude, timeZone, elevation, north, albedo, PVsurfacePercent, moduleActiveAreaPercent, srfArea, activeArea, nameplateDCpowerRating, DCtoACderateFactor, model, moduleEfficiency, srfAzimuthD, srfTiltD, conditionalStatementForFinalPrint)
    print resultsCompletedMsg
    print printOutputMsg


level = gh.GH_RuntimeMessageLevel.Warning
if sc.sticky.has_key("ladybug_release"):
    if sc.sticky["ladybug_release"].isCompatible(ghenv.Component):
        lb_preparation = sc.sticky["ladybug_Preparation"]()
        lb_photovoltaics = sc.sticky["ladybug_Photovoltaics"]()
        
        if _PVsurface:
            unitConversionFactor = lb_preparation.checkUnits()
            unitAreaConversionFactor = unitConversionFactor**2
            PVsurfaceInputType, nameplateDCpowerRating, srfArea, activeArea, PVsurfacePercent, DCtoACderateFactor, moduleActiveAreaPercent, moduleType, moduleEfficiency, validPVsurfaceData, printMsg = PVsurfaceInputData(_PVsurface, PVsurfacePercent_, unitAreaConversionFactor, DCtoACderateFactor_, moduleActiveAreaPercent_, moduleType_, moduleEfficiency_)
            if validPVsurfaceData:
                latitude, longitude, timeZone, elevation, locationName, validLocationData, printMsg = getLocationData(_location)
                if validLocationData:
                    dryBulbTemperature, windSpeed, directNormalRadiation, diffuseHorizontalRadiation, years, months, days, hours, HOYs, albedo, validWeatherData, printMsg = getWeatherData(_dryBulbTemperature, _windSpeed, _directNormalRadiation, _diffuseHorizontalRadiation, _modelYear, albedo_)
                    if validWeatherData:
                        validAnnualHourlyData, annualHourlyDataLists, annualHourlyDataListsEpwNames, printMsg = checkAnnualHourlyInputData(annualHourlyData_)
                        if validAnnualHourlyData:
                            validConditionalStatement, weatherPerHourDataConditionalStatementSubLists, conditionalStatementForFinalPrint, printMsg = checkConditionalStatement(conditionalStatement_, annualHourlyDataLists, annualHourlyDataListsEpwNames, [dryBulbTemperature, windSpeed, directNormalRadiation, diffuseHorizontalRadiation], True)
                            if validConditionalStatement:
                                dryBulbTemperatureCondStat, windSpeedCondStat, directNormalRadiationCondStat, diffuseHorizontalRadiationCondStat = weatherPerHourDataConditionalStatementSubLists
                                # all inputs ok
                                if _runIt:
                                    srfAzimuthD, surfaceTiltDCalculated = srfAzimuthAngle(PVsurfaceAzimuthAngle_, PVsurfaceInputType, _PVsurface, latitude)
                                    correctedSrfAzimuthD, northDeg, validNorth, printMsg = correctSrfAzimuthDforNorth(north_, srfAzimuthD)
                                    srfTiltD = srfTiltAngle(PVsurfaceTiltAngle_, surfaceTiltDCalculated, PVsurfaceInputType, _PVsurface, latitude)
                                    ACenergyPerHour, ACenergyPerMonth, ACenergyPerYear, beamRadiationPerHour, diffuseRadiationPerHour, reflectedRadiationPerHour, totalRadiationPerHour, totalRadiationPerMonth, totalRadiationPerYear, averageDailyRadiationPerMonth, averageDailyRadiationPerYear, moduleTemperaturePerHour, cellTemperaturePerHour = radiation_ACenergy(latitude, longitude, timeZone, locationName, years, months, days, hours, HOYs, nameplateDCpowerRating, DCtoACderateFactor, srfArea, srfTiltD, correctedSrfAzimuthD, moduleType, moduleEfficiency, dryBulbTemperatureCondStat, windSpeedCondStat, directNormalRadiationCondStat, diffuseHorizontalRadiationCondStat, albedo)
                                    printOutput(unitAreaConversionFactor, northDeg, latitude, longitude, timeZone, elevation, locationName, albedo, nameplateDCpowerRating, srfArea, activeArea, PVsurfacePercent, DCtoACderateFactor, srfTiltD, correctedSrfAzimuthD, moduleActiveAreaPercent, moduleType, moduleEfficiency, conditionalStatementForFinalPrint)
                                    surfaceArea = srfArea; surfaceActiveArea = activeArea
                                else:
                                    print "All inputs are ok. Please set the \"_runIt\" to True, in order to run the Photovoltaics surface component"
                            else:
                                print printMsg
                                ghenv.Component.AddRuntimeMessage(level, printMsg)
                        else:
                            print printMsg
                            ghenv.Component.AddRuntimeMessage(level, printMsg)
                    else:
                        print printMsg
                        ghenv.Component.AddRuntimeMessage(level, printMsg)
                else:
                    print printMsg
                    ghenv.Component.AddRuntimeMessage(level, printMsg)
            else:
                print printMsg
                ghenv.Component.AddRuntimeMessage(level, printMsg)
        else:
            printMsg = "Please input a Surface (not a polysurface) to \"_PVsurface\".\nOr input surface Area in square meters (example: \"100\").\nOr input Nameplate DC power rating in kiloWatts (example: \"4 kw\")."
            print printMsg
            ghenv.Component.AddRuntimeMessage(level, printMsg)
    else:
        printMsg = "You need a newer version of Ladybug to use this component." + \
            "Use updateLadybug component to update userObjects.\n" + \
            "If you have already updated userObjects drag the Ladybug_Ladybug component " + \
            "into the canvas and try again."
        print printMsg
        ghenv.Component.AddRuntimeMessage(level, printMsg)
else:
    printMsg = "First please let the Ladybug fly..."
    print printMsg
    ghenv.Component.AddRuntimeMessage(level, printMsg)
