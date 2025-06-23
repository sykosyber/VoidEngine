import os
import json
import time
import random
import uuid
from enum import Enum

# Define constants
CONFIG_DIR = "config"
OUTPUT_DIR = "artifacts"
SAVE_DIR = "saves"

# Ensure directories exist
for directory in [CONFIG_DIR, OUTPUT_DIR, SAVE_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

class Rarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    LEGENDARY = "legendary"
    
    @staticmethod
    def get_weight(rarity):
        weights = {
            Rarity.COMMON: 0.70,
            Rarity.UNCOMMON: 0.20,
            Rarity.RARE: 0.08,
            Rarity.LEGENDARY: 0.02
        }
        return weights.get(rarity, 0)
    
    @staticmethod
    def get_cost(rarity):
        costs = {
            Rarity.COMMON: 1,
            Rarity.UNCOMMON: 3,
            Rarity.RARE: 7,
            Rarity.LEGENDARY: 15
        }
        return costs.get(rarity, 0)
    
    @staticmethod
    def get_value_range(rarity):
        value_ranges = {
            Rarity.COMMON: (5, 15),
            Rarity.UNCOMMON: (20, 50),
            Rarity.RARE: (60, 200),
            Rarity.LEGENDARY: (250, 1000)
        }
        return value_ranges.get(rarity, (1, 5))
        
    @staticmethod
    def weighted_random():
        """Return a random rarity based on weighted probabilities"""
        rarities = list(Rarity)
        weights = [Rarity.get_weight(r) for r in rarities]
        return random.choices(rarities, weights=weights, k=1)[0]
        
    @staticmethod
    def get_all():
        return list(Rarity)

class Category(Enum):
    ARCHAEOLOGICAL = "archaeological"
    BOTANICAL = "botanical"
    MECHANICAL = "mechanical"
    MYSTICAL = "mystical"
    LINGUISTIC = "linguistic"
    ASTRONOMICAL = "astronomical"
    BIOLOGICAL = "biological"
    
    @staticmethod
    def get_random():
        return random.choice(list(Category))
    
    @staticmethod
    def get_all():
        return list(Category)

def generate_id():
    """Generate a unique ID for an artifact"""
    return str(uuid.uuid4())[:8]

def save_json(data, filepath):
    """Save data to JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def load_json(filepath):
    """Load data from JSON file"""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def print_centered(text, width=70):
    """Print text centered in the terminal"""
    print(text.center(width))

def print_box(text, width=70):
    """Print text in a box"""
    print("╔" + "═" * (width - 2) + "╗")
    for line in text.split('\n'):
        print("║" + line.center(width - 2) + "║")
    print("╚" + "═" * (width - 2) + "╝")

def print_artifact_preview(artifact):
    """Print a preview of an artifact"""
    rarity = artifact.get("rarity", "common").upper()
    name = artifact.get("name", "Unknown Artifact")
    category = artifact.get("category", "unknown").capitalize()
    value = artifact.get("value", 0)
    
    print(f"[{rarity}] {name}")
    print(f"Category: {category} | Value: {value} credits")
    
    # Print a small preview of the ASCII art if available
    if "ascii_art" in artifact:
        art_lines = artifact["ascii_art"].split('\n')
        if len(art_lines) > 3:
            preview = '\n'.join(art_lines[:3]) + "\n..."
        else:
            preview = artifact["ascii_art"]
        print(preview)
