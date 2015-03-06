from sublime import error_message
from sublime_plugin import WindowCommand

class BuildSelectCommand(WindowCommand):
    def run(self, *args, **kwargs):
        projectData = self.window.project_data()
        
        if not projectData:
            return
        
        self.buildSystems = get_build_systems(projectData)
        
        if len(self.buildSystems) == 0:
            error_message("No build systems defined for this project")
        
        self.window.show_quick_panel(
            list(map(lambda system: system.displayName, self.buildSystems)),
            self.run_build
        )
    
    def run_build(self, index):
        if index == -1:
            return
        
        try:
            selectedSystem = self.buildSystems[index]
        except IndexError:
            error_message("Selected build system does not exist (??!)")
            
            return
        
        self.window.run_command("set_build_system", {"file": selectedSystem.name})
        self.window.run_command("build", {"variant": selectedSystem.variant})

class BuildSystem(object):
    def __init__(self, displayName, name = None, variant = None):
        self.displayName = displayName
        self.name = name or displayName
        self.variant = variant

def get_build_systems(projectData):
    result = []
    
    for system in projectData.get("build_systems", []):
        systemName = None
        
        try:
            systemName = system["name"]
        except KeyError:
            continue
        
        result.append(BuildSystem(systemName))
        
        for variant in system.get("variants", []):
            try:
                variantName = variant["name"]
                
                result.append(
                    BuildSystem(
                        "{} ({})".format(systemName, variantName),
                        systemName,
                        variantName
                    )
                )
            except KeyError:
                continue
    
    return result
