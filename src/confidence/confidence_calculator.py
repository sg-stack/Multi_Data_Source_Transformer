import re

from src.models.parsed_candidate import ParsedCandidate


class ConfidenceCalculator:

    SOURCE_SCORE = {
        "resume": 1.00,
        "linkedin": 0.90,
        "github": 0.80,
        "csv": 0.60,
    }

    def calculate(self, candidate: ParsedCandidate) -> dict:
        """
        Returns confidence for each field along with
        the overall profile confidence.
        """

        confidence = {}

        confidence["full_name"] = self._string_confidence(
            candidate.full_name,
            candidate.source
        )

        confidence["emails"] = self._email_confidence(
            candidate.emails,
            candidate.source
        )

        confidence["phones"] = self._phone_confidence(
            candidate.phones,
            candidate.source
        )

        confidence["location"] = self._location_confidence(
            candidate.location,
            candidate.source
        )

        confidence["headline"] = self._string_confidence(
            candidate.headline,
            candidate.source
        )

        confidence["skills"] = self._list_confidence(
            candidate.skills,
            candidate.source
        )

        confidence["experience"] = self._experience_confidence(
            candidate.experience,
            candidate.source
        )

        confidence["education"] = self._education_confidence(
            candidate.education,
            candidate.source
        )

        confidence["projects"] = self._list_confidence(
            candidate.projects,
            candidate.source
        )

        confidence["certifications"] = self._list_confidence(
            candidate.certifications,
            candidate.source
        )

        confidence["links"] = self._list_confidence(
            candidate.links,
            candidate.source
        )

        confidence["achievements"] = self._list_confidence(
            candidate.Achievements,
            candidate.source
        )

        values = list(confidence.values())

        confidence["profile_confidence"] = round(
            sum(values) / len(values),
            2
        )

        return confidence

    ##############################################################
    # Generic String Confidence
    ##############################################################

    def _string_confidence(self, value, source):

        if not value:
            return 0.0

        source_score = self.SOURCE_SCORE.get(source, 0.5)

        quality = 1.0 if len(value) >= 3 else 0.5

        return round(
            0.7 * source_score +
            0.3 * quality,
            2,
        )

    ##############################################################
    # Email
    ##############################################################

    def _email_confidence(self, emails, source):

        if not emails:
            return 0.0

        source_score = self.SOURCE_SCORE.get(source, 0.5)

        valid = 0

        for email in emails:

            if re.match(
                r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
                email,
            ):
                valid += 1

        quality = valid / len(emails)

        return round(
            0.7 * source_score +
            0.3 * quality,
            2,
        )

    ##############################################################
    # Phone
    ##############################################################

    def _phone_confidence(self, phones, source):

        if not phones:
            return 0.0

        source_score = self.SOURCE_SCORE.get(source, 0.5)

        valid = 0

        for phone in phones:

            digits = re.sub(r"\D", "", phone)

            if len(digits) >= 10:
                valid += 1

        quality = valid / len(phones)

        return round(
            0.7 * source_score +
            0.3 * quality,
            2,
        )

    ##############################################################
    # Location
    ##############################################################

    def _location_confidence(self, location, source):

        if not location:
            return 0.0

        source_score = self.SOURCE_SCORE.get(source, 0.5)

        filled = 0

        for value in location.values():

            if value:
                filled += 1

        quality = filled / 3

        return round(
            0.7 * source_score +
            0.3 * quality,
            2,
        )

    ##############################################################
    # List Fields
    ##############################################################

    def _list_confidence(self, values, source):

        if not values:
            return 0.0

        source_score = self.SOURCE_SCORE.get(source, 0.5)

        quality = min(len(values) / 5, 1)

        return round(
            0.7 * source_score +
            0.3 * quality,
            2,
        )

    ##############################################################
    # Experience
    ##############################################################

    def _experience_confidence(self, experience, source):

        if not experience:
            return 0.0

        source_score = self.SOURCE_SCORE.get(source, 0.5)

        complete = 0

        for exp in experience:

            if (
                exp.get("company")
                and exp.get("title")
            ):
                complete += 1

        quality = complete / len(experience)

        return round(
            0.7 * source_score +
            0.3 * quality,
            2,
        )

    ##############################################################
    # Education
    ##############################################################

    def _education_confidence(self, education, source):

        if not education:
            return 0.0

        source_score = self.SOURCE_SCORE.get(source, 0.5)

        complete = 0

        for edu in education:

            if (
                edu.get("degree")
                and edu.get("institution")
            ):
                complete += 1

        quality = complete / len(education)

        return round(
            0.7 * source_score +
            0.3 * quality,
            2,
        )