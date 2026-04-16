For Linux:

- unzip the source code:

    unzip swarm-world.zip


- install the following python packages:

    1. sudo apt-get install python3.6 python3-pip  gnuplot

    2. sudo pip install numpy pandas PyOpenGL Pillow PyQt5 opencv-python


- go to the main folder of the SNS-Folder and start it with:

    python swarm-sim.py

If needed check the config.ini for which solution and scenario has been selected


For development the IDE Pycharm is recommended:

https://www.jetbrains.com/help/pycharm/install-and-set-up-pycharm.html

0. Install python, pip and gnuplot
	e.g. sudo apt-get install python3.6 python3-pip gnuplot	
1. Download and install PyCharm, enter your licence
2. Settings - version control - github -> Add your account
3. Checkout https://github.com/graffi/swarmsim.git
4. Create a new interpreter - a virtual environment (venv)
5. Locally go to the folder of the corresponding venv. and activate it: source /bin/activate
6. sudo pip install numpy pandas PyOpenGL Pillow PyQt5 opencv-python
7. In PyCharm: chose Run -> swarm-sim.py
