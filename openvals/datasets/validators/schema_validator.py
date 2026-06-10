REQUIRED_FIELDS = [

    "prompt",
    "expected_output"

]

def validate_schema(dataset):

    errors = []

    for index, sample in enumerate(dataset):

        for field in REQUIRED_FIELDS:

            if field not in sample:

                errors.append(

                    f"Record {index}: "
                    f"missing '{field}'"

                )

                continue

            if not isinstance(

                sample[field],
                str

            ):

                errors.append(

                    f"Record {index}: "
                    f"'{field}' must be string"

                )

    return {

        "valid": len(errors) == 0,

        "errors": errors

    }