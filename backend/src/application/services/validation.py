from src.application.schemas.extraction import CandidateProfile
from src.domain.exceptions import ValidationFailedException
from src.observability.tracing import get_tracer

tracer = get_tracer(__name__)

class CandidateProfileValidator:
    def validate(self, profile: CandidateProfile) -> CandidateProfile:
        """
        Validates business rules that Pydantic typing might miss.
        Raises ValidationFailedException if critical issues are found.
        """
        with tracer.start_as_current_span("CandidateProfileValidator.validate"):
            # Example rule: Can't have completely empty names if email/phone are missing
            if not profile.first_name and not profile.last_name and not profile.email and not profile.phone:
                raise ValidationFailedException("Profile has no identifiable contact information.")
            
            # Example rule: deduplicate skills (case-insensitive)
            seen_skills = set()
            unique_skills = []
            for skill in profile.skills:
                skill_lower = skill.name.lower().strip()
                if skill_lower not in seen_skills:
                    seen_skills.add(skill_lower)
                    unique_skills.append(skill)
            profile.skills = unique_skills
            
            # Example rule: Date consistency
            for exp in profile.experience:
                if exp.start_date and exp.end_date and exp.start_date > exp.end_date:
                    # Instead of failing, we can flip them or clear them.
                    # Or raise an exception if strictness is required.
                    # Here we flip for recovery.
                    exp.start_date, exp.end_date = exp.end_date, exp.start_date
                    
            return profile
