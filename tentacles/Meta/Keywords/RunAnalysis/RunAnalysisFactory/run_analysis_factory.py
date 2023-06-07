from types import ModuleType


def get_installed_run_analyzer_modules(modules_root):
    available_run_analyzer_modules = {
        module_name: {
            sub_module_name: sub_module
            for sub_module_name, sub_module in module.__dict__.items()
            if isinstance(sub_module, type)
            and hasattr(sub_module, "evaluate")
            and hasattr(sub_module, "init_user_inputs")
        }
        for module_name, module in modules_root.__dict__.items()
        if isinstance(module, ModuleType)
    }
    return available_run_analyzer_modules
