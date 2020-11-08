
flexcode = """
TITLE 'DesignProject'     { the problem identification }
COORDINATES cartesian2  { coordinate system, 1D,2D,3D, etc }
SELECT
ngrid = 19
VARIABLES        { system variables }
  Temp(threshold=0.1)
DEFINITIONS

tfinal = 1800
h=20
k
cp
rho
initTemp
initTempCube = %s
Thickness=-1
Surroundings=40

qdot = -k*grad(Temp)
INITIAL VALUES
Temp = initTemp
EQUATIONS        { PDE's, one for each variable }
rho*cp*dt(Temp) - div(k*grad(Temp))=0
BOUNDARIES       { The domain definition }
	

		region 'can filled with water'
		k = 0.6
		cp = 4200
		rho = 1000
		initTemp = 4
		Surroundings=40
		START (0,0) !Left side
		LINE TO (0,12) !top side 
		load (temp)=h*(Temp-Surroundings)
		LINE TO (6.5,12)!right side
		load(temp)=0
		LINE TO (6.5, 0) !bottom side
		load(temp)=0
		LINE TO CLOSE

	region 'Aluminium coated ice cube'
		k = 205
		cp = 895
		rho = 2720
		initTemp = initTempCube
		START (0,0) 
		LINE TO (6.5,0) 
		LINE TO (6.5,Thickness) 
		LINE TO (0,Thickness)
		TO CLOSE
TIME 0 TO tfinal
PLOTS            { save result displays }
for time = tfinal !don't need to specify a time range if you just want one particular time
contour(Temp) painted 
vector(qdot) norm
SUMMARY
Export file="afile.txt"
report integral(Temp,'can filled with water')/integral(1,'can filled with water') as 'Average Temperature'
report (initTempCube) as 'Inital Temperature of Ice Cube'
END
"""
FlexFileName = "Flexin.pde"

import scipy as sp
import subprocess
import matplotlib.pyplot as plt
temp_H = -16
Temperatures = sp.arange(-15,6,1)
for Temperature in Temperatures:
    print("Temperature: ",Temperature)
    with open(FlexFileName, "w") as f:
        print(flexcode%Temperature,file=f)
    subprocess.run(["C:\FlexPDE6student\FlexPDE6s", "-S", FlexFileName])
    with open ("afile_1.txt", "r") as f:
        output = f.readlines()
    AvgT = float(output[7][22:])
    print(AvgT)
    plt.scatter(AvgT,Temperature)
    if AvgT < 4 and Temperature > temp_H:
        temp_H = Temperature
print("Rough Maximum Initial Temperature of the Ice: ", temp_H,"\N{DEGREE SIGN}"'C')
X = 1/((4.00194-3.994533)/(4-3.994533))
print("Through Linear Interpolation, the highest temperature the cooling device can be to maintain the inital temperature of the beverage after 30 min is: ", X,"\N{DEGREE SIGN}"'C')
plt.plot(AvgT,Temperature,label=Temperature)
plt.xlabel('Average Temperature of the Beverage\N{DEGREE SIGN}''C')
plt.ylabel('Initial Temperature of the Cooling Device\N{DEGREE SIGN}''C')
plt.show()



















