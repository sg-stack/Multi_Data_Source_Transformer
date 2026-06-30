import json
import os

from src.parsers.resume_parser import ResumeParser
from src.parsers.csv_parser import CSVParser
# from src.parsers.github_parser import GitHubParser
# from src.parsers.linkedin_parser import LinkedInParser

from src.normalizers.normalizer import Normalizer
from src.merger.merger import Merger
from src.confidence.confidence_calculator import ConfidenceCalculator
from src.provenance.provenance_tracker import ProvenanceTracker
from src.projection.projection import Projector


def main():

    ###########################################################
    # Input Files
    ###########################################################

    resume_path ="sample_inputs/CIT_Shrinivasan S G_AI&DS.pdf"

    csv_path = "sample_inputs/professional_profiles.csv"

    config_path = "src/config/config.json"

    ###########################################################
    # Parse Sources
    ###########################################################

    parsed_candidates = []

    # Resume

    if os.path.exists(resume_path):

        resume_candidate = ResumeParser().parse(
            resume_path
        )

        parsed_candidates.append(
            resume_candidate
        )

    # CSV

    if os.path.exists(csv_path):

        csv_candidates = CSVParser().parse(
            csv_path
        )

        parsed_candidates.extend(
            csv_candidates
        )



    ###########################################################
    # Normalize
    ###########################################################

    normalizer = Normalizer()

    normalized_candidates = []

    for candidate in parsed_candidates:

        normalized_candidates.append(

            normalizer.normalize(candidate)

        )

    ###########################################################
    # Merge
    ###########################################################

    merger = Merger()

    canonical_candidate = merger.merge(
        normalized_candidates
    )

    ###########################################################
    # Confidence
    ###########################################################

    confidence = ConfidenceCalculator().calculate(
        canonical_candidate
    )

    ###########################################################
    # Provenance
    ###########################################################

    provenance = ProvenanceTracker().generate(
        canonical_candidate,
        normalized_candidates,
    )

    ###########################################################
    # Projection
    ###########################################################

    projector = Projector(
        config_path
    )

    final_output = projector.project(

        canonical_candidate,

        confidence,

        provenance,

    )

    ###########################################################
    # Print
    ###########################################################

    print(
        json.dumps(
            final_output,
            indent=4,
        )
    )

    ###########################################################
    # Save Output
    ###########################################################

    os.makedirs(
        "sample_outputs",
        exist_ok=True,
    )

    with open(

        "sample_outputs/canonical_profile.json",

        "w",

        encoding="utf-8",

    ) as file:

        json.dump(

            final_output,

            file,

            indent=4,

        )

    print(
        "\nCanonical profile saved successfully."
    )


if __name__ == "__main__":
    main()