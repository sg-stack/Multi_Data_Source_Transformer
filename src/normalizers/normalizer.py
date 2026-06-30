import re
from copy import deepcopy

from src.models.parsed_candidate import ParsedCandidate


class Normalizer:

    """
    Converts extracted ParsedCandidate objects into
    standardized canonical representations.
    """

    COUNTRY_MAPPING = {

        "india": "IN",
        "united states": "US",
        "usa": "US",
        "uk": "GB",
        "united kingdom": "GB",
        "canada": "CA",
        "germany": "DE",
        "france": "FR",
        "australia": "AU",
        "singapore": "SG",
        "japan": "JP",
        "china": "CN"

    }

    SKILL_MAPPING = {

        "js": "JavaScript",
        "javascript": "JavaScript",
        "ts": "TypeScript",
        "node": "Node.js",
        "nodejs": "Node.js",
        "reactjs": "React",
        "react.js": "React",
        "py": "Python",
        "c++": "C++",
        "cpp": "C++",
        "ml": "Machine Learning",
        "dl": "Deep Learning",
        "ai": "Artificial Intelligence",
        "tf": "TensorFlow"

    }

    def normalize(
        self,
        candidate: ParsedCandidate
    ) -> ParsedCandidate:

        candidate = deepcopy(candidate)

        candidate.full_name = self.normalize_name(
            candidate.full_name
        )

        candidate.emails = self.normalize_emails(
            candidate.emails
        )

        candidate.phones = self.normalize_phones(
            candidate.phones
        )

        candidate.location = self.normalize_location(
            candidate.location
        )

        candidate.links = self.normalize_links(
            candidate.links
        )

        candidate.skills = self.normalize_skills(
            candidate.skills
        )

        candidate.experience = self.normalize_experience(
            candidate.experience
        )

        candidate.education = self.normalize_education(
            candidate.education
        )

        candidate.projects = self.normalize_projects(
            candidate.projects
        )

        candidate.certifications = self.normalize_certifications(
            candidate.certifications
        )

        return candidate
    def normalize_name(self, name):

        if not name:
            return None

        name = re.sub(r"\s+", " ", name)

        return name.strip().title()
    

    def normalize_emails(self, emails):

        if not emails:
            return []

        normalized = []

        for email in emails:

            email = email.strip().lower()

            if re.match(
                r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
                email
            ):

                if email not in normalized:
                    normalized.append(email)

        return normalized
    
    
    def normalize_phones(self, phones):

        if not phones:
            return []

        normalized = []

        for phone in phones:

            digits = re.sub(r"\D", "", phone)

            if len(digits) == 10:

                digits = "+91" + digits

            elif len(digits) == 12 and digits.startswith("91"):

                digits = "+" + digits

            elif len(digits) == 13 and digits.startswith("+91"):

                pass

            else:

                continue

            if digits not in normalized:
                normalized.append(digits)

        return normalized
    

    def normalize_location(self, location):

        if not location:

            return {

                "city": None,
                "region": None,
                "country": None

            }

        country = location.get("country")

        if country:

            country = self.COUNTRY_MAPPING.get(

                country.lower(),

                country

            )

        return {

            "city": location.get("city"),

            "region": location.get("region"),

            "country": country

        }
    

    def normalize_links(self, links):

        if not links:
            return []

        normalized = []

        seen = set()

        for link in links:

            if not isinstance(link, dict):
                continue

            link_type = link.get("type")
            url = link.get("url")

            if not url:
                continue

            url = url.strip()

            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            key = (link_type, url)

            if key in seen:
                continue

            seen.add(key)

            normalized.append({
                "type": link_type,
                "url": url
            })

        return normalized
    
    
    def normalize_skills(self, skills):

        if not skills:
            return []

        normalized = []

        seen = set()

        for skill in skills:

            if not skill:
                continue

            skill = skill.strip()

            canonical = self.SKILL_MAPPING.get(
                skill.lower(),
                skill.title()
            )

            if canonical in seen:
                continue

            seen.add(canonical)

            normalized.append(canonical)

        return normalized
    

    def normalize_experience(self, experiences):

        if not experiences:
            return []

        normalized = []

        for exp in experiences:

            if not isinstance(exp, dict):
                continue

            company = exp.get("company")
            title = exp.get("title")
            duration = exp.get("duration")

            start = None
            end = None

            if duration:

                matches = re.findall(
                    r"(\d{2})/(\d{4})",
                    duration
                )

                if len(matches) >= 1:

                    month, year = matches[0]

                    start = f"{year}-{month}"

                if len(matches) >= 2:

                    month, year = matches[1]

                    end = f"{year}-{month}"

                elif "present" in duration.lower():

                    end = "Present"

            normalized.append({

                "company": company,

                "title": title,

                "start": start,

                "end": end,

                "summary": exp.get("summary")

            })

        return normalized
    
    
    def normalize_education(self, education):

        if not education:
            return []

        normalized = []

        for edu in education:

            if not isinstance(edu, dict):
                continue

            end_year = None

            duration = edu.get("duration")

            if duration:

                years = re.findall(
                    r"\d{4}",
                    duration
                )

                if years:

                    end_year = years[-1]

            normalized.append({

                "institution": edu.get("institution"),

                "degree": edu.get("degree"),

                "field": edu.get("field"),

                "end_year": end_year

            })

        return normalized
    

    def normalize_projects(self, projects):

        if not projects:
            return []

        normalized = []

        seen = set()

        for project in projects:

            if not isinstance(project, dict):
                continue

            title = project.get("title")

            if not title:
                continue

            key = title.lower()

            if key in seen:
                continue

            seen.add(key)

            normalized.append({

                "title": title.strip(),

                "tech_stack": project.get("tech_stack")

            })

        return normalized
    

    def normalize_certifications(self, certifications):

        if not certifications:
            return []

        normalized = []

        seen = set()

        for cert in certifications:

            cert = cert.strip()

            if not cert:
                continue

            if cert.lower() in seen:
                continue

            seen.add(cert.lower())

            normalized.append(cert)

        return normalized