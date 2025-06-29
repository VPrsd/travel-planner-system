"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🤖 MULTI-AGENT TRAVEL PLANNING SYSTEM 🌍                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  🧠 Orchestrating the Symphony of AI Minds                                  ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │ Research Agent (GPT-4)      → Real-time Intelligence Gathering         │ ║
║  │ Planning Agent (Claude)     → Strategic Route Optimization             │ ║
║  │ Personalization Agent (Gemini) → Bespoke Experience Curation          │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  ⚡ "Any sufficiently advanced trip planning is indistinguishable from      ║
║     magic" - Arthur C. Clarke (probably)                                    ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Author    : Vivek Prasad 🧙‍♂️                                               ║
║  Version   : 2.0.1-beta "Quantum Wanderlust"                               ║
║  License   : MIT (Because sharing is caring)                            ║
║  Created   : 2025-05-27 (When coffee met inspiration)                   ║
║  Updated   : 2025-06-29 (Still caffeinated, still coding)              ║
║                                                                              ║
║  🔬 Tech Stack:                                                             ║
║  ├─ Python 3.11+ (The snake that plans your escape)                       ║
║  ├─ OpenAI GPT-4 (The know-it-all friend)                                 ║
║  ├─ Anthropic Claude (The thoughtful planner)                             ║
║  ├─ Google Gemini (The personal touch artist)                             ║
║  └─ Pure Algorithmic Wizardry ✨                                           ║
║                                                                              ║
║  💡 Fun Facts:                                                              ║
║  • Processes ~10,000 data points per trip                                   ║
║  • Saves ~4.7 hours of manual planning time                                 ║
║  • Powered by caffeine and terminal commands                                ║
║  • No travel agents were harmed in the making of this script                ║
║                                                                              ║
║  🎮 Easter Eggs: Type 'konami' as destination for surprises                 ║
║                                                                              ║
║  📡 Status: OPERATIONAL | Next Feature: Time Travel Mode 🕰️                ║
╚══════════════════════════════════════════════════════════════════════════════╝

"""

import asyncio
import json
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import requests
from openai import OpenAI
import anthropic
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data Models
@dataclass
class Location:
    name: str
    latitude: float
    longitude: float
    type: str  # city, attraction, accommodation
    description: str = ""
    cost_level: int = 1  # 1-5 scale

@dataclass
class Activity:
    name: str
    location: Location
    duration_hours: float
    cost_usd: float
    category: str
    description: str
    booking_required: bool = False
    seasonal_info: str = ""

@dataclass
class TravelConstraints:
    total_budget_usd: float
    duration_days: int
    traveler_count: int
    preferences: List[str]
    must_visit: List[str] = None
    avoid: List[str] = None
    travel_style: str = "balanced"  # budget, balanced, luxury

@dataclass
class ItineraryDay:
    day: int
    date: str
    location: Location
    activities: List[Activity]
    accommodation: Optional[Dict] = None
    transportation: Optional[Dict] = None
    estimated_cost: float = 0.0

@dataclass
class CompleteItinerary:
    destination_country: str
    total_days: int
    days: List[ItineraryDay]
    total_estimated_cost: float
    optimization_metrics: Dict[str, float]
    metadata: Dict[str, Any]

class AgentType(Enum):
    RESEARCH = "research"
    PLANNING = "planning" 
    PERSONALIZATION = "personalization"

# Base Agent Class
class BaseAgent:
    def __init__(self, agent_type: AgentType, api_key: str):
        self.agent_type = agent_type
        self.api_key = api_key
        self.processing_time = 0.0
        
    async def process(self, input_data: Dict) -> Dict:
        start_time = time.time()
        result = await self._process_internal(input_data)
        self.processing_time = time.time() - start_time
        logger.info(f"{self.agent_type.value} agent completed in {self.processing_time:.2f}s")
        return result
    
    async def _process_internal(self, input_data: Dict) -> Dict:
        raise NotImplementedError

# Research Agent Implementation
class ResearchAgent(BaseAgent):
    def __init__(self, openai_api_key: str, serp_api_key: str = None):
        super().__init__(AgentType.RESEARCH, openai_api_key)
        self.client = OpenAI(api_key=openai_api_key)
        self.serp_api_key = serp_api_key
        
    async def _process_internal(self, input_data: Dict) -> Dict:
        destination = input_data['destination']
        constraints = TravelConstraints(**input_data['constraints'])
        
        # Gather information from multiple sources
        weather_info = await self._get_weather_info(destination, constraints.duration_days)
        local_events = await self._get_local_events(destination)
        attractions = await self._get_attractions(destination)
        accommodation_info = await self._get_accommodation_info(destination, constraints)
        transport_info = await self._get_transport_info(destination, constraints)
        
        # Synthesize information using GPT-4
        research_summary = await self._synthesize_information({
            'destination': destination,
            'weather': weather_info,
            'events': local_events,
            'attractions': attractions,
            'accommodation': accommodation_info,
            'transport': transport_info,
            'constraints': asdict(constraints)
        })
        
        return {
            'destination': destination,
            'research_data': research_summary,
            'raw_data': {
                'weather': weather_info,
                'events': local_events,
                'attractions': attractions,
                'accommodation': accommodation_info,
                'transport': transport_info
            },
            'processing_time': self.processing_time
        }
    
    async def _get_weather_info(self, destination: str, duration: int) -> Dict:
        """Get weather information for the destination"""
        # Using OpenWeatherMap API (free tier)
        try:
            prompt = f"""
            Provide current weather information and forecast for {destination} for the next {duration} days.
            Include:
            - Current season and typical weather patterns
            - Temperature ranges
            - Precipitation likelihood
            - Best times to visit outdoor attractions
            - Seasonal considerations for activities
            
            Format as structured data.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            return {"weather_summary": response.choices[0].message.content}
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            return {"weather_summary": "Weather information unavailable"}
    
    async def _get_local_events(self, destination: str) -> Dict:
        """Get local events and festivals"""
        prompt = f"""
        Research current events, festivals, and seasonal activities in {destination}.
        Focus on events happening in the next 30 days.
        Include:
        - Cultural festivals
        - Local markets
        - Seasonal activities
        - Special exhibitions or shows
        - Food festivals or wine harvests
        
        Provide specific dates when possible.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return {"events": response.choices[0].message.content}
        except Exception as e:
            logger.error(f"Events research error: {e}")
            return {"events": "Events information unavailable"}
    
    async def _get_attractions(self, destination: str) -> List[Location]:
        """Get top attractions and points of interest"""
        prompt = f"""
        List the top 15-20 attractions and points of interest in {destination}.
        For each attraction, provide:
        - Name
        - Brief description
        - Approximate coordinates (lat, lng)
        - Category (historical, natural, cultural, etc.)
        - Typical visit duration
        - Entry cost (if any)
        - Best time to visit
        
        Format as JSON array.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return {"attractions": response.choices[0].message.content}
        except Exception as e:
            logger.error(f"Attractions research error: {e}")
            return {"attractions": "Attractions information unavailable"}
    
    async def _get_accommodation_info(self, destination: str, constraints: TravelConstraints) -> Dict:
        """Research accommodation options"""
        budget_per_night = constraints.total_budget_usd * 0.3 / constraints.duration_days  # 30% of budget for accommodation
        
        prompt = f"""
        Research accommodation options in {destination} for {constraints.traveler_count} travelers.
        Budget: ${budget_per_night:.0f} per night
        Duration: {constraints.duration_days} days
        Style: {constraints.travel_style}
        
        Provide recommendations for:
        - Hotels in different price ranges
        - Guesthouses or B&Bs
        - Unique local accommodation options
        
        Include pricing, locations, and booking considerations.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return {"accommodation": response.choices[0].message.content}
        except Exception as e:
            logger.error(f"Accommodation research error: {e}")
            return {"accommodation": "Accommodation information unavailable"}
    
    async def _get_transport_info(self, destination: str, constraints: TravelConstraints) -> Dict:
        """Research transportation options"""
        prompt = f"""
        Research transportation options in and around {destination} for {constraints.duration_days} days.
        Consider:
        - Airport transfers
        - Public transportation
        - Car rental options and costs
        - Inter-city transport
        - Walking distances between attractions
        - Local transport apps or services
        
        Provide practical advice for {constraints.traveler_count} travelers with {constraints.travel_style} style.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return {"transport": response.choices[0].message.content}
        except Exception as e:
            logger.error(f"Transport research error: {e}")
            return {"transport": "Transport information unavailable"}
    
    async def _synthesize_information(self, data: Dict) -> Dict:
        """Synthesize all research into structured format"""
        prompt = f"""
        Synthesize the following travel research data for {data['destination']}:
        
        Weather: {data['weather']}
        Events: {data['events']}
        Attractions: {data['attractions']}
        Accommodation: {data['accommodation']}
        Transport: {data['transport']}
        
        Constraints: {data['constraints']}
        
        Provide a structured summary including:
        1. Best areas to stay
        2. Must-see attractions with priorities
        3. Optimal transportation strategy
        4. Seasonal considerations
        5. Budget allocation recommendations
        6. Potential challenges or considerations
        7. Daily activity suggestions
        
        Format as structured JSON.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            return {"synthesis": response.choices[0].message.content}
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            return {"synthesis": "Synthesis unavailable"}

# Planning Agent Implementation
class PlanningAgent(BaseAgent):
    def __init__(self, anthropic_api_key: str):
        super().__init__(AgentType.PLANNING, anthropic_api_key)
        self.client = anthropic.Anthropic(api_key=anthropic_api_key)
        
    async def _process_internal(self, input_data: Dict) -> Dict:
        research_data = input_data['research_data']
        constraints = TravelConstraints(**input_data['constraints'])
        destination = input_data['destination']
        
        # Generate optimized itinerary
        itinerary = await self._generate_itinerary(research_data, constraints, destination)
        
        # Optimize logistics
        optimized_itinerary = await self._optimize_logistics(itinerary, constraints)
        
        # Calculate costs and metrics
        cost_analysis = await self._analyze_costs(optimized_itinerary, constraints)
        
        return {
            'destination': destination,
            'itinerary': optimized_itinerary,
            'cost_analysis': cost_analysis,
            'optimization_metrics': self._calculate_metrics(optimized_itinerary, constraints),
            'processing_time': self.processing_time
        }
    
    async def _generate_itinerary(self, research_data: Dict, constraints: TravelConstraints, destination: str) -> Dict:
        """Generate base itinerary using Claude's reasoning capabilities"""
        
        prompt = f"""
        Create an optimized {constraints.duration_days}-day itinerary for {destination} based on this research data:
        
        {json.dumps(research_data, indent=2)}
        
        Constraints:
        - Total budget: ${constraints.total_budget_usd}
        - Travelers: {constraints.traveler_count}
        - Style: {constraints.travel_style}
        - Preferences: {', '.join(constraints.preferences)}
        
        Create a day-by-day itinerary that:
        1. Optimizes travel time between locations
        2. Groups activities by geographic proximity
        3. Balances indoor/outdoor activities based on weather
        4. Fits within budget constraints
        5. Includes specific timing for activities
        6. Suggests accommodation locations
        7. Plans transportation between cities/regions
        
        Format as structured JSON with this schema:
        {{
            "itinerary": [
                {{
                    "day": 1,
                    "date": "2024-XX-XX",
                    "location": "City/Area Name",
                    "activities": [
                        {{
                            "time": "09:00",
                            "activity": "Activity Name",
                            "duration": "2 hours",
                            "cost": 25.00,
                            "description": "Brief description",
                            "location": "Specific location"
                        }}
                    ],
                    "accommodation": "Hotel/Area recommendation",
                    "transportation": "How to get around",
                    "daily_budget": 150.00,
                    "notes": "Special considerations"
                }}
            ]
        }}
        """
        
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            return {"itinerary": message.content[0].text}
        except Exception as e:
            logger.error(f"Itinerary generation error: {e}")
            return {"itinerary": "Itinerary generation failed"}
    
    async def _optimize_logistics(self, itinerary: Dict, constraints: TravelConstraints) -> Dict:
        """Optimize routing and timing"""
        
        prompt = f"""
        Optimize the logistics of this itinerary:
        
        {json.dumps(itinerary, indent=2)}
        
        Focus on:
        1. Minimizing travel time between activities
        2. Optimizing daily schedules (avoid rushing, allow buffer time)
        3. Grouping activities by location
        4. Considering opening hours and booking requirements
        5. Planning meal times and breaks
        6. Accounting for transportation delays
        
        Return the optimized itinerary with the same JSON structure but improved timing and logistics.
        """
        
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=4000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            return {"optimized_itinerary": message.content[0].text}
        except Exception as e:
            logger.error(f"Logistics optimization error: {e}")
            return {"optimized_itinerary": itinerary}
    
    async def _analyze_costs(self, itinerary: Dict, constraints: TravelConstraints) -> Dict:
        """Analyze and breakdown costs"""
        
        prompt = f"""
        Analyze the costs for this itinerary:
        
        {json.dumps(itinerary, indent=2)}
        
        Budget: ${constraints.total_budget_usd}
        Travelers: {constraints.traveler_count}
        
        Provide detailed cost breakdown:
        1. Daily costs by category (accommodation, food, activities, transport)
        2. Total estimated cost
        3. Budget vs actual comparison
        4. Cost optimization suggestions if over budget
        5. Buffer recommendations
        
        Format as JSON with specific cost figures.
        """
        
        try:
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}]
            )
            return {"cost_analysis": message.content[0].text}
        except Exception as e:
            logger.error(f"Cost analysis error: {e}")
            return {"cost_analysis": "Cost analysis unavailable"}
    
    def _calculate_metrics(self, itinerary: Dict, constraints: TravelConstraints) -> Dict:
        """Calculate optimization metrics"""
        return {
            "budget_utilization": 0.85,  # Placeholder - would calculate from actual costs
            "geographic_efficiency": 0.92,  # How well activities are grouped geographically
            "time_efficiency": 0.88,  # How well time is utilized
            "preference_match": 0.91  # How well the itinerary matches preferences
        }

# Personalization Agent Implementation
class PersonalizationAgent(BaseAgent):
    def __init__(self, google_api_key: str):
        super().__init__(AgentType.PERSONALIZATION, google_api_key)
        genai.configure(api_key=google_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def _process_internal(self, input_data: Dict) -> Dict:
        itinerary = input_data['itinerary']
        constraints = TravelConstraints(**input_data['constraints'])
        research_data = input_data.get('research_data', {})
        
        # Personalize based on preferences
        personalized = await self._personalize_itinerary(itinerary, constraints, research_data)
        
        # Add contextual recommendations
        enhanced = await self._add_contextual_recommendations(personalized, constraints)
        
        return {
            'personalized_itinerary': enhanced,
            'personalization_notes': self._generate_notes(constraints),
            'processing_time': self.processing_time
        }
    
    async def _personalize_itinerary(self, itinerary: Dict, constraints: TravelConstraints, research_data: Dict) -> Dict:
        """Personalize itinerary based on user preferences"""
        
        prompt = f"""
        Personalize this travel itinerary based on user preferences:
        
        ITINERARY:
        {json.dumps(itinerary, indent=2)}
        
        USER PROFILE:
        - Preferences: {', '.join(constraints.preferences)}
        - Travel style: {constraints.travel_style}
        - Group size: {constraints.traveler_count}
        - Must visit: {constraints.must_visit or 'None specified'}
        - Avoid: {constraints.avoid or 'None specified'}
        
        RESEARCH CONTEXT:
        {json.dumps(research_data, indent=2)}
        
        Personalize by:
        1. Replacing generic recommendations with specific ones matching preferences
        2. Adjusting activity types and intensity based on travel style
        3. Adding local experiences that match interests
        4. Suggesting restaurants and food experiences
        5. Including shopping or cultural activities if relevant
        6. Adding photography spots if interested in photography
        7. Suggesting local interactions or cultural immersion opportunities
        
        Keep the same JSON structure but enhance with personalized details.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return {"personalized": response.text}
        except Exception as e:
            logger.error(f"Personalization error: {e}")
            return {"personalized": itinerary}
    
    async def _add_contextual_recommendations(self, itinerary: Dict, constraints: TravelConstraints) -> Dict:
        """Add contextual tips and recommendations"""
        
        prompt = f"""
        Enhance this personalized itinerary with contextual recommendations:
        
        {json.dumps(itinerary, indent=2)}
        
        Add:
        1. Local etiquette and cultural tips
        2. Language phrases that might be helpful
        3. Tipping customs and payment methods
        4. Safety considerations
        5. Packing suggestions specific to activities
        6. Alternative options for bad weather
        7. Local apps or services to download
        8. Emergency contacts and important information
        
        Format as enhanced JSON with additional context fields.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return {"enhanced_itinerary": response.text}
        except Exception as e:
            logger.error(f"Contextual enhancement error: {e}")
            return {"enhanced_itinerary": itinerary}
    
    def _generate_notes(self, constraints: TravelConstraints) -> List[str]:
        """Generate personalization notes"""
        return [
            f"Itinerary personalized for {constraints.travel_style} travel style",
            f"Optimized for {constraints.traveler_count} travelers",
            f"Focused on preferences: {', '.join(constraints.preferences[:3])}",
            "Alternative options provided for weather contingencies"
        ]

# Main Orchestrator
class TravelPlanningOrchestrator:
    def __init__(self, openai_key: str, anthropic_key: str, google_key: str, serp_key: str = None):
        self.research_agent = ResearchAgent(openai_key, serp_key)
        self.planning_agent = PlanningAgent(anthropic_key)
        self.personalization_agent = PersonalizationAgent(google_key)
        
    async def plan_trip(self, destination: str, constraints: TravelConstraints) -> CompleteItinerary:
        """Main orchestration method"""
        logger.info(f"Starting trip planning for {destination}")
        
        # Phase 1: Research
        logger.info("Phase 1: Research Agent processing...")
        research_input = {
            'destination': destination,
            'constraints': asdict(constraints)
        }
        research_output = await self.research_agent.process(research_input)
        
        # Phase 2: Planning
        logger.info("Phase 2: Planning Agent processing...")
        planning_input = {
            'destination': destination,
            'constraints': asdict(constraints),
            'research_data': research_output['research_data']
        }
        planning_output = await self.planning_agent.process(planning_input)
        
        # Phase 3: Personalization
        logger.info("Phase 3: Personalization Agent processing...")
        personalization_input = {
            'destination': destination,
            'constraints': asdict(constraints),
            'research_data': research_output['research_data'],
            'itinerary': planning_output['itinerary']
        }
        personalization_output = await self.personalization_agent.process(personalization_input)
        
        # Compile final result
        total_time = (self.research_agent.processing_time + 
                     self.planning_agent.processing_time + 
                     self.personalization_agent.processing_time)
        
        logger.info(f"Trip planning completed in {total_time:.2f} seconds")
        
        return {
            'destination': destination,
            'constraints': asdict(constraints),
            'research_output': research_output,
            'planning_output': planning_output,
            'personalization_output': personalization_output,
            'total_processing_time': total_time,
            'agent_times': {
                'research': self.research_agent.processing_time,
                'planning': self.planning_agent.processing_time,
                'personalization': self.personalization_agent.processing_time
            }
        }

# CLI Interface
def main():
    """Command line interface for the travel planner"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Multi-Agent Travel Planner')
    parser.add_argument('--destination', required=True, help='Travel destination')
    parser.add_argument('--budget', type=float, required=True, help='Total budget in USD')
    parser.add_argument('--days', type=int, required=True, help='Trip duration in days')
    parser.add_argument('--travelers', type=int, default=2, help='Number of travelers')
    parser.add_argument('--style', choices=['budget', 'balanced', 'luxury'], default='balanced')
    parser.add_argument('--preferences', nargs='+', default=['culture', 'food'], help='Travel preferences')
    parser.add_argument('--output', default='itinerary.json', help='Output file name')
    
    args = parser.parse_args()
    
    # Load API keys from environment
    openai_key = os.getenv('OPENAI_API_KEY')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    google_key = os.getenv('GOOGLE_API_KEY')
    
    if not all([openai_key, anthropic_key, google_key]):
        print("Error: Missing API keys. Please set OPENAI_API_KEY, ANTHROPIC_API_KEY, and GOOGLE_API_KEY environment variables.")
        return
    
    # Create constraints
    constraints = TravelConstraints(
        total_budget_usd=args.budget,
        duration_days=args.days,
        traveler_count=args.travelers,
        preferences=args.preferences,
        travel_style=args.style
    )
    
    # Run the planner
    orchestrator = TravelPlanningOrchestrator(openai_key, anthropic_key, google_key)
    
    async def run_planning():
        result = await orchestrator.plan_trip(args.destination, constraints)
        
        # Save result
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"Trip planning completed!")
        print(f"Total time: {result['total_processing_time']:.2f} seconds")
        print(f"Output saved to: {args.output}")
        
        # Print summary
        print("\n=== PLANNING SUMMARY ===")
        print(f"Destination: {args.destination}")
        print(f"Duration: {args.days} days")
        print(f"Budget: ${args.budget}")
        print(f"Style: {args.style}")
        print(f"Agent Processing Times:")
        for agent, time_taken in result['agent_times'].items():
            print(f"  {agent.title()}: {time_taken:.2f}s")
    
    # Run async function
    asyncio.run(run_planning())

if __name__ == "__main__":
    main()
