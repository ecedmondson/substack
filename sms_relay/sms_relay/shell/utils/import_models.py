import importlib.util
import os


def import_all_models():
    base_path = os.getcwd()
    for root, dirs, files in os.walk(base_path):
        if "__init__.py" in files:
            module_path = os.path.join(root, "__init__.py")
            module_name = os.path.relpath(module_path, base_path).replace(os.sep, ".").replace(".py", "")
            
            try:
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)  # Import the module
                print(f"Imported models from: {module_name}")
            except Exception as e:
                print(f"Failed to import {module_name}: {e}")
