from CodGenLib import cdlib_push
import os 
import json

module_name = 'HwAbDio'
module_conf_dir = os.path.dirname(os.path.realpath(__file__))
working_dir = os.getcwd()
gen_dir = working_dir + '/_out/'


# check module activation
def is_module_activated( conf_data):
    if( (module_name in conf_data) and ('configset' in conf_data[module_name])):
        return True
    else:
        return False

# set default value
def set_default_value(conf_data):
    if(is_module_activated(conf_data)):
        if(not ("general" in  conf_data[module_name])):
            conf_data[module_name]['general'] = dict()

        if( not "debug" in  conf_data[module_name]['general'] ):
            conf_data[module_name]['general']['debug'] = True

        configset = dict(conf_data[module_name]['configset'])
        for signal in configset.keys():
            if( not "callback" in  configset[signal]):
                configset[signal]['callback'] = 'NULL'
            if( not "init_state" in  configset[signal]):
                configset[signal]['init_state'] = 'STD_OFF'
            if( not "inverted" in  configset[signal]):
                configset[signal]['inverted'] = 'false'
            if( not "interrupt" in  configset[signal]):
                configset[signal]['interrupt'] = 'DISABLE'
    return conf_data
def get_devices(conf_data):
    return dict(conf_data[module_name]['devices']).keys()
def get_configset(conf_data):
    return dict(conf_data[module_name]['configset'])

def hwabdio_forward(conf_data):
    print("- hwabdio_forward:")
    if( not is_module_activated(conf_data) ):
        print("Component is deactivated!\r\n")
    else:
        conf_data = set_default_value(conf_data)
        devices = get_devices(conf_data)
        pushed_data = dict()
        confgiset = get_configset(conf_data)
        for signal in confgiset.keys():
            signal_pushed_data = dict({})
            connected_device = str(confgiset[signal]['connected_to']).split('_')[0]
            signal_pushed_data['connected_to'] = str(confgiset[signal]['connected_to']).split('_')[1]
            signal_pushed_data['init_state']   = confgiset[signal]['init_state']
            signal_pushed_data['callback']     = confgiset[signal]['callback']
            signal_pushed_data['inverted']     = confgiset[signal]['inverted']
            signal_pushed_data['direction']    = confgiset[signal]['direction']
            signal_pushed_data['interrupt']    = confgiset[signal]['interrupt']
            signal_pushed_data = {module_name + '_' + signal: signal_pushed_data}
            for device in devices:
                if(connected_device.upper() == str(device).upper()):
                    signal_pushed_data = dict({device:{'configset':signal_pushed_data}})
            pushed_data = dict(cdlib_push(pushed_data, dict(signal_pushed_data)))

        push_file_content = str( json.dumps(pushed_data,indent=2))
        push_file = open(gen_dir + '/' +module_name +  "_Pushed.json", "w")
        push_file.write(push_file_content)
        push_file.close()

        conf_data = dict(cdlib_push(conf_data, dict(pushed_data)))
    return conf_data



def generate_cfg_h(conf_data):
    cfg_ht_file = open(module_conf_dir + "/" +module_name + "_Cfg.ht","r")
    cfg_h_file_content = cfg_ht_file.read()
    cfg_h_setting = ""
    cfg_h_include = ""
    cfg_h_signals_id =""
    off_setting = "    STD_OFF\r\n"
    on_setting  = "    STD_ON\r\n"
    cfg_h_setting += "#define HWABDIO_CFG_MODULE_ACTIVE"
    if( not is_module_activated(conf_data) ):
        cfg_h_setting += off_setting
    else:
        cfg_h_setting += on_setting
        cfg_h_setting += "#define HWABDIO_CFG_DEBUG"
        if(conf_data[module_name]['general']['debug']):
            cfg_h_setting += on_setting
        else:
            cfg_h_setting += off_setting
        cfg_h_setting += "#define HWABDIO_CFG_NUM    " + str(len(conf_data[module_name]['configset'])) +'u\r\n'
        devices = dict(conf_data[module_name]['devices']).keys()
        signal_id = 0
        connected_devices = set()
        configset = dict(conf_data[module_name]['configset'])
        for signal in configset.keys():
            cfg_h_signals_id += "#define " + str(module_name + "_"+signal).upper() + "   \t" + str(signal_id)+"u\r\n"

            connected_device = str(configset[signal]['connected_to']).split('_')[0]
            for device in devices:
                 if(connected_device.upper() == str(device).upper()):
                     connected_devices.add(device)

            signal_id +=1
        cfg_h_signals_id +="\r\n"
        device_id =0
        
        for device in connected_devices:
            cfg_h_signals_id += "#define " + str(module_name + "_Dev_"+ device).upper() + "   \t" + str(device_id)+"u\r\n"
            device_id +=1
        
        for device in connected_devices:
            cfg_h_include += "#include \"" + conf_data[module_name]['devices'][device]['header'] +"\"\r\n"

    cfg_h_file_content = cfg_h_file_content.replace("<INCLUDE DRIVERS>", cfg_h_include)
    cfg_h_file_content = cfg_h_file_content.replace("<SIGNALS IDS>", cfg_h_signals_id)
    cfg_h_file_content = cfg_h_file_content.replace("<CONFIGURATION SETTINGS>", cfg_h_setting)
    # generate the files
    cfg_h_file = open(gen_dir + '/' + module_name + "_Cfg.h", "w")
    cfg_h_file.write(cfg_h_file_content)
    cfg_h_file.close()

def generate_cfg_c(conf_data):
    cfg_c_signals = ""
    cfg_c_devices = ""
    if( not is_module_activated(conf_data) ):
        return
    else:
        cfg_ct_file = open(module_conf_dir + '/' + module_name + "_Cfg.ct","r")
        cfg_c_file_content = cfg_ct_file.read()

        devices = dict(conf_data[module_name]['devices']).keys()
        connected_devices = set()
        configset = dict(conf_data[module_name]['configset'])
        for signal in configset.keys():
            cfg_c_signals += "  {\r\n"
            cfg_c_signals += "      //" + signal + "\r\n"
            connected_device = str(configset[signal]['connected_to']).split('_')[0]
            for device in devices:
                 if(connected_device.upper() == str(device).upper()):
                     cfg_c_signals += "      " + str(module_name + "_Dev_" + device).upper() + ",\r\n"
                     cfg_c_signals += "      " + device + "_" + module_name + "_" + signal + "\r\n"
                     connected_devices.add(device)
            cfg_c_signals += "  },\r\n"
        for device in connected_devices:
            cfg_c_devices += "      &"+conf_data[module_name]['devices'][device]['interfaces']+",\r\n"
    cfg_c_file_content = cfg_c_file_content.replace("<SIGNALS CONFIGURATIONS>", cfg_c_signals)
    cfg_c_file_content = cfg_c_file_content.replace("<DEVICES CONFIGURATIONS>", cfg_c_devices)
    cfg_ct_file.close()
    # generate the files
    cfg_c_file = open(gen_dir + '/' +module_name +"_Cfg.c", "w")
    cfg_c_file.write(cfg_c_file_content)
    cfg_c_file.close()


def hwabdio_deviceinfo_forward(conf_data):
    print("- hwabdio_deviceinfo_forward:")
    return conf_data

def hwabdio_generate(conf_data):
    print("- hwabdio_generate:")
    if( not is_module_activated(conf_data) ):
        print("Component is deactivated!\r\n")

    conf_data = set_default_value(conf_data)
    generate_cfg_h(conf_data)
    generate_cfg_c(conf_data)
 
    

