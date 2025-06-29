# test_travel_planner.py
import pytest
import asyncio
import json
from unittest.mock import Mock, patch
from travel_planner import (
    TravelPlanningOrchestrator, 
    TravelConstraints,
    ResearchAgent,
    PlanningAgent,
    PersonalizationAgent
)

class TestTravelPlanner:
    
    @pytest.fixture
    def sample_constraints(self):
        return TravelConstraints(
            total_budget_usd=1500,
            duration_days=7,
            traveler_count=2,
            preferences=["culture", "food"],
            travel_style="balanced"
        )
    
    @pytest.fixture
    def mock_orchestrator(self):
        return TravelPlanningOrchestrator(
            openai_key="test-key",
            anthropic_key="test-key",
            google_key="test-key"
        )
    
    def test_constraints_creation(self, sample_constraints):
        assert sample_constraints.total_budget_usd == 1500
        assert sample_constraints.duration_days == 7
        assert "culture" in sample_constraints.preferences
    
    @patch('openai.OpenAI')
    def test_research_agent_initialization(self, mock_openai):
        agent = ResearchAgent("test-key")
        assert agent.agent_type.value == "research"
        assert agent.api_key == "test-key"
    
    @patch('anthropic.Anthropic')
    def test_planning_agent_initialization(self, mock_anthropic):
        agent = PlanningAgent("test-key")
        assert agent.agent_type.value == "planning"
    
    @patch('google.generativeai.configure')
    def test_personalization_agent_initialization(self, mock_genai):
        agent = PersonalizationAgent("test-key")
        assert agent.agent_type.value == "personalization"
    
    @pytest.mark.asyncio
    async def test_orchestrator_flow(self, mock_orchestrator, sample_constraints):
        # Mock the agent responses
        with patch.object(mock_orchestrator.research_agent, 'process', return_value={'research_data': 'test'}), \
             patch.object(mock_orchestrator.planning_agent, 'process', return_value={'itinerary': 'test'}), \
             patch.object(mock_orchestrator.personalization_agent, 'process', return_value={'personalized_itinerary': 'test'}):
            
            result = await mock_orchestrator.plan_trip("Georgia", sample_constraints)
            
            assert result['destination'] == "Georgia"
            assert 'total_processing_time' in result
            assert 'agent_times' in result

if __name__ == "__main__":  
    pytest.main([__file__])

