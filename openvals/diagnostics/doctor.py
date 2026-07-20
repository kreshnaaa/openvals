from openvals.diagnostics.system import get_detailed_system_profile

from openvals.models.discovery import discover_providers
from openvals.advisor.model_catalog import list_models

from openvals.diagnostics.datasets import discover_datasets
from openvals.diagnostics.configs import discover_configs
from openvals.diagnostics.version import get_version_info
from openvals.diagnostics.health import compute_health

def run_doctor():
    """
    Run OpenVals diagnostics and return a complete health profile.
    """
    version = get_version_info()
    system = get_detailed_system_profile(
        mode="standard",
        model_count=1
    )

    providers = discover_providers()
    installed_models = list_models()
    datasets = discover_datasets()
    configs = discover_configs()
    health = compute_health(
        providers=providers,
        datasets=datasets,
        configs=configs
    )

    return {
        "version": version,
        "system": system,
        "providers": providers,
        "installed_models": installed_models,
        "datasets": datasets,
        "configs": configs,
        "health": health
    }