import importlib
import pkgutil


def load_skills():
    skills = {}
    for m in pkgutil.iter_modules(__path__):
        if m.ispkg:
            continue
        mod = importlib.import_module(f"{__name__}.{m.name}")
        if hasattr(mod, "SKILL_NAME") and hasattr(mod, "run"):
            skills[mod.SKILL_NAME] = mod.run
    return skills
