# SIR-turtle-sim
SIR Infectious disease spread model using turtle graphics library in python

Things implemented:
- Random Walk of turtles
- Infection and removed categories along with color coding

Things not implemented:
- Graphs of any kind to view the data
- Other scenarios like central market, social distancing, etc

The use of turtle graphics makes the animation of the nodes moving and the infection spreading very slow. Recommended N is < 100 nodes.
There is an internal status variable which keeps track of [S,I,R] but not implemented to a graphical representation because of the limitation of matplotlib and lack of animated graphical libraries that can change axes with addition of new data
