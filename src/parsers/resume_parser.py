from pathlib import Path
import re
import pdfplumber
import docx
from .base_parser import BaseParser
from src.models.parsed_candidate import ParsedCandidate
from datetime import datetime

class ResumeParser(BaseParser):
    """
    Parser for PDF and DOCX resumes.
    """

    SUPPORTED_EXTENSIONS = {".pdf", ".docx"}
   

    def parse(self, source: str) -> ParsedCandidate:
        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(f"Resume not found: {source}")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported resume format: {path.suffix}. "
                f"Supported formats: {self.SUPPORTED_EXTENSIONS}"
            )

        text = self._extract_text(path)
        return ParsedCandidate(

            source="resume",

            full_name=self._extract_name(text),

            emails=self._extract_emails(text),

            phones=self._extract_phones(text),

            location=self._extract_location(text),

            headline=self._extract_headline(text),

            years_experience=self._extract_years_experience(text),

            skills=self._extract_skills(text),

            experience=self._extract_experience(text),

            education=self._extract_education(text),

            projects=self._extract_projects(text),

            certifications=self._extract_certifications(text),

            links=self._extract_links(text),

            Achievements=self._extract_achievements(text),
        )


    def _extract_text(self, path: Path) -> str:
        if path.suffix.lower() == ".pdf":
            return self._extract_pdf(path)

        if path.suffix.lower() == ".docx":
            return self._extract_docx(path)

        return ""

    def _extract_pdf(self, path: Path) -> str:
        text = []

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)

        return "\n".join(text)

    def _extract_docx(self, path: Path) -> str:
        document = docx.Document(path)

        paragraphs = []

        for para in document.paragraphs:
            if para.text.strip():
                paragraphs.append(para.text)

        return "\n".join(paragraphs)

    

    def _extract_name(self, text: str):
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        if lines:
            return lines[0].title()

        return None

    def _extract_emails(self, text: str):
        return list(
            set(
                re.findall(
                    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                    text,
                )
            )
        )

    def _extract_phones(self, text: str):
        phones = re.findall(
            r"(?:\+?\d{1,3}[- ]?)?(?:\d{10})",
            text,
        )

        return list(set(phones))

    def _extract_location(self, text: str):

        location = {
            "city": None,
            "region": None,
            "country": None
        }

        cities = {
            "Chennai": ("Tamil Nadu", "India"),
            "Coimbatore": ("Tamil Nadu", "India"),
            "Bangalore": ("Karnataka", "India"),
            "Hyderabad": ("Telangana", "India"),
            "Mumbai": ("Maharashtra", "India"),
            "Delhi": ("Delhi", "India"),
            "Pune": ("Maharashtra", "India")
        }

        for city in cities:

            if city.lower() in text.lower():

                region, country = cities[city]

                location["city"] = city
                location["region"] = region
                location["country"] = country

                break

        return location
    def _extract_headline(self, text: str):

        experience = self._extract_experience(text)

        if experience:
            return experience[0]["title"]

        return None

    def _extract_skills(self, text: str):

        section = re.search(
            r"Skills(.*?)Achievements",
            text,
            re.DOTALL | re.IGNORECASE,
        )

        if not section:
            return []

        block = section.group(1)

        skills = []

        for part in block.split("|"):

            if ":" in part:

                _, values = part.split(":", 1)

                skills.extend(

                    skill.strip()

                    for skill in values.split(",")

                    if skill.strip()

                )

        return sorted(list(set(skills)))
    
    
    
    
    def _extract_experience(self, text: str):

        experience = []

        section = re.search(
            r"Professional Experience(.*?)Projects",
            text,
            re.DOTALL | re.IGNORECASE,
        )

        if not section:
            return experience

        block = section.group(1)

        pattern = re.compile(
            r"([^\n,]+),\s*(.*?)\s+(\d{2}/\d{4}-\d{2}/\d{4}|\d{2}/\d{4}-Present)",
            re.MULTILINE,
        )

        for match in pattern.finditer(block):

            experience.append({

                "company": match.group(1).strip(),

                "title": match.group(2).strip(),

                "duration": match.group(3).strip()

            })

        return experience


    def _extract_education(self, text: str):

        education = []

        section = re.search(
            r"Education(.*?)Professional Experience",
            text,
            re.DOTALL | re.IGNORECASE,
        )

        if not section:
            return education

        block = section.group(1).strip()

        lines = [
            line.strip()
            for line in block.splitlines()
            if line.strip()
        ]

        if len(lines) < 2:
            return education

        degree = lines[0]
        institution = lines[1]

        duration = None
        cgpa = None

        duration_match = re.search(
            r"(\d{2}/\d{4}\s*[–-]\s*(?:Present|\d{2}/\d{4}))",
            degree
        )

        if duration_match:
            duration = duration_match.group(1)
            degree = degree.replace(duration, "").strip()

        cgpa_match = re.search(
            r"CGPA[: ]*([\d.]+)",
            institution,
            re.IGNORECASE
        )

        if cgpa_match:
            cgpa = cgpa_match.group(1)
            institution = re.sub(
                r"CGPA[: ]*[\d.]+",
                "",
                institution,
                flags=re.IGNORECASE
            ).strip()

        education.append({

            "degree": degree,

            "institution": institution,

            "duration": duration,

            "cgpa": cgpa

        })

        return education

    def _extract_projects(self, text: str):

        projects = []

        section = re.search(
            r"Projects(.*?)Certifications",
            text,
            re.DOTALL | re.IGNORECASE,
        )

        if not section:
            return projects

        lines = [
            line.strip()
            for line in section.group(1).splitlines()
            if line.strip()
        ]
        
        for line in lines:
            if "|" in line:
                v=line.split(",")
                projects.append({
                    "title":v[0],
                    "tech_stack":v[1]
                })

        return projects
        

    def _extract_certifications(self, text: str):

        certifications = []

        section = re.search(
            r"Certifications(.*?)Skills",
            text,
            re.DOTALL | re.IGNORECASE,
        )

        if not section:
            return certifications

        certs = section.group(1).replace("\n", " ")

        certifications = [

            cert.strip()

            for cert in certs.split("|")

            if cert.strip()

        ]

        return certifications
        
    def _extract_github_username(self, text: str):

        # Match full GitHub URL
        match = re.search(
            r"https?://(?:www\.)?github\.com/([A-Za-z0-9_-]+)",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

        # Match github.com/username
        match = re.search(
            r"github\.com/([A-Za-z0-9_-]+)",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

        # Match GitHub: username
        match = re.search(
            r"github\s*[:\-]?\s*([A-Za-z0-9_-]+)",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group(1)

        return None
    

    def _extract_linkedin_url(self, text: str):

        # Match complete LinkedIn URL
        match = re.search(
            r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9._\-]+/?",
            text,
            re.IGNORECASE,
        )

        if match:
            return match.group().rstrip("/")

        # Match linkedin.com/in/username
        match = re.search(
            r"linkedin\.com/in/[A-Za-z0-9._\-]+/?",
            text,
            re.IGNORECASE,
        )

        if match:
            url = match.group().rstrip("/")

            if not url.startswith("http"):
                url = "https://" + url

            return url

        return None
    

    def _extract_links(self, text: str):

        links = []

        github = self._extract_github_username(text)

        linkedin = self._extract_linkedin_url(text)

        if github:

            links.append({

                "type": "github",

                "url": f"https://github.com/{github}"

            })

        if linkedin:

            links.append({

                "type": "linkedin",

                "url": linkedin

            })

        return links
    

    def _extract_achievements(self, text: str):

        achievements = []

        lines = [
            line.strip()
            for line in text.splitlines()
        ]

        inside = False

        for line in lines:
            lower = line.lower()
            if lower == "achievements":
                inside = True
                continue

            if inside and "." in line:
                achievements.append(line)
            elif inside and "." not in line and "•"!=line:
                break
                

        return achievements
    
   

    

    def _extract_years_experience(self, text: str):

        experience = self._extract_experience(text)

        if not experience:
            return 0

        years = []

        for exp in experience:

            match = re.search(r"\d{4}", exp["duration"])

            if match:

                years.append(int(match.group()))

        if not years:
            return 0

        return datetime.now().year - min(years)