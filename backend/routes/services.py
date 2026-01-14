from fastapi import APIRouter, HTTPException
from models.schemas import ServiceInfo
from typing import List

router = APIRouter()

# K2 Communications Services Data
K2_SERVICES = [
    {
        "id": "pr-consultancy",
        "name": "PR Consultancy",
        "description": "Strategic public relations consultancy to build and maintain your brand's reputation",
        "key_features": [
            "Media relations and outreach",
            "Brand positioning and messaging",
            "Strategic communication planning",
            "Executive visibility programs"
        ],
        "use_cases": [
            "Brand launches",
            "Corporate communications",
            "Thought leadership campaigns"
        ]
    },
    {
        "id": "crisis-management",
        "name": "Reputation & Crisis Management",
        "description": "Proactive and reactive crisis management to protect and restore your brand reputation",
        "key_features": [
            "24/7 crisis response",
            "Reputation monitoring",
            "Crisis communication strategies",
            "Stakeholder management"
        ],
        "use_cases": [
            "Product recalls",
            "Negative media coverage",
            "Social media crises"
        ]
    },
    {
        "id": "digital-marketing",
        "name": "Digital & Social Media Marketing",
        "description": "Comprehensive digital marketing strategies to amplify your brand's online presence",
        "key_features": [
            "Social media strategy and management",
            "Content creation and curation",
            "Influencer partnerships",
            "Digital campaign execution"
        ],
        "use_cases": [
            "Brand awareness campaigns",
            "Product launches",
            "Community building"
        ]
    },
    {
        "id": "content-development",
        "name": "Content Development",
        "description": "High-quality content creation tailored to your brand voice and audience",
        "key_features": [
            "Press releases",
            "Blog posts and articles",
            "Website content",
            "Marketing collateral"
        ],
        "use_cases": [
            "Thought leadership content",
            "SEO-optimized articles",
            "Product announcements"
        ]
    },
    {
        "id": "market-research",
        "name": "Market Research",
        "description": "In-depth market research and analysis to inform your communication strategies",
        "key_features": [
            "Competitive analysis",
            "Audience insights",
            "Media landscape analysis",
            "Trend identification"
        ],
        "use_cases": [
            "Market entry strategies",
            "Campaign planning",
            "Brand positioning"
        ]
    },
    {
        "id": "translation",
        "name": "Translation Services",
        "description": "Professional translation services for multilingual campaigns across India",
        "key_features": [
            "Regional language translation",
            "Cultural adaptation",
            "Localization services",
            "Quality assurance"
        ],
        "use_cases": [
            "Pan-India campaigns",
            "Regional market entry",
            "Multilingual content"
        ]
    }
]

@router.get("/", response_model=List[ServiceInfo])
async def get_all_services():
    """
    Get all services offered by K2 Communications.
    """
    return K2_SERVICES

@router.get("/{service_id}", response_model=ServiceInfo)
async def get_service_details(service_id: str):
    """
    Get detailed information about a specific service.
    """
    service = next((s for s in K2_SERVICES if s["id"] == service_id), None)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service
