"""
Quick start example for the travel planning system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from travel_planner import TravelPlanner

def main():
    planner = TravelPlanner()
    
    # Example trip to Georgia
    trip = planner.plan_trip(
        destination="Georgia",
        budget=1500,
        days=7,
        travelers=2,
        preferences=["culture", "food", "hiking", "wine"]
    )
    
    print("🎉 Trip planned successfully!")
    print(f"📍 Destination: {trip.destination}")
    print(f"💰 Total Cost: ${trip.total_cost}")
    print(f"📅 Duration: {trip.days} days")

if __name__ == "__main__":
    main()