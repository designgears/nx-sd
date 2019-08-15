class NXSDConfig(object):

    def __init__(self, build_directory, components_directory, defaults_directory, dockerfiles_directory):
        self.build_directory = build_directory
        self.components_directory = components_directory
        self.defaults_directory = defaults_directory
        self.dockerfiles_directory = dockerfiles_directory


settings = NXSDConfig(
    build_directory='out/',
    components_directory='components/',
    defaults_directory='defaults/',
    dockerfiles_directory='dockerfiles/',
)
