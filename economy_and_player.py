import os
import json
import random
from utils import Rarity, Category, save_json, load_json, OUTPUT_DIR, SAVE_DIR

class ArtifactEconomy:
    """Manages market dynamics and artifact valuation"""
    
    def __init__(self):
        self.market_fluctuations = {}
        self.player_reputation = 1.0
        self.initialize_market()
        
    def initialize_market(self):
        """Set up initial market conditions"""
        # Initialize random market demand for each category
        for category in Category:
            self.market_fluctuations[category.value] = random.uniform(0.8, 1.2)
            
    def update_market(self):
        """Update market conditions - called periodically"""
        for category in self.market_fluctuations:
            # Current value affects how it changes (regression to mean)
            current = self.market_fluctuations[category]
            change = random.uniform(-0.15, 0.15)
            
            # Higher values tend to decrease, lower values tend to increase
            if current > 1.2:
                change -= 0.05
            elif current < 0.8:
                change += 0.05
                
            # Apply change with limits
            new_value = max(0.5, min(1.5, current + change))
            self.market_fluctuations[category] = new_value
            
    def calculate_value(self, artifact):
        """Calculate the current market value of an artifact"""
        rarity = artifact.get("rarity", "common")
        category = artifact.get("category", "unknown")
        
        # Use base value if it's already calculated
        base_value = artifact.get("value", 0)
        
        # If no base value, calculate from rarity
        if base_value == 0:
            for r in Rarity:
                if r.value == rarity:
                    min_val, max_val = Rarity.get_value_range(r)
                    base_value = random.randint(min_val, max_val)
                    break
            if base_value == 0:  # Fallback if rarity not found
                base_value = random.randint(5, 15)
        
        # Apply market fluctuation
        market_multiplier = self.market_fluctuations.get(category, 1.0)
        
        # Calculate current market value
        current_value = int(base_value * market_multiplier * self.player_reputation)
        
        return max(1, current_value)  # Ensure minimum value of 1
    
    def get_market_report(self):
        """Generate a market report showing current trends"""
        report = []
        report.append("=== MARKET CONDITIONS ===")
        report.append(f"Player Reputation Modifier: {self.player_reputation:.2f}x")
        report.append("\nCategory Demand:")
        
        # Sort categories by demand (high to low)
        sorted_categories = sorted(
            self.market_fluctuations.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        for category, multiplier in sorted_categories:
            # Determine market state
            if multiplier >= 1.3:
                state = "HOT MARKET"
            elif multiplier >= 1.1:
                state = "Rising"
            elif multiplier <= 0.7:
                state = "OVERSUPPLIED"
            elif multiplier <= 0.9:
                state = "Declining"
            else:
                state = "Stable"
                
            report.append(f"- {category.capitalize()}: {multiplier:.2f}x ({state})")
            
        return "\n".join(report)
    
    def update_player_reputation(self, player_stats):
        """Update player reputation based on their activities"""
        # More sold artifacts increases reputation
        artifacts_sold = player_stats.get("artifacts_sold", 0)
        
        # Legendary artifacts found increases reputation more significantly
        legendary_found = player_stats.get("legendary_found", 0)
        
        # Basic formula (can be adjusted)
        new_reputation = 1.0 + (artifacts_sold * 0.01) + (legendary_found * 0.05)
        
        # Cap at reasonable levels
        self.player_reputation = min(1.5, new_reputation)
        
        return self.player_reputation
    
    def save_market_state(self):
        """Save current market state to file"""
        market_state = {
            "fluctuations": self.market_fluctuations,
            "player_reputation": self.player_reputation
        }
        
        filepath = os.path.join(SAVE_DIR, "market_state.json")
        save_json(market_state, filepath)
        
    def load_market_state(self):
        """Load market state from file"""
        filepath = os.path.join(SAVE_DIR, "market_state.json")
        market_state = load_json(filepath)
        
        if market_state:
            self.market_fluctuations = market_state.get("fluctuations", self.market_fluctuations)
            self.player_reputation = market_state.get("player_reputation", self.player_reputation)
            return True
        
        return False


class Player:
    """Manages player stats, collection, and actions"""
    
    def __init__(self, starting_credits=50):
        self.credits = starting_credits
        self.collection = {}  # id -> artifact
        self.discovered_categories = set()
        self.discovered_rarities = set(["common"])
        self.stats = {
            "artifacts_generated": 0,
            "artifacts_sold": 0,
            "credits_earned": 0,
            "credits_spent": 0,
            "legendary_found": 0
        }
        
    def can_afford(self, cost):
        """Check if player can afford a cost"""
        return self.credits >= cost
        
    def spend_credits(self, amount):
        """Spend credits if player can afford it"""
        if not self.can_afford(amount):
            return False
        self.credits -= amount
        self.stats["credits_spent"] += amount
        return True
        
    def add_credits(self, amount):
        """Add credits to player's balance"""
        self.credits += amount
        self.stats["credits_earned"] += amount
        
    def add_to_collection(self, artifact):
        """Add an artifact to the player's collection"""
        artifact_id = artifact.get("id")
        if not artifact_id:
            from utils import generate_id
            artifact_id = generate_id()
            artifact["id"] = artifact_id
            
        self.collection[artifact_id] = artifact
        
        # Update discoveries
        self.discovered_categories.add(artifact.get("category"))
        self.discovered_rarities.add(artifact.get("rarity"))
        
        # Update stats
        self.stats["artifacts_generated"] += 1
        if artifact.get("rarity") == "legendary":
            self.stats["legendary_found"] += 1
            
        return artifact_id
            
    def remove_from_collection(self, artifact_id):
        """Remove an artifact from collection (for selling)"""
        if artifact_id in self.collection:
            artifact = self.collection.pop(artifact_id)
            return artifact
        return None
    
    def get_artifact(self, artifact_id):
        """Get an artifact from the collection by ID"""
        return self.collection.get(artifact_id)
    
    def get_collection_by_rarity(self):
        """Group collection by rarity"""
        by_rarity = {}
        for artifact_id, artifact in self.collection.items():
            rarity = artifact.get("rarity", "common")
            if rarity not in by_rarity:
                by_rarity[rarity] = []
            by_rarity[rarity].append(artifact_id)
        return by_rarity
    
    def get_collection_by_category(self):
        """Group collection by category"""
        by_category = {}
        for artifact_id, artifact in self.collection.items():
            category = artifact.get("category", "unknown")
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(artifact_id)
        return by_category
    
    def save_player_data(self):
        """Save player data to file"""
        player_data = {
            "credits": self.credits,
            "stats": self.stats,
            "discovered_categories": list(self.discovered_categories),
            "discovered_rarities": list(self.discovered_rarities)
        }
        
        # Save player data
        filepath = os.path.join(SAVE_DIR, "player_data.json")
        save_json(player_data, filepath)
        
        # Save collection separately (could be large)
        collection_path = os.path.join(SAVE_DIR, "collection.json")
        save_json(self.collection, collection_path)
        
    def load_player_data(self):
        """Load player data from file"""
        filepath = os.path.join(SAVE_DIR, "player_data.json")
        player_data = load_json(filepath)
        
        if player_data:
            self.credits = player_data.get("credits", self.credits)
            self.stats = player_data.get("stats", self.stats)
            self.discovered_categories = set(player_data.get("discovered_categories", []))
            self.discovered_rarities = set(player_data.get("discovered_rarities", []))
            
            # Load collection
            collection_path = os.path.join(SAVE_DIR, "collection.json")
            collection_data = load_json(collection_path)
            if collection_data:
                self.collection = collection_data
                
            return True
        
        return False
    
    def export_artifact(self, artifact_id):
        """Export a single artifact to a text file"""
        artifact = self.get_artifact(artifact_id)
        if not artifact:
            return False
            
        # Create output directory if it doesn't exist
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            
        # Generate filename based on artifact name
        name = artifact.get("name", "Unknown Artifact")
        safe_name = name.replace(" ", "_").replace("/", "_").lower()
        
        filepath = os.path.join(OUTPUT_DIR, f"{safe_name}_{artifact_id}.txt")
        
        # Format artifact data
        lines = []
        lines.append("=" * 60)
        lines.append(f"{name}")
        lines.append("=" * 60)
        
        # Add metadata
        lines.append(f"ID: {artifact_id}")
        lines.append(f"Category: {artifact.get('category', 'unknown').capitalize()}")
        lines.append(f"Rarity: {artifact.get('rarity', 'common').upper()}")
        lines.append(f"Value: {artifact.get('value', 0)} credits")
        lines.append("")
        
        # Add ASCII art
        if "ascii_art" in artifact:
            lines.append(artifact["ascii_art"])
        lines.append("")
        
        # Add description
        if "description" in artifact:
            lines.append(artifact["description"])
        
        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
            
        return filepath