import csv
from pathlib import Path
from typing import List

from .base_parser import BaseParser
from src.models.parsed_candidate import ParsedCandidate


class CSVParser(BaseParser):
    """
    Parser for recruiter CSV files.

    Expected Columns:
        name
        email
        phone
        current_company
        title
    """

    REQUIRED_COLUMNS = {
        "name",
        "email",
        "phone",
        "current_company",
        "title",
    }

    def parse(self, source: str) -> List[ParsedCandidate]:

        path = Path(source)

        if not path.exists():
            raise FileNotFoundError(f"CSV file not found: {source}")

        if path.suffix.lower() != ".csv":
            raise ValueError("Input must be a CSV file.")

        candidates = []

        with open(
            path,
            mode="r",
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise ValueError("CSV file is empty.")

            columns = {
                column.strip().lower()
                for column in reader.fieldnames
            }

            missing = self.REQUIRED_COLUMNS - columns

            if missing:
                raise ValueError(
                    f"Missing columns: {', '.join(sorted(missing))}"
                )

            for row in reader:

                if self._is_empty_row(row):
                    continue

                candidate = ParsedCandidate(

                    source="csv",

                    full_name=self._get_value(row, "name"),

                    emails=self._get_list(row, "email"),

                    phones=self._get_list(row, "phone"),

                    experience=self._build_experience(row)

                )

                candidates.append(candidate)

        return candidates

    def _build_experience(self, row):

        company = self._get_value(row, "current_company")
        title = self._get_value(row, "title")

        if company is None and title is None:
            return []

        return [

            {
                "company": company,
                "title": title,
                "duration": None
            }

        ]

    def _get_value(self, row, key):

        value = row.get(key)

        if value is None:
            return None

        value = value.strip()

        return value if value else None

    def _get_list(self, row, key):

        value = self._get_value(row, key)

        if value is None:
            return []

        return [value]

    def _is_empty_row(self, row):

        return all(
            value is None or str(value).strip() == ""
            for value in row.values()
        )