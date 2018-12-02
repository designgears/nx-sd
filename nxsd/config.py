class NXSDConfig(object):

    def __init__(self, build_directory, components_directory, defaults_directory, patches_directory):
        self.build_directory = build_directory
        self.components_directory = components_directory
        self.defaults_directory = defaults_directory
        self.patches_directory = patches_directory


settings = NXSDConfig(
    build_directory='build/',
    components_directory='components/',
    defaults_directory='defaults/',
    patches_directory='patches/',
)
