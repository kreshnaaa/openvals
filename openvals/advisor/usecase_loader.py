import json
from pathlib import Path


# =========================================================
# USE CASE LOADER
# =========================================================

def load_use_case_from_file(file_path):

    path = Path(file_path)

    if not path.exists():

        raise FileNotFoundError(
            f"Use case file not found: {file_path}"
        )

    suffix = path.suffix.lower()

    if suffix == ".txt":

        return path.read_text(
            encoding="utf-8"
        ).strip()

    if suffix == ".json":

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(data, dict):

            raise ValueError(
                "JSON use case file must be an object"
            )

        return parse_use_case_json(
            data
        )

    raise ValueError(
        f"Unsupported use case file format: {suffix}"
    )


# =========================================================
# JSON PARSER
# =========================================================

def parse_use_case_json(data):

    fields = [
        "problem",
        "use_case",
        "industry",
        "domain",
        "requirements",
        "constraints",
        "deployment",
        "data_sensitivity",
        "latency",
        "budget"
    ]

    parts = []

    for field in fields:

        value = data.get(field)

        if value is None:
            continue

        if isinstance(value, list):

            value = ", ".join(
                [
                    str(item)
                    for item in value
                ]
            )

        elif isinstance(value, dict):

            value = json.dumps(
                value
            )

        else:

            value = str(value)

        parts.append(
            f"{field}: {value}"
        )

    if not parts:

        raise ValueError(
            "JSON use case file contains no supported fields"
        )

    return "\n".join(parts)