from src.models.parsed_candidate import ParsedCandidate


class ProvenanceTracker:
    """
    Tracks the origin of every field in the
    canonical candidate profile.
    """

    def generate(
        self,
        merged_candidate: ParsedCandidate,
        source_candidates: list[ParsedCandidate],
    ) -> dict:

        provenance = {}

        provenance["full_name"] = self._find_source(
            merged_candidate.full_name,
            source_candidates,
            "full_name",
        )

        provenance["emails"] = self._find_list_sources(
            merged_candidate.emails,
            source_candidates,
            "emails",
        )

        provenance["phones"] = self._find_list_sources(
            merged_candidate.phones,
            source_candidates,
            "phones",
        )

        provenance["location"] = self._find_location_source(
            merged_candidate.location,
            source_candidates,
        )

        provenance["headline"] = self._find_source(
            merged_candidate.headline,
            source_candidates,
            "headline",
        )

        provenance["skills"] = self._find_list_sources(
            merged_candidate.skills,
            source_candidates,
            "skills",
        )

        provenance["experience"] = self._find_experience_sources(
            merged_candidate.experience,
            source_candidates,
        )

        provenance["education"] = self._find_education_sources(
            merged_candidate.education,
            source_candidates,
        )

        provenance["projects"] = self._find_project_sources(
            merged_candidate.projects,
            source_candidates,
        )

        provenance["certifications"] = self._find_list_sources(
            merged_candidate.certifications,
            source_candidates,
            "certifications",
        )

        provenance["links"] = self._find_link_sources(
            merged_candidate.links,
            source_candidates,
        )

        provenance["achievements"] = self._find_list_sources(
            merged_candidate.Achievements,
            source_candidates,
            "Achievements",
        )

        return provenance

    ##########################################################
    # Generic Value
    ##########################################################

    def _find_source(self, value, candidates, field):

        if value is None:
            return None

        for candidate in candidates:

            if getattr(candidate, field) == value:
                return candidate.source

        return "merged"

    ##########################################################
    # List Fields
    ##########################################################

    def _find_list_sources(self, values, candidates, field):

        result = {}

        if not values:
            return result

        for value in values:

            result[value] = []

            for candidate in candidates:

                field_values = getattr(candidate, field)

                if value in field_values:
                    result[value].append(candidate.source)

        return result

    ##########################################################
    # Location
    ##########################################################

    def _find_location_source(self, location, candidates):

        if not location:
            return None

        provenance = {}

        for key in ["city", "region", "country"]:

            provenance[key] = []

            for candidate in candidates:

                loc = candidate.location

                if (
                    loc
                    and loc.get(key)
                    and loc.get(key) == location.get(key)
                ):
                    provenance[key].append(candidate.source)

        return provenance

    ##########################################################
    # Experience
    ##########################################################

    def _find_experience_sources(self, experiences, candidates):

        provenance = []

        for exp in experiences:

            sources = []

            for candidate in candidates:

                for e in candidate.experience:

                    if (
                        e.get("company") == exp.get("company")
                        and
                        e.get("title") == exp.get("title")
                    ):

                        sources.append(candidate.source)

            provenance.append({

                "company": exp.get("company"),

                "title": exp.get("title"),

                "sources": sources

            })

        return provenance

    ##########################################################
    # Education
    ##########################################################

    def _find_education_sources(self, education, candidates):

        provenance = []

        for edu in education:

            sources = []

            for candidate in candidates:

                for e in candidate.education:

                    if (

                        e.get("institution") == edu.get("institution")

                        and

                        e.get("degree") == edu.get("degree")

                    ):

                        sources.append(candidate.source)

            provenance.append({

                "institution": edu.get("institution"),

                "degree": edu.get("degree"),

                "sources": sources

            })

        return provenance

    ##########################################################
    # Projects
    ##########################################################

    def _find_project_sources(self, projects, candidates):

        provenance = []

        for project in projects:

            sources = []

            for candidate in candidates:

                for p in candidate.projects:

                    if p.get("title") == project.get("title"):

                        sources.append(candidate.source)

            provenance.append({

                "title": project.get("title"),

                "sources": sources

            })

        return provenance

    ##########################################################
    # Links
    ##########################################################

    def _find_link_sources(self, links, candidates):

        provenance = []

        for link in links:

            sources = []

            for candidate in candidates:

                for l in candidate.links:

                    if l.get("url") == link.get("url"):

                        sources.append(candidate.source)

            provenance.append({

                "url": link.get("url"),

                "sources": sources

            })

        return provenance