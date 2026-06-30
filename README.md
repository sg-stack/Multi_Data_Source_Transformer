# Candidate Transformer

A modular multi-source candidate profile generator that ingests candidate information from different sources such as Resume (PDF/DOCX), CSV, GitHub, and LinkedIn, normalizes the extracted data, resolves conflicts, merges duplicate information into a unified canonical profile, computes confidence and provenance, and finally projects the output according to a configurable schema.

---

## Project Structure

```
candidate-transformer/
│
├── config/
│   ├── config.json
│
├── sample_inputs/
│   ├── resume.pdf
│   ├── recruiter.csv
│
├── sample_outputs/
    ├── canonical_profile.json
├── src/
│   ├── parsers/
│   │   ├── base_parser.py
│   │   ├── resume_parser.py
│   │   ├── csv_parser.py
│   │   ├── github_parser.py
│   │   ├── linkedin_parser.py
│   │
│   ├── normalizers/
│   │   └── normalizer.py
│   │
│   ├── merger/
│   │   └── merger.py
│   │
│   ├── confidence/
│   │   └── confidence_calculator.py
│   │
│   ├── provenance/
│   │   └── provenance_tracker.py
│   │
│   ├── projection/
│   │   └── projector.py
│   │
│   ├── models/
│   │   └── parsed_candidate.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Features

- Parse Resume (PDF / DOCX)
- Parse Structured CSV
- Parse GitHub Profile
- Parse LinkedIn Profile
- Data Normalization
- Duplicate Detection
- Conflict Resolution
- Candidate Profile Merging
- Confidence Calculation
- Provenance Tracking
- Configurable Output Projection
- Canonical JSON Generation

---

## Pipeline

```
Resume
CSV
GitHub
LinkedIn
      │
      ▼
Parsers
      │
      ▼
Normalizer
      │
      ▼
Merger
      │
      ▼
Confidence Calculator
      │
      ▼
Provenance Tracker
      │
      ▼
Projection Layer
      │
      ▼
Canonical Candidate Profile
```

---

## Installation

Clone the repository

```bash
git clone <repository_url>
```

Move into the project

```bash
cd Multi_Data_Source_Transformer
```


Install dependencies

```bash
pip install -r requirements.txt
```

---

## Input Files

Place your files inside

```
sample_inputs/
```

Example

```
sample_inputs/
    resume.pdf
    recruiter.csv
```

---

## Configuration

Projection configuration is stored inside

```
config/default_config.json
```

The configuration supports

- Selecting output fields
- Renaming fields
- Nested field mapping
- Missing field policy
- Confidence toggle
- Provenance toggle

Example

```json
{
    "fields": [
        {
            "path": "candidate_name",
            "from": "full_name"
        },
        {
            "path": "primary_email",
            "from": "emails[0]"
        }
    ],
    "include_confidence": true,
    "include_provenance": true,
    "on_missing": "null"
}
```

---

## Running the Project

Execute

```bash
python main.py
```

---

## Output

After successful execution

```
sample_outputs/
```

will contain

```
canonical_profile.json
```

Example

```json
{
    "candidate_id": "...",
    "full_name": "John Doe",
    "emails": [
        "john@gmail.com"
    ],
    "phones": [
        "+919876543210"
    ],
    "skills": [
        "Python",
        "React"
    ]
}
```

---

## Conflict Resolution Policy

When conflicting information exists across sources, the following priority is used

```
Resume
   ↓
LinkedIn
   ↓
GitHub
   ↓
CSV
```

If two sources have the same priority, the more complete value is selected.

Examples

- Longer full name preferred
- More detailed location preferred
- More descriptive job title preferred

---

## Deduplication Strategy

Duplicate information is removed during merging.

Examples

- Duplicate emails
- Duplicate phone numbers
- Duplicate skills
- Duplicate certifications
- Duplicate education entries
- Duplicate projects

---

## Normalization

The normalizer performs

- Email normalization
- Phone normalization (E.164)
- Country normalization (ISO-3166 Alpha-2)
- Skill canonicalization
- Date normalization
- Whitespace cleanup
- Duplicate removal

---

## Confidence Calculation

Confidence is computed using

- Source reliability
- Data quality
- Completeness
- Validation score

An overall profile confidence is generated.

---

## Provenance

Every merged field stores its origin.

Example

```json
{
    "emails": {
        "john@gmail.com": [
            "resume",
            "csv"
        ]
    }
}
```

---

## Supported Input Sources

- Resume (.pdf)
- Resume (.docx)
- CSV
- GitHub
- LinkedIn

---

## Technologies Used

- Python 3
- pdfplumber
- python-docx
- dataclasses
- Regular Expressions
- JSON

---

## Author

Shrinivasan S G