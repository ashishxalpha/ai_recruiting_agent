import pytest
from src.application.schemas.extraction import CandidateProfile, Skill, Experience
from src.application.services.validation import CandidateProfileValidator
from src.application.services.evaluation import ProfileEvaluator
from src.domain.exceptions import ValidationFailedException
from datetime import date

def test_validator_success():
    validator = CandidateProfileValidator()
    profile = CandidateProfile(
        first_name="Jane", last_name="Doe",
        skills=[Skill(name="Python"), Skill(name="python "), Skill(name="Java")]
    )
    validated = validator.validate(profile)
    assert len(validated.skills) == 2
    assert validated.skills[0].name == "Python"
    assert validated.skills[1].name == "Java"

def test_validator_fails_missing_contact():
    validator = CandidateProfileValidator()
    profile = CandidateProfile(skills=[Skill(name="Python")])
    with pytest.raises(ValidationFailedException):
        validator.validate(profile)

def test_validator_date_flip():
    validator = CandidateProfileValidator()
    profile = CandidateProfile(
        first_name="Jane", last_name="Doe",
        experience=[Experience(company="Acme", title="Engineer", start_date=date(2023,1,1), end_date=date(2020,1,1))]
    )
    validated = validator.validate(profile)
    assert validated.experience[0].start_date == date(2020,1,1)
    assert validated.experience[0].end_date == date(2023,1,1)

def test_evaluator():
    evaluator = ProfileEvaluator()
    profile = CandidateProfile(
        first_name="Jane", last_name="Doe", email="jane@test.com", phone="123",
        skills=[Skill(name="Python")]
    )
    result = evaluator.evaluate(profile)
    assert result.contact_confidence == 1.0
    assert result.skills_confidence == 1.0
    assert result.education_confidence == 0.0
    assert result.experience_confidence == 0.0
    assert len(result.warnings) == 2
    assert result.completeness_score == 0.5  # 0.4(contact) + 0.1(skills)
