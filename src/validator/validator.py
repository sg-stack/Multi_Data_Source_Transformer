from src.models.parsed_candidate import ParsedCandidate

class Validator:
    """
    Validates the final canonical candidate before projection/output.
    """

    def validate(self, candidate: ParsedCandidate) -> bool:

        if candidate is None:
            raise ValueError("Candidate cannot be None.")

        if not candidate.full_name:
            raise ValueError("Candidate name is required.")

        if not candidate.emails and not candidate.phones:
            raise ValueError(
                "At least one contact detail (email or phone) must be present."
            )

        return True