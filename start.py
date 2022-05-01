import sys
from CIM_Data_Manager import start_gui
from Simple_mode import import_cim


def helpme():
    print('-help       shows the args documentation')
    print('-mode       sets the mode: - simple (background task) or gui to start CIM Data Manager')
    print('-input      input folder where the CIM files are located')
    print('-export     output folder where the CIM files will be exported to')
    print('-profiles   Sets the profiles to be exported')
    print('Example: py.exe .\start.py -mode:simple -input:.\ImportedData2 -output:.\ExportedData\ ')


def main():
    mode = None
    input_path = None
    output_path = None
    sincal2pf = None
    ProfileList = None
    for arg in sys.argv:
        if 'help' in arg:
            helpme()
            break
        if 'mode' in arg:
            mode = arg[6:].lower()
        if 'input' in arg:
            input_path = arg[7:]
        if 'output' in arg:
            output_path = arg[8:]
        if 'profiles' in arg:
            ProfileList = (arg[10:]).split(',')
        if 'Sincal2PF' in arg:
            sincal2pf = True

    if not mode:
        print('Please select a mode from this list [simple, Gui]')
        return
    elif mode == 'simple':
        if not input_path or not output_path:
            print('Please select an input and an output folder')
            print('For more help type -help')
            return
        if not ProfileList:
            print('Please set the profiles to be exported')
            print('For more help type -help')
            return
    if mode == 'simple':
        try:
            import_cim(input_path, output_path, sincal2pf, ProfileList)
        except Exception as e:
            print('ERROR!!!:'+str(e))
            print('Please make sure that the input and output folders exist.')
    elif mode == 'gui':
        try:
            start_gui()
        except Exception as e:
            print('ERROR!!!:'+str(e))


if __name__ == '__main__':
    main()
