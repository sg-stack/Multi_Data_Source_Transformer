import json
import re
from dataclasses import asdict


class Projector:
    """
    Converts the internal canonical profile into the
    requested output schema using config.json.
    """

    def __init__(self, config_path):

        with open(config_path, "r", encoding="utf-8") as file:
            self.config = json.load(file)

    ###########################################################
    # Main Projection Function
    ###########################################################

    def project(
        self,
        candidate,
        confidence=None,
        provenance=None,
    ):

        candidate = asdict(candidate)

        output = {}

        fields = self.config.get("fields", [])

        for field in fields:

            output_name = field["path"]

            source_path = field.get("from", output_name)

            value = self._get_value(
                candidate,
                source_path,
            )

            # Handle Missing Values

            if value is None:

                action = self.config.get(
                    "on_missing",
                    "null",
                )

                if action == "omit":
                    continue

                if action == "error":
                    raise ValueError(
                        f"Missing required field : {output_name}"
                    )

                output[output_name] = None
                continue

            ###################################################
            # Optional Normalization
            ###################################################

            normalize = field.get("normalize")

            if normalize == "canonical":

                if isinstance(value, list):

                    value = sorted(
                        list(
                            set(value)
                        )
                    )

            output[output_name] = value

        #######################################################
        # Confidence
        #######################################################

        if self.config.get(
            "include_confidence",
            False,
        ):

            output["confidence"] = confidence

        #######################################################
        # Provenance
        #######################################################

        if self.config.get(
            "include_provenance",
            False,
        ):

            output["provenance"] = provenance

        return output

    ###########################################################
    # Nested Field Resolver
    ###########################################################

    def _get_value(
        self,
        obj,
        path,
    ):

        current = obj

        tokens = path.split(".")

        for token in tokens:

            index_match = re.match(
                r"(\w+)\[(\d+)\]",
                token,
            )

            if index_match:

                key = index_match.group(1)

                index = int(
                    index_match.group(2)
                )

                current = current.get(key)

                if current is None:
                    return None

                if len(current) <= index:
                    return None

                current = current[index]

            else:

                if isinstance(current, dict):

                    current = current.get(token)

                else:

                    return None

                if current is None:

                    return None

        return current