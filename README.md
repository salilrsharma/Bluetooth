# Processing Bluetooth data for deriving route choices of truck drivers

ToGRIP-Bluetooth service provides the Bluetooth data collected by the port of Rotterdam. When queried, the service returns data in a json format. The real MAC address is converted to an 11 digit vehicle ID using hashing thus the privacy is retained at the user level. The Bluetooth sensor records the time stamp and the strength of the vehicle identification for every MAC address associated with a passing vehicle. The travel time between two Bluetooth sensors can be estimated from the time stamps of the corresponding MAC address. Bluetooth data retrieved from ToGRIP-Bluetooth service are coded with UTC time zone; therefore, it is necessary to convert UTC time to CET/CEST depending on the time of the year. 

The code provided in this repository can be used for various purposes such as estimatign travel time between two Bluetooth locations, inferring cars and trucks from Bluetooth data, and creating a data file for route choice model to be estimated by Biogeme. 

I present here a workflow related to deriving route choices of truck drivers usign Bluetooth data based on our recent MT-ITS conference paper. 

1. Run new_Bluetooth.py

Basic code to retrieve Bluetooth observations between two points. With this file, we can process individual travel times between two Bluetooth sensors. Moreover, we can also cluster vehicles into two groups based on travel time observation using Gaussian mixture model based clustering. This clustering helps to identify different travel modes. 

2. Run new_trajectory.py

Generate Bluetooth observations along a trajectory

3. Run dataprocessing.py

Create a master list by combining individual observations from above step

4. Run new_find_trucks.py

Extract truck-specific data from the master list created in step 3.

5. Run new_file_for_biogeme.py

Putting up a file together for biogeme by combining Bluetooth data and other data sources such as loop-detecor data and variable message sign (VMS) data
