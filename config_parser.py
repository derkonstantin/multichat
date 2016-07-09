import configparser


CONFIG_DEFAULT = './multi_chat.config'


def get_config(config_file = CONFIG_DEFAULT):
        config = {}
        cfg = configparser.ConfigParser()
        cfg.read(config_file)
        for section in cfg.sections():
            config[section] = {}
            for key in cfg[section].keys():
                config[section][key] = cfg[section][key]
        return(config)

if __name__ == '__main__':
    print (get_config())