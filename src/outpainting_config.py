from configparser import ConfigParser


class OutPaintingConfig:
    config_object = ConfigParser()
    config_name = 'outpainting_config.ini'

    def __load_config(self):
        self.config_object.read(self.config_name)
        return self.config_object

    def save_config(self):
        with open(self.config_name, 'w') as conf:
            self.config_object.write(conf)

    def set_config(self, section, key, value):
        self.__load_config()
        if section not in self.config_object:
            self.config_object[section] = {}
        self.config_object[section][key] = value
        self.save_config()

    def get_config(self, section, key) -> str:
        self.__load_config()
        if section not in self.config_object or key not in self.config_object[section]:
            return ''
        return self.config_object[section][key]

    def get_config_int(self, section, key) -> int:
        result = self.get_config(section, key)
        if result == '':
            return 0
        return int(result)

    def get_config_float(self, section, key) -> float:
        result = self.get_config(section, key)
        if result == '':
            return 0.0
        return float(result)

    def print_config(self):
        self.__load_config()
        for section in self.config_object.sections():
            print(f'[{section}]')
            for key in self.config_object[section]:
                print(f'{key}={self.config_object[section][key]}')
            print()
