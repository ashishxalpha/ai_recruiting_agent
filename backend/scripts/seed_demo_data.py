import asyncio
import os
import sys
import uuid
from datetime import datetime, timezone
import hashlib
import openai
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

# Ensure backend directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.infrastructure.database.models import (
    UserModel,
    JobRequirementModel,
    JobRequirementEmbeddingModel,
    CandidateModel,
    CandidateSkillModel,
    CandidateEducationModel,
    CandidateExperienceModel,
    CandidateEmbeddingModel,
    SearchSessionModel,
    CandidateMatchModel,
    RecruiterFeedbackModel,
    AuditLogModel
)
from src.infrastructure.auth.security import hash_password
from src.domain.enums import CandidateStatus, RecruiterDecision

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required to run seed_demo_data.py.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def get_embedding(text: str) -> list[float]:
    if openai_client:
        try:
            response = openai_client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"   [WARN] OpenAI embedding call failed ({e}), generating fallback unit vector.")
    import numpy as np
    vec = np.random.randn(1536).astype(float)
    return (vec / np.linalg.norm(vec)).tolist()

async def seed_data():
    print("=== SEEDING ENTERPRISE DEMO DATA ===")
    engine = create_async_engine(DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with session_factory() as session:
        # 1. Seed Users
        print("\n1. Seeding Users...")
        users_data = [
            {
                "email": "ashish@example.com",
                "first_name": "Ashish",
                "last_name": "Kumar",
                "role": "recruiter",
                "password": "Recruiter123!"
            },
            {
                "email": "admin@example.com",
                "first_name": "Admin",
                "last_name": "User",
                "role": "admin",
                "password": "Admin123!"
            }
        ]
        seeded_users = {}
        for u in users_data:
            stmt = select(UserModel).where(UserModel.email == u["email"])
            existing = (await session.execute(stmt)).scalars().first()
            if not existing:
                user = UserModel(
                    email=u["email"],
                    hashed_password=hash_password(u["password"]),
                    first_name=u["first_name"],
                    last_name=u["last_name"],
                    role=u["role"],
                    is_active=True
                )
                session.add(user)
                await session.flush()
                seeded_users[u["email"]] = user
                print(f"   Created user: {u['email']} ({u['role']})")
            else:
                seeded_users[u["email"]] = existing
                print(f"   User {u['email']} already exists.")

        # 2. Seed Job Requisitions
        print("\n2. Seeding Job Requisitions...")
        jobs_data = [
            {
                "title": "Senior Backend Engineer (Python & Distributed Systems)",
                "description": "Architect high-throughput asynchronous microservices handling millions of events daily. Expertise in Python, FastAPI, PostgreSQL, Kafka, and Kubernetes required.",
                "skills_required": ["Python", "FastAPI", "PostgreSQL", "Distributed Systems", "Kafka", "Docker", "Kubernetes", "AsyncIO", "Redis"],
                "experience_required": "5+ years of production experience in distributed backend architectures.",
                "status": "ACTIVE",
                "department": "Platform Engineering",
                "location": "San Francisco, CA (Hybrid)",
                "employment_type": "Full-Time",
                "hiring_manager": "Sarah Connor"
            },
            {
                "title": "Lead AI / ML Systems Engineer (LLM Agents & RAG)",
                "description": "Design autonomous multi-agent pipelines, RAG retrieval architectures, and agentic workflows using LangGraph, pgvector, and frontier LLMs.",
                "skills_required": ["Python", "PyTorch", "LangGraph", "LangChain", "OpenAI API", "pgvector", "Vector Databases", "RAG Architecture", "Prompt Engineering"],
                "experience_required": "4+ years in machine learning and 2+ years deploying LLM/agentic applications.",
                "status": "ACTIVE",
                "department": "Artificial Intelligence",
                "location": "New York, NY (Remote)",
                "employment_type": "Full-Time",
                "hiring_manager": "Ashish Kumar"
            },
            {
                "title": "Staff Full-Stack Engineer (Next.js & Cloud Platforms)",
                "description": "Lead the frontend and API integrations for modern enterprise AI products. Deep expertise in React, Next.js App Router, TypeScript, TailwindCSS, and cloud-native containerized deployments.",
                "skills_required": ["TypeScript", "Next.js", "React", "TailwindCSS", "Node.js", "Python", "GraphQL", "Azure Container Apps", "REST APIs"],
                "experience_required": "6+ years building scalable web applications and cloud architectures.",
                "status": "ACTIVE",
                "department": "Product Engineering",
                "location": "Seattle, WA (Hybrid)",
                "employment_type": "Full-Time",
                "hiring_manager": "Elena Vance"
            }
        ]

        seeded_jobs = []
        for j in jobs_data:
            stmt = select(JobRequirementModel).where(JobRequirementModel.title == j["title"])
            existing_job = (await session.execute(stmt)).scalars().first()
            if not existing_job:
                job = JobRequirementModel(
                    title=j["title"],
                    description=j["description"],
                    skills_required=j["skills_required"],
                    experience_required=j["experience_required"],
                    status=j["status"],
                    department=j["department"],
                    location=j["location"],
                    employment_type=j["employment_type"],
                    hiring_manager=j["hiring_manager"]
                )
                session.add(job)
                await session.flush()
                seeded_jobs.append(job)
                print(f"   Created Job: {job.title}")

                # Create Embedding
                print(f"   Generating OpenAI vector embedding for {job.title}...")
                embed_text = f"{job.title} {job.description} {' '.join(job.skills_required)}"
                vec = get_embedding(embed_text)
                job_emb = JobRequirementEmbeddingModel(
                    job_requirement_id=job.id,
                    embedding_type="full_profile",
                    embedding_model="text-embedding-3-small",
                    embedding_version="v1",
                    source_hash=hashlib.sha256(embed_text.encode()).hexdigest(),
                    vector_data=vec
                )
                session.add(job_emb)
            else:
                seeded_jobs.append(existing_job)
                print(f"   Job {existing_job.title} already exists.")

        # 3. Seed Candidates
        print("\n3. Seeding Candidates & Profiles...")
        candidates_data = [
            {
                "first_name": "Elena",
                "last_name": "Rostova",
                "email": "elena.rostova@example.com",
                "phone": "+1 (415) 555-0192",
                "summary": "Senior Distributed Systems & Backend Engineer with 7+ years of experience designing fault-tolerant distributed services in Python, Go, Kafka, and PostgreSQL.",
                "status": CandidateStatus.NEW,
                "skills": [
                    ("Python", "expert"),
                    ("FastAPI", "expert"),
                    ("Distributed Systems", "expert"),
                    ("PostgreSQL", "advanced"),
                    ("Kafka", "advanced"),
                    ("Kubernetes", "advanced"),
                    ("Docker", "expert"),
                    ("AsyncIO", "expert")
                ],
                "experiences": [
                    ("Stripe", "Senior Software Engineer", datetime(2022, 1, 1, tzinfo=timezone.utc), None, "Architected high-throughput ledger services handling 50k ops/sec."),
                    ("Palantir Technologies", "Backend Engineer", datetime(2018, 6, 1, tzinfo=timezone.utc), datetime(2021, 12, 31, tzinfo=timezone.utc), "Designed distributed data pipeline ingestion engines in Python.")
                ],
                "education": [
                    ("Carnegie Mellon University", "M.S. Computer Science", "Computer Science", datetime(2016, 9, 1, tzinfo=timezone.utc), datetime(2018, 5, 1, tzinfo=timezone.utc))
                ]
            },
            {
                "first_name": "David",
                "last_name": "Chen",
                "email": "david.chen@example.com",
                "phone": "+1 (212) 555-0144",
                "summary": "Lead AI Systems Engineer specializing in Agentic Workflows, LangGraph, Multi-Vector RAG, and production LLM orchestration.",
                "status": CandidateStatus.NEW,
                "skills": [
                    ("Python", "expert"),
                    ("LangGraph", "expert"),
                    ("LangChain", "expert"),
                    ("OpenAI API", "expert"),
                    ("pgvector", "advanced"),
                    ("PyTorch", "advanced"),
                    ("RAG Architecture", "expert"),
                    ("Vector Databases", "expert")
                ],
                "experiences": [
                    ("Cohere", "AI Tech Lead", datetime(2022, 6, 1, tzinfo=timezone.utc), None, "Led development of enterprise multi-agent retrieval frameworks."),
                    ("Scale AI", "Machine Learning Engineer", datetime(2019, 8, 1, tzinfo=timezone.utc), datetime(2022, 5, 31, tzinfo=timezone.utc), "Engineered fine-tuning and evaluation pipelines for reasoning models.")
                ],
                "education": [
                    ("Stanford University", "B.S. Artificial Intelligence", "Computer Science", datetime(2015, 9, 1, tzinfo=timezone.utc), datetime(2019, 6, 1, tzinfo=timezone.utc))
                ]
            },
            {
                "first_name": "Sarah",
                "last_name": "Jenkins",
                "email": "sarah.jenkins@example.com",
                "phone": "+1 (206) 555-0178",
                "summary": "Staff Full-Stack Engineer with a passion for high-performance Next.js web applications, design systems, and cloud architectures.",
                "status": CandidateStatus.NEW,
                "skills": [
                    ("TypeScript", "expert"),
                    ("Next.js", "expert"),
                    ("React", "expert"),
                    ("TailwindCSS", "expert"),
                    ("Python", "advanced"),
                    ("Azure Container Apps", "advanced"),
                    ("Node.js", "expert")
                ],
                "experiences": [
                    ("Vercel", "Staff Engineer", datetime(2021, 3, 1, tzinfo=timezone.utc), None, "Built foundational layout engines and telemetry tooling for Next.js App Router."),
                    ("GitHub", "Senior Frontend Engineer", datetime(2017, 9, 1, tzinfo=timezone.utc), datetime(2021, 2, 28, tzinfo=timezone.utc), "Implemented accessibility and real-time collaboration UI.")
                ],
                "education": [
                    ("University of Washington", "B.S. Software Engineering", "Computer Science", datetime(2013, 9, 1, tzinfo=timezone.utc), datetime(2017, 6, 1, tzinfo=timezone.utc))
                ]
            },
            {
                "first_name": "Marcus",
                "last_name": "Vance",
                "email": "marcus.vance@example.com",
                "phone": "+1 (510) 555-0129",
                "summary": "Backend Engineer with 3 years building REST APIs, asynchronous database pipelines, and microservices in Python and FastAPI.",
                "status": CandidateStatus.NEW,
                "skills": [
                    ("Python", "advanced"),
                    ("FastAPI", "advanced"),
                    ("PostgreSQL", "intermediate"),
                    ("Docker", "intermediate"),
                    ("Git", "advanced"),
                    ("Redis", "intermediate")
                ],
                "experiences": [
                    ("FinTech Innovations", "Backend Developer", datetime(2021, 7, 1, tzinfo=timezone.utc), None, "Maintained FastAPI endpoints and relational database schema migrations.")
                ],
                "education": [
                    ("UC Berkeley", "B.S. Computer Science", "Computer Science", datetime(2017, 9, 1, tzinfo=timezone.utc), datetime(2021, 5, 1, tzinfo=timezone.utc))
                ]
            },
            {
                "first_name": "Priya",
                "last_name": "Patel",
                "email": "priya.patel@example.com",
                "phone": "+1 (617) 555-0163",
                "summary": "Senior Machine Learning Engineer focusing on Vector Search, embeddings fine-tuning, and semantic matching systems.",
                "status": CandidateStatus.NEW,
                "skills": [
                    ("Python", "expert"),
                    ("pgvector", "expert"),
                    ("Vector Databases", "expert"),
                    ("PyTorch", "expert"),
                    ("LangChain", "advanced"),
                    ("RAG Architecture", "advanced")
                ],
                "experiences": [
                    ("Databricks", "Senior ML Engineer", datetime(2021, 10, 1, tzinfo=timezone.utc), None, "Optimized vector search indexing and sparse-dense hybrid retrieval."),
                    ("Allen Institute for AI", "Research Engineer", datetime(2019, 6, 1, tzinfo=timezone.utc), datetime(2021, 9, 30, tzinfo=timezone.utc), "Conducted semantic retrieval and cross-encoder evaluation research.")
                ],
                "education": [
                    ("MIT", "Ph.D. Computational Linguistics", "EECS", datetime(2015, 9, 1, tzinfo=timezone.utc), datetime(2019, 5, 1, tzinfo=timezone.utc))
                ]
            }
        ]

        seeded_candidates = []
        for c in candidates_data:
            stmt = select(CandidateModel).where(CandidateModel.email == c["email"])
            existing_c = (await session.execute(stmt)).scalars().first()
            if not existing_c:
                cand = CandidateModel(
                    first_name=c["first_name"],
                    last_name=c["last_name"],
                    email=c["email"],
                    phone=c["phone"],
                    summary=c["summary"],
                    status=c["status"]
                )
                session.add(cand)
                await session.flush()

                # Add Skills
                for sk_name, prof in c["skills"]:
                    session.add(CandidateSkillModel(
                        candidate_id=cand.id,
                        name=sk_name,
                        proficiency=prof
                    ))

                # Add Experience
                for comp, title, sdate, edate, desc in c["experiences"]:
                    session.add(CandidateExperienceModel(
                        candidate_id=cand.id,
                        company=comp,
                        title=title,
                        start_date=sdate,
                        end_date=edate,
                        description=desc
                    ))

                # Add Education
                for inst, deg, field, sdate, edate in c["education"]:
                    session.add(CandidateEducationModel(
                        candidate_id=cand.id,
                        institution=inst,
                        degree=deg,
                        field_of_study=field,
                        start_date=sdate,
                        end_date=edate
                    ))

                await session.flush()

                # Generate Real Vector Embeddings
                print(f"   Generating OpenAI vector embedding for {cand.first_name} {cand.last_name}...")
                profile_text = f"{cand.first_name} {cand.last_name} {cand.summary} {' '.join([s[0] for s in c['skills']])}"
                vec = get_embedding(profile_text)
                cand_emb = CandidateEmbeddingModel(
                    candidate_id=cand.id,
                    embedding_type="full_profile",
                    embedding_model="text-embedding-3-small",
                    embedding_version="v1",
                    source_hash=hashlib.sha256(profile_text.encode()).hexdigest(),
                    vector_data=vec
                )
                session.add(cand_emb)

                # Add Audit Log
                session.add(AuditLogModel(
                    entity_type="CANDIDATE",
                    entity_id=cand.id,
                    action="PROFILE_INGESTED",
                    changes={"email": cand.email, "name": f"{cand.first_name} {cand.last_name}"}
                ))

                seeded_candidates.append(cand)
                print(f"   Created Candidate: {cand.first_name} {cand.last_name}")
            else:
                seeded_candidates.append(existing_c)
                print(f"   Candidate {existing_c.email} already exists.")

        # 4. Seed Matches and Recruiter Feedback
        print("\n4. Seeding Matches and Recruiter Feedback...")
        if len(seeded_jobs) >= 3 and len(seeded_candidates) >= 5:
            # Job 0 (Senior Backend) matches: Elena Rostova (0.94), Marcus Vance (0.76)
            # Job 1 (Lead AI) matches: David Chen (0.97), Priya Patel (0.92)
            # Job 2 (Staff Full-Stack) matches: Sarah Jenkins (0.95)

            match_configs = [
                (seeded_jobs[0], seeded_candidates[0], 0.94, 0.96, 0.92, 0.94, RecruiterDecision.APPROVED, 0.96, "Exceptional distributed systems background and Kafka experience. Advance to technical loop."),
                (seeded_jobs[0], seeded_candidates[3], 0.76, 0.78, 0.72, 0.76, RecruiterDecision.SHORTLISTED, 0.72, "Solid Python basics, but lacks the distributed systems scale needed for senior level."),
                (seeded_jobs[1], seeded_candidates[1], 0.97, 0.98, 0.96, 0.97, RecruiterDecision.APPROVED, 0.98, "Outstanding LangGraph and agent orchestration portfolio. Strong technical leader."),
                (seeded_jobs[1], seeded_candidates[4], 0.92, 0.94, 0.90, 0.92, RecruiterDecision.APPROVED, 0.91, "Superb vector search, pgvector, and NLP research depth."),
                (seeded_jobs[2], seeded_candidates[2], 0.95, 0.96, 0.94, 0.95, RecruiterDecision.APPROVED, 0.95, "Deep Next.js App Router expertise and clean aesthetic engineering sensibility.")
            ]

            for job, cand, sem, sk, exp, final, dec, conf, notes in match_configs:
                # Create Search Session
                search_sess = SearchSessionModel(job_requirement_id=job.id)
                session.add(search_sess)
                await session.flush()

                # Create Match
                stmt_m = select(CandidateMatchModel).where(
                    CandidateMatchModel.candidate_id == cand.id,
                    CandidateMatchModel.search_session_id == search_sess.id
                )
                match = (await session.execute(stmt_m)).scalars().first()
                if not match:
                    match = CandidateMatchModel(
                        search_session_id=search_sess.id,
                        candidate_id=cand.id,
                        semantic_score=sem,
                        skills_score=sk,
                        experience_score=exp,
                        education_score=0.90,
                        quality_score=0.95,
                        final_score=final
                    )
                    session.add(match)
                    await session.flush()

                    # Recruiter Feedback
                    session.add(RecruiterFeedbackModel(
                        candidate_match_id=match.id,
                        decision=dec.value if hasattr(dec, 'value') else str(dec),
                        confidence=conf,
                        reason="Match Evaluation",
                        notes=notes
                    ))

                    # Audit Log
                    session.add(AuditLogModel(
                        entity_type="MATCH",
                        entity_id=match.id,
                        action=f"FEEDBACK_{dec.value}",
                        changes={"job": job.title, "candidate": cand.email, "score": final}
                    ))

                    print(f"   Created Match & Feedback: {cand.first_name} -> {job.title[:30]} ({final*100:.0f}%) [{dec.value}]")

        await session.commit()
        print("\n=== DEMO DATA SEEDED SUCCESSFULLY! ===")

if __name__ == "__main__":
    asyncio.run(seed_data())
