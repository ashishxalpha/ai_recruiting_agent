from src.domain.organization_models import OrganizationRole

class ResumeIntelligenceLead(OrganizationRole):
    title: str = "Resume Intelligence Lead"
    assigned_skills: list[str] = [
        "ParseResume",
        "NormalizeSkills",
        "GenerateProfile",
        "ValidateProfile",
        "GenerateEmbeddings"
    ]

class CandidateIntelligenceLead(OrganizationRole):
    title: str = "Candidate Intelligence Lead"
    assigned_skills: list[str] = [
        "SemanticSearch",
        "RankCandidates",
        "ExplainRanking",
        "EvaluateCandidate"
    ]

class RecruiterAssistantLead(OrganizationRole):
    title: str = "Recruiter Assistant Lead"
    assigned_skills: list[str] = [
        "Summarize",
        "Compare",
        "QuestionAnswering",
        "Recommendation"
    ]

class InterviewOperationsLead(OrganizationRole):
    title: str = "Interview Operations Lead"
    assigned_skills: list[str] = [
        "ScheduleInterview",
        "FindAvailability",
        "CreateInterviewPlan",
        "ReminderGeneration"
    ]

class CommunicationLead(OrganizationRole):
    title: str = "Communication Lead"
    assigned_skills: list[str] = [
        "DraftCommunication",
        "ReviewCommunication",
        "SendCommunication",
        "TrackResponses"
    ]
