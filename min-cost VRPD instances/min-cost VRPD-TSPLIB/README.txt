A) NODE INFO files: <MAP NAME>_<DEPOT LOCATION>_<DRONE-ELIGIBLE %>.csv
    MAP NAME = {att48; berlin52; eil101; gr120; pr152; gr229}
    DEPOT LOCATION = 0 : depot locates at the CENTER
                   = 1 : depot locates at the CORNER
For example: 
berlin52_0_80.csv -> map "berlin52", depot locates at the center, 80% of nodes are eligible to drone delivery.

FORMAT for nodes info files
Node #		x	y	tooHeavy
0 (depot)				*
1				0 or 1
2				0 or 1
...				... (1 if The customer's parcel is too heavy for the UAV, 0 otherwise)
n				0 or 1

B) Other parameters tailored for min-cost VRPD: <MAP NAME>_<DEPOT LOCATION>.csv
This file contains a list of parameters needed to define the min-cost VRPD. The data are in a single row in the following order:
1. Number of drone
2. Number of trucks		
3. Capacity of a truck
4. Capacity of a drone
5. Truck speed
6. Drone speed
7. Drone endurance
8. Travel time limit for a drone tour
9. Travel time limit for a truck tour
10. Truck unit cost (alpha)
11. Drone unit cost (beta)