from src.application.schemas.extraction import CandidateProfile
from src.application.schemas.evaluation import ProfileEvaluationResult
from src.observability.tracing import get_tracer

tracer = get_tracer(__name__)

class ProfileEvaluator:
    def evaluate(self, profile: CandidateProfile) -> ProfileEvaluationResult:
        """
        Evaluates the parsed candidate profile to score it on completeness, quality,
        and assign confidence estimations.
        """
        with tracer.start_as_current_span("ProfileEvaluator.evaluate"):
            warnings = []
            issues = []
            
            # Contact confidence & completeness
            contact_score = 0.0
            if profile.first_name and profile.last_name: contact_score += 0.4
            if profile.email: contact_score += 0.4
            if profile.phone: contact_score += 0.2
            
            if contact_score < 0.5:
                warnings.append("Low contact information extracted.")
            if not profile.email and not profile.phone:
                issues.append("No email or phone number found.")
                
            # Education
            edu_score = 1.0 if profile.education else 0.0
            if not profile.education:
                warnings.append("No education history found.")
                
            # Experience
            exp_score = 1.0 if profile.experience else 0.0
            if not profile.experience:
                warnings.append("No work experience found.")
                
            # Skills
            skills_score = 1.0 if profile.skills else 0.0
            if not profile.skills:
                warnings.append("No skills extracted.")
                
            # Completeness aggregate
            completeness = (contact_score * 0.4) + (edu_score * 0.2) + (exp_score * 0.3) + (skills_score * 0.1)
            
            # Overall confidence (heuristic: high if we got standard sections)
            overall_conf = completeness * 0.95  # Slightly degraded as we are using heuristics
            
            return ProfileEvaluationResult(
                confidence_score=overall_conf,
                completeness_score=completeness,
                quality_score=completeness,  # Placeholder, could integrate an LLM review later
                warnings=warnings,
                issues=issues,
                contact_confidence=contact_score,
                education_confidence=edu_score,
                experience_confidence=exp_score,
                skills_confidence=skills_score
            )
