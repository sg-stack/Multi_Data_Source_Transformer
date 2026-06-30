import uuid
from copy import deepcopy

from src.models.parsed_candidate import ParsedCandidate


class Merger:

    """
    Merges multiple ParsedCandidate objects into
    one unified canonical candidate profile.
    """
    SOURCE_PRIORITY = {
    "resume": 4,
    "linkedin": 3,
    "github": 2,
    "csv": 1,
    }
    def _resolve_conflict(self,
    current_value,
    current_source,
    incoming_value,
    incoming_source,):
        """
        Resolves conflicts between two scalar values.

        Priority:
        1. Higher priority source wins.
        2. If same priority, choose more complete value.
        """

        if incoming_value is None:
            return current_value

        if current_value is None:
            return incoming_value

        if current_value == incoming_value:
            return current_value

        current_priority = self.SOURCE_PRIORITY.get(
            current_source,
            0,
        )

        incoming_priority = self.SOURCE_PRIORITY.get(
            incoming_source,
            0,
        )

        if incoming_priority > current_priority:
            return incoming_value

        if current_priority > incoming_priority:
            return current_value

        # Same priority → choose longer value
        if len(str(incoming_value)) > len(str(current_value)):
            return incoming_value

        return current_value
    

    def merge(
        self,
        candidates: list[ParsedCandidate]
    ) -> ParsedCandidate:

        if not candidates:
            raise ValueError("No candidates provided.")

        canonical = deepcopy(candidates[0])

        canonical.candidate_id = str(uuid.uuid4())

        for candidate in candidates[1:]:

            canonical.full_name = self._merge_value(
                canonical.full_name,
                canonical.source,
                candidate.full_name,
                candidate.source,
            )

            canonical.headline = self._merge_value(
                canonical.headline,
                canonical.source,
                candidate.headline,
                candidate.source,
            )

            canonical.location = self._merge_location(
                canonical.location,
                candidate.location
            )

            canonical.years_experience = max(
                canonical.years_experience or 0,
                candidate.years_experience or 0
            )

            canonical.emails = self._merge_list(
                canonical.emails,
                candidate.emails
            )

            canonical.phones = self._merge_list(
                canonical.phones,
                candidate.phones
            )

            canonical.skills = self._merge_list(
                canonical.skills,
                candidate.skills
            )

            canonical.certifications = self._merge_list(
                canonical.certifications,
                candidate.certifications
            )

            canonical.Achievements = self._merge_list(
                canonical.Achievements,
                candidate.Achievements
            )

            canonical.links = self._merge_links(
                canonical.links,
                candidate.links
            )

            canonical.experience = self._merge_experience(
                canonical.experience,
                candidate.experience
            )

            canonical.education = self._merge_education(
                canonical.education,
                candidate.education
            )

            canonical.projects = self._merge_projects(
                canonical.projects,
                candidate.projects
            )

        return canonical


    def _merge_value(self,existing,existing_source,incoming,incoming_source,): 
        return self._resolve_conflict(
        existing,
        existing_source,
        incoming,
        incoming_source,)
    

    def _merge_list(self, existing, incoming):

        existing = existing or []
        incoming = incoming or []

        merged = []

        seen = set()

        for item in existing + incoming:

            key = str(item).lower()

            if key in seen:
                continue

            seen.add(key)

            merged.append(item)

        return merged

    ##########################################################
    # Location
    ##########################################################

    def _merge_location(self, loc1, loc2):

        if not loc1:
            return loc2

        if not loc2:
            return loc1

        result = {}

        for key in ["city", "region", "country"]:

            value1 = loc1.get(key)
            value2 = loc2.get(key)

            if value1 and value2:

                result[key] = (
                    value1
                    if len(str(value1)) >= len(str(value2))
                    else value2
                )

            else:

                result[key] = value1 or value2

        return result

    

    def _merge_links(self, links1, links2):

        links1 = links1 or []
        links2 = links2 or []

        merged = []

        seen = set()

        for link in links1 + links2:

            if not isinstance(link, dict):
                continue

            key = link.get("url")

            if key in seen:
                continue

            seen.add(key)

            merged.append(link)

        return merged

    

    def _merge_experience(self, exp1, exp2):

        merged = {}

        for exp in (exp1 or []) + (exp2 or []):

            key = (
                exp.get("company"),
                exp.get("start"),
                exp.get("end"),
            )

            if key not in merged:

                merged[key] = exp

                continue

            existing = merged[key]

            if len(
                str(exp.get("title", ""))
            ) > len(
                str(existing.get("title", ""))
            ):

                existing["title"] = exp["title"]

            if exp.get("summary"):

                existing["summary"] = exp.get("summary")

        return list(merged.values())



    def _merge_education(self, edu1, edu2):

        merged = {}

        for edu in (edu1 or []) + (edu2 or []):

            key = (
                edu.get("institution"),
                edu.get("degree"),
            )

            if key not in merged:

                merged[key] = edu

                continue

            existing = merged[key]

            for field in [
                "cgpa",
                "field",
                "duration",
                "end_year",
            ]:

                if not existing.get(field):

                    existing[field] = edu.get(field)

        return list(merged.values())
        


    def _merge_projects(self, p1, p2):

        merged = {}

        for project in (p1 or []) + (p2 or []):

            title = project.get("title")

            if title not in merged:

                merged[title] = project

                continue

            existing = merged[title]

            if (
                len(
                    str(project.get("tech_stack", ""))
                )
                >
                len(
                    str(existing.get("tech_stack", ""))
                )
            ):

                existing["tech_stack"] = project["tech_stack"]

        return list(merged.values())