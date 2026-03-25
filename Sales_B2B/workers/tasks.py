from workers.celery_app import app

MOCK_PROSPECTS = {
    "1": {"linkedin": "VP of Sales at CloudScale", "intent": "High - 5x Whitepaper downloads"},
    "2": {"linkedin": "Data Engineer at TechLib", "intent": "Medium - 2x Demo views"},
    "3": {"linkedin": "CTO at StartUp Inc", "intent": "High - Pricing page visited"},
    "4": {"linkedin": "Product Manager at GlobalCo", "intent": "Low - Email unsubscribed"},
    "5": {"linkedin": "Head of Ops at FinTech", "intent": "High - Attended Webinar"},
    "6": {"linkedin": "Architect at BuildIt", "intent": "Medium - 1x Whitepaper download"},
    "7": {"linkedin": "CEO at Solved", "intent": "High - Contact Sales form filled"},
    "8": {"linkedin": "Director at MediaHouse", "intent": "Low - Old lead re-activated"},
    "9": {"linkedin": "HR Lead at PeopleFirst", "intent": "Medium - 3x Blog reads"},
    "10": {"linkedin": "Consultant at AdviceGroup", "intent": "Low - No recent activity"},
    "11": {"linkedin": "Manager at StoreFront", "intent": "Medium - Cart abandoned"},
    "12": {"linkedin": "Lead Dev at CodeWorks", "intent": "High - API docs viewed"},
    "13": {"linkedin": "Founder at NewVentures", "intent": "High - 10x Site visits"},
    "14": {"linkedin": "Analyst at DataPoint", "intent": "Low - Social media click"},
    "15": {"linkedin": "Sales Lead at GrowthOrg", "intent": "High - Requested case study"}
}

@app.task(name="workers.tasks.gather_linkedin_signal")
def gather_linkedin_signal(pid: str):
    data = MOCK_PROSPECTS.get(pid, {"linkedin": "Unknown Profile"})
    return {"linkedin": data["linkedin"]}

@app.task(name="workers.tasks.gather_intent_signal")
def gather_intent_signal(pid: str):
    data = MOCK_PROSPECTS.get(pid, {"intent": "No activity detected"})
    return {"intent": data["intent"]}