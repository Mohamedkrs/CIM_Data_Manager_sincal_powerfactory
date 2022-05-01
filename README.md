# CIMPy_Sincal_ODMS_PowerFactory

helps data exchange between PowerFactory and PSSⓇSincal
# Why?
Data excahnge between PSSⓇSincal and PowerFactory is not as straight forward as it seems, especially when going from PSSⓇSincal to PowerFactory. This repo uses and adapt the [CIMPy library from RWTH Aachen Germany](https://git.rwth-aachen.de/acs/public/cim/cimpy).
## Important
The use of PSSⓇODMS is also important in this work as it automatically builds the ConnectivityNode element, which is mandatory by PowerFactroy.
## Overall roadmap
The discontinuous lines means that the step is optional.
![newschma](https://user-images.githubusercontent.com/44847005/166157527-643b00a9-79f7-4165-9e7a-4edd657ec034.png)

# Documentation
## Install requierments
Clone this repository locally, if you want to install the required modules globally, start the following command in the vscode or whatever terminal you are using. Otherwise if you want contain the code and its modules in a virtual environment, the create on ( see [here](https://docs.python.org/3/library/venv.html) how to create a virtual environment) and run the following command.
> pip install -r requirements.txt
## Start CIM Data Manager
### Commands
- -help    :   shows the args documentation
- -mode    :   sets the mode: - simple (background task) or gui to start CIM Data Manager
- -input    :  input folder where the CIM files are located
- -export   :  output folder where the CIM files will be exported to
- -profiles :  Sets the profiles to be exported

### Simple mode
start start.py with its command as specify all of the obove mentionned parameters
> py.exe .\start.py [commands]

Example: 
> py.exe .\start.py -mode:simple -input:.\ImportedData -output:.\ExportedData\

### GUI mode
Run the following command:
> py.exe .\start.py -mode:gui

A user interface will appear and data can be displayed as follow after importing it from a folder containing CIM files:
![image](https://user-images.githubusercontent.com/44847005/166158745-7fd86c80-7fa9-485e-8a0b-b84e2ee5e196.png)

# License
This project is released under the terms of the [MIT License](https://github.com/Mohamedkrs/CIMPy_Sincal_ODMS_PowerFactory/blob/main/LICENSE)
