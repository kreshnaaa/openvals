MODEL_REGISTRY = {}

def register_model(
    provider,
    model_class
):
    MODEL_REGISTRY[
        provider
    ] = model_class

def get_provider(
    provider
):
    return MODEL_REGISTRY.get(
        provider
    )

def list_providers():
    return list(
        MODEL_REGISTRY.keys()
    )