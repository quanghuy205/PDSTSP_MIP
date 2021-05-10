A) NODE INFO files:
FORMAT for nodes info files
Node #		x	y	tooHeavy
0 (depot)				*
1				0 or 1
2				0 or 1
...				... (1 if The customer's parcel is too heavy for the UAV, 0 otherwise)
n				0 or 1

B) Other parameters tailored for min-cost VRPD are contained in: params.csv
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