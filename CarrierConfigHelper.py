import os
import sys
import shutil
import glob
import xml.etree.ElementTree as ET

WINDOWS_ADB_PATH = ".\platform-tools\\"

CONFIG_VOLTE    = "carrier_volte_available_bool"
CONFIG_WFC      = "carrier_wfc_ims_available_bool"

def main():
    os.system(WINDOWS_ADB_PATH + 'adb devices')
    print('Start adb root ... ')
    os.system(WINDOWS_ADB_PATH +'adb root')
    print('Start adb remount ... ')
    os.system(WINDOWS_ADB_PATH +'adb remount')
    print('Start pull Carrier Config ...')
    os.system(WINDOWS_ADB_PATH +'adb pull data/user_de/0/com.android.phone/files')

    fpath = os.path.join('.\\files', '*.xml')
    config_files = glob.glob(fpath)

    print("List all config files ...")
    for config_file, i in zip(config_files, range(len(config_files))):
        print('[{}]:\t{}'.format(i,config_file))
    print('Which file?')
    file_index = user_input()

    if (not file_index):
        sys.exit(0)
    else:
        file_index = int(file_index)

    tree = ET.parse(config_files[file_index])
    root = tree.getroot()


    while(1):
        add = None
        print('config -> ')
        
        config_name = user_input()

        if (not config_name):
            break

        if (root.findall(".//*[@name='{}']".format(config_name))):
            print(root.findall(".//*[@name='{}']".format(config_name))[0].attrib)
        else:
            print('Could not find ' + config_name)
            print('Add \'{}\' into config?[Y/N]'.format(config_name))
            add = user_input()

            if (not add):
                break

            if (add != 'Y'):
                continue

        print('value -> ')

        config_value = user_input()

        if (not config_value):
            break

        if (add == "Y"):
            print('Type?[string/boolean/int/long ...]')
            config_type = user_input()

            if (not config_type):
                break

            new_config = ET.SubElement(root, config_type)
            new_config.set('name', config_name)
            new_config.set('value', config_value)

        else:
            root.findall(".//*[@name='{}']".format(config_name))[0].attrib['value'] = config_value

        print(root.findall(".//*[@name='{}']".format(config_name))[0].attrib)

    tree.write(config_files[0])

    print('Start push Carrier Config ...')
    os.system(WINDOWS_ADB_PATH +"adb push .\\files /data/user_de/0/com.android.phone/")

    print("Reboot?[Y/N]")
    reboot = user_input()


    if (reboot == "Y"):
        print('Rebooting ...')
        os.system(WINDOWS_ADB_PATH +"adb reboot")
    else:
        print('Manaul reboot device to make the modification effect.')
    
    try:
        shutil.rmtree('.\\files')
    except OSError as e:
        print(e)

    return

def user_input():
    if (sys.version.startswith('2')):
        user_in = raw_input()
    else:
        user_in = input()

    if (user_in in ['q', 'exit', 'quit']):
        return ''
    return user_in

if __name__ == '__main__':
    main()