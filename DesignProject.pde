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
initTempCube = 0.75
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
		load (temp)=0
		LINE TO (0,12) !top side 
		load (temp)=h*(Temp-Surroundings)
		LINE TO (6.5,12)!right side
		load (temp)=0
		LINE TO (6.5, 0) !bottom side
		load (temp)=0
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
