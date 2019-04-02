class NXSDConfig(object):

    def __init__(self, build_directory, components_directory, defaults_directory):
        self.build_directory = build_directory
        self.components_directory = components_directory
        self.defaults_directory = defaults_directory


settings = NXSDConfig(
    build_directory='build/',
    components_directory='components/',
    defaults_directory='defaults/',
)
