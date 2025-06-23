import os
import time
import sys
import random
from utils import Rarity, Category, print_box, print_centered, print_artifact_preview
from prompt_library import PromptLibrary
from api_client import APIClient, DeepVoid
from economy_and_player import ArtifactEconomy, Player

class ArtifactTradingGame:
    """Main game class for the Void Artifact Trader"""
    
    def __init__(self, api_key=None, provider="openai"):
        # Initialize API client
        self.api_client = APIClient(api_key, provider)
        
        # Initialize core systems
        self.deep_void = DeepVoid(self.api_client)
        self.economy = ArtifactEconomy()
        self.player = Player(starting_credits=50)
        
        # Game state
        self.turn = 0
        self.market_update_frequency = 5  # turns
        self.running = True
        
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def start_game(self):
        """Initialize and start the game"""
        self.clear_screen()
        
        # Check for saved game
        if self.try_load_game():
            choice = input("Would you like to continue your saved game? (y/n): ").strip().lower()
            if choice != 'y':
                # Reset to new game
                self.economy = ArtifactEconomy()
                self.player = Player(starting_credits=50)
                self.turn = 0
        
        # Display title screen
        self.display_title_screen()
        
        # Initialize economy if new game
        if self.turn == 0:
            self.economy.initialize_market()
        
        # Start main game loop
        self.game_loop()
        
    def try_load_game(self):
        """Attempt to load a saved game"""
        player_loaded = self.player.load_player_data()
        market_loaded = self.economy.load_market_state()
        
        return player_loaded and market_loaded
        
    def save_game(self):
        """Save the current game state"""
        self.player.save_player_data()
        self.economy.save_market_state()
        print("\nGame saved successfully!")
        
    def display_title_screen(self):
        """Display the game title screen"""
        print_box("""
THE VOID ARTIFACT TRADER

Collect • Trade • Discover

The Deep Void produces virtual artifacts of strange origin.
Will you become a master collector?
""", width=70)
        
        #print(f"\nWelcome to the Deep Void. You are a collector of strange artifacts.")
        print(f"You have {self.player.credits} credits to start.\n")
        
        input("Press Enter to begin your journey...")
        
    def game_loop(self):
        """Main game loop"""
        self.running = True
        
        while self.running:
            # Update market periodically
            if self.turn % self.market_update_frequency == 0 and self.turn > 0:
                self.economy.update_market()
                print("\n>>> Market conditions have shifted. <<<\n")
                time.sleep(1)
            
            # Update player reputation based on stats
            self.economy.update_player_reputation(self.player.stats)
            
            # Display current status
            self.display_status()
            
            # Get player action
            action = self.get_player_action()
            
            # Process action
            self.process_action(action)
            
            # Increment turn if still running
            if self.running:
                self.turn += 1
                
        # End game summary
        self.display_end_game_summary()
            
    def get_player_action(self):
        """Get the player's next action"""
        print("\nWhat would you like to do?")
        print("1. Generate artifacts from the Deep Void")
        print("2. View your collection")
        print("3. Check market conditions")
        print("4. Sell artifacts")
        print("5. Save and exit")
        
        return input("> ").strip()
    
    def process_action(self, action):
        """Process the player's chosen action"""
        if action == "1":
            self.generate_artifacts()
        elif action == "2":
            self.view_collection()
        elif action == "3":
            self.view_market()
        elif action == "4":
            self.sell_artifacts()
        elif action == "5":
            self.save_game()
            self.running = False
        else:
            print("Invalid choice. Please try again.")
    
    def display_status(self):
        """Display the current game status"""
        self.clear_screen()
        
        print_centered("=== THE VOID ARTIFACT TRADER ===")
        print(f"Turn: {self.turn} | Credits: {self.player.credits} | Artifacts: {len(self.player.collection)}")
        print(f"Reputation: {self.economy.player_reputation:.2f}x")
        print("-" * 70)
        
    def generate_artifacts(self):
        """Generate new artifacts"""
        self.clear_screen()
        print_centered("=== ARTIFACT GENERATION ===")
        print("The Deep Void can produce artifacts of different rarities.")
        print("Each rarity has a different cost:")
        
        # Show costs for each rarity
        for rarity in Rarity:
            cost = Rarity.get_cost(rarity)
            print(f"- {rarity.value.capitalize()}: {cost} credits")
        
        print(f"\nYou have {self.player.credits} credits.")
        
        # Let player choose batch size
        print("\nHow many artifacts would you like to generate? (1-10)")
        
        try:
            count = int(input("> ").strip())
            count = max(1, min(10, count))
        except ValueError:
            print("Invalid input. Generating 1 artifact.")
            count = 1
        
        # Let player choose specific rarities or random
        choice = input("\nDo you want to specify rarities? (y/n): ").strip().lower()
        
        rarities = []
        total_cost = 0
        
        if choice == 'y':
            # Player chooses rarities
            print("\nChoose rarities (enter the number):")
            available_rarities = list(Rarity)
            
            for i, rarity in enumerate(available_rarities, 1):
                cost = Rarity.get_cost(rarity)
                print(f"{i}. {rarity.value.capitalize()} ({cost} credits)")
            
            for i in range(count):
                try:
                    rarity_choice = int(input(f"Artifact {i+1} rarity (1-{len(available_rarities)}): "))
                    if 1 <= rarity_choice <= len(available_rarities):
                        chosen_rarity = available_rarities[rarity_choice-1]
                        rarities.append(chosen_rarity)
                        total_cost += Rarity.get_cost(chosen_rarity)
                    else:
                        print(f"Invalid choice. Using {Rarity.COMMON.value}.")
                        rarities.append(Rarity.COMMON)
                        total_cost += Rarity.get_cost(Rarity.COMMON)
                except ValueError:
                    print(f"Invalid input. Using {Rarity.COMMON.value}.")
                    rarities.append(Rarity.COMMON)
                    total_cost += Rarity.get_cost(Rarity.COMMON)
        else:
            # Random rarities based on weighted distribution
            for _ in range(count):
                rarity = Rarity.weighted_random()
                rarities.append(rarity)
                total_cost += Rarity.get_cost(rarity)
                
        # Check if player can afford it
        if not self.player.can_afford(total_cost):
            print(f"\nYou don't have enough credits! That would cost {total_cost} credits.")
            input("\nPress Enter to return to the main menu...")
            return
            
        # Confirm generation
        print(f"\nThis will cost {total_cost} credits. Proceed? (y/n)")
        if input("> ").strip().lower() != 'y':
            print("Generation cancelled.")
            input("\nPress Enter to return to the main menu...")
            return
            
        # Spend credits
        self.player.spend_credits(total_cost)
        
        # Generate artifacts
        print("\nGenerating artifacts from the Deep Void...")
        print("This may take a moment as the Void forms your artifacts...")
        
        try:
            # Generate artifacts in batch for API efficiency
            artifacts = self.deep_void.generate_batch(len(rarities), rarities)
            
            # Add artifacts to collection
            print("\n=== ARTIFACTS DISCOVERED ===")
            for artifact in artifacts:
                artifact_id = self.player.add_to_collection(artifact)
                print_artifact_preview(artifact)
                print("")
                
                # Export artifact to file
                filepath = self.player.export_artifact(artifact_id)
                print(f"Saved to: {filepath}")
                print("-" * 40)
                
            print(f"\nYou now have {self.player.credits} credits remaining.")
            
        except Exception as e:
            print(f"\nError generating artifacts: {str(e)}")
            print("Your credits have been refunded.")
            self.player.add_credits(total_cost)
            
        input("\nPress Enter to continue...")
    
    def view_collection(self):
        """View and interact with the player's collection"""
        self.clear_screen()
        print_centered("=== YOUR COLLECTION ===")
        
        if not self.player.collection:
            print("\nYour collection is empty. Generate some artifacts first!")
            input("\nPress Enter to return to the main menu...")
            return
            
        print(f"Total artifacts: {len(self.player.collection)}")
        
        # Show different viewing options
        print("\nHow would you like to view your collection?")
        print("1. By rarity")
        print("2. By category")
        print("3. View a specific artifact")
        print("4. Return to main menu")
        
        choice = input("> ").strip()
        
        if choice == "1":
            self.view_by_rarity()
        elif choice == "2":
            self.view_by_category()
        elif choice == "3":
            self.view_specific_artifact()
        else:
            return
    
    def view_by_rarity(self):
        """View collection organized by rarity"""
        self.clear_screen()
        print_centered("=== COLLECTION BY RARITY ===")
        
        # Group by rarity
        by_rarity = self.player.get_collection_by_rarity()
        
        # Order rarities by value (highest first)
        rarity_order = [r.value for r in sorted(Rarity, key=lambda r: Rarity.get_cost(r), reverse=True)]
        
        # Display
        artifact_ids = []
        
        for rarity in rarity_order:
            if rarity in by_rarity and by_rarity[rarity]:
                print(f"\n--- {rarity.upper()} ({len(by_rarity[rarity])}) ---")
                
                for artifact_id in by_rarity[rarity]:
                    artifact = self.player.get_artifact(artifact_id)
                    if artifact:
                        # Update market value
                        current_value = self.economy.calculate_value(artifact)
                        
                        # Display basic info
                        print(f"{len(artifact_ids)+1}. {artifact.get('name')} (ID: {artifact_id[:4]}...) - {current_value} credits")
                        artifact_ids.append(artifact_id)
        
        # Offer to view specific artifact
        if artifact_ids:
            print("\nEnter a number to view details, or 0 to return:")
            try:
                idx = int(input("> ").strip())
                if 1 <= idx <= len(artifact_ids):
                    self.display_artifact(artifact_ids[idx-1])
            except ValueError:
                pass
    
    def view_by_category(self):
        """View collection organized by category"""
        self.clear_screen()
        print_centered("=== COLLECTION BY CATEGORY ===")
        
        # Group by category
        by_category = self.player.get_collection_by_category()
        
        # Display
        artifact_ids = []
        
        for category in sorted(by_category.keys()):
            if by_category[category]:
                print(f"\n--- {category.upper()} ({len(by_category[category])}) ---")
                
                for artifact_id in by_category[category]:
                    artifact = self.player.get_artifact(artifact_id)
                    if artifact:
                        # Update market value
                        current_value = self.economy.calculate_value(artifact)
                        rarity = artifact.get('rarity', 'common').upper()
                        
                        # Display basic info
                        print(f"{len(artifact_ids)+1}. [{rarity}] {artifact.get('name')} (ID: {artifact_id[:4]}...) - {current_value} credits")
                        artifact_ids.append(artifact_id)
        
        # Offer to view specific artifact
        if artifact_ids:
            print("\nEnter a number to view details, or 0 to return:")
            try:
                idx = int(input("> ").strip())
                if 1 <= idx <= len(artifact_ids):
                    self.display_artifact(artifact_ids[idx-1])
            except ValueError:
                pass
    
    def view_specific_artifact(self):
        """View a specific artifact by ID"""
        self.clear_screen()
        print_centered("=== VIEW SPECIFIC ARTIFACT ===")
        
        if not self.player.collection:
            print("Your collection is empty.")
            input("\nPress Enter to return...")
            return
            
        # List all artifacts with ID prefixes
        artifact_ids = list(self.player.collection.keys())
        
        if not artifact_ids:
            print("No artifacts found.")
            input("\nPress Enter to return...")
            return
            
        for i, artifact_id in enumerate(artifact_ids, 1):
            artifact = self.player.get_artifact(artifact_id)
            if artifact:
                name = artifact.get('name', 'Unknown')
                rarity = artifact.get('rarity', 'common').upper()
                print(f"{i}. [{rarity}] {name} (ID: {artifact_id[:4]}...)")
                
        print("\nEnter the number of the artifact to view:")
        try:
            idx = int(input("> ").strip())
            if 1 <= idx <= len(artifact_ids):
                self.display_artifact(artifact_ids[idx-1])
        except ValueError:
            print("Invalid input.")
    
    def display_artifact(self, artifact_id):
        """Display full details of a specific artifact"""
        artifact = self.player.get_artifact(artifact_id)
        
        if not artifact:
            print("Artifact not found.")
            input("\nPress Enter to return...")
            return
            
        self.clear_screen()
        
        # Get current market value
        current_value = self.economy.calculate_value(artifact)
        
        # Display header
        name = artifact.get('name', 'Unknown Artifact')
        rarity = artifact.get('rarity', 'common').upper()
        category = artifact.get('category', 'unknown').capitalize()
        
        print_centered(f"=== {name} ===")
        print(f"ID: {artifact_id}")
        print(f"Rarity: {rarity} | Category: {category}")
        print(f"Base Value: {artifact.get('value', 0)} credits | Current Market Value: {current_value} credits")
        print("-" * 70)
        
        # Display ASCII art
        if "ascii_art" in artifact:
            print(artifact["ascii_art"])
            print("")
            
        # Display description
        if "description" in artifact:
            print(artifact["description"])
            
        print("\nOptions:")
        print("1. Export to file")
        print("2. Return to collection")
        
        choice = input("> ").strip()
        
        if choice == "1":
            filepath = self.player.export_artifact(artifact_id)
            print(f"Exported to: {filepath}")
            input("\nPress Enter to continue...")
    
    def view_market(self):
        """View current market conditions"""
        self.clear_screen()
        print_centered("=== MARKET CONDITIONS ===")
        
        # Display market report
        print(self.economy.get_market_report())
        
        # Show market tips
        print("\nMarket Tips:")
        print("- Market conditions shift every few turns")
        print("- Sell artifacts when their category is in high demand")
        print("- Your reputation affects selling prices")
        print("- Finding legendary artifacts improves your reputation")
        
        input("\nPress Enter to return to the main menu...")
    
    def sell_artifacts(self):
        """Sell artifacts from collection"""
        self.clear_screen()
        print_centered("=== SELL ARTIFACTS ===")
        
        if not self.player.collection:
            print("Your collection is empty. Nothing to sell!")
            input("\nPress Enter to return to the main menu...")
            return
            
        print("Select artifacts to sell:\n")
        
        # List artifacts with current market values
        artifact_ids = list(self.player.collection.keys())
        for i, artifact_id in enumerate(artifact_ids, 1):
            artifact = self.player.get_artifact(artifact_id)
            
            if artifact:
                name = artifact.get('name', 'Unknown')
                rarity = artifact.get('rarity', 'common').upper()
                category = artifact.get('category', 'unknown')
                
                # Calculate current market value
                current_value = self.economy.calculate_value(artifact)
                
                # Get market multiplier for category
                market_multiplier = self.economy.market_fluctuations.get(category, 1.0)
                market_status = ""
                
                if market_multiplier >= 1.2:
                    market_status = "(HOT MARKET!)"
                elif market_multiplier <= 0.8:
                    market_status = "(Low Demand)"
                    
                print(f"{i}. [{rarity}] {name} - {current_value} credits {market_status}")
                
        print("\nEnter the numbers of artifacts to sell (comma-separated), or 'all' to sell everything:")
        sell_input = input("> ").strip().lower()
        
        to_sell = []
        
        if sell_input == 'all':
            to_sell = artifact_ids
        else:
            try:
                indices = [int(idx.strip()) for idx in sell_input.split(',') if idx.strip()]
                for idx in indices:
                    if 1 <= idx <= len(artifact_ids):
                        to_sell.append(artifact_ids[idx-1])
            except ValueError:
                print("Invalid input. No artifacts selected.")
                input("\nPress Enter to return...")
                return
                
        if not to_sell:
            print("No artifacts selected for sale.")
            input("\nPress Enter to return...")
            return
            
        # Calculate total value
        total_value = 0
        artifacts_to_sell = []
        
        print("\n=== SELLING SUMMARY ===")
        
        for artifact_id in to_sell:
            artifact = self.player.get_artifact(artifact_id)
            if artifact:
                current_value = self.economy.calculate_value(artifact)
                total_value += current_value
                
                print(f"- {artifact.get('name')} sold for {current_value} credits")
                artifacts_to_sell.append((artifact_id, artifact))
                
        print(f"\nTotal sale value: {total_value} credits")
        
        # Confirm sale
        print("\nProceed with sale? (y/n)")
        if input("> ").strip().lower() != 'y':
            print("Sale cancelled.")
            input("\nPress Enter to return...")
            return
            
        # Process sale
        for artifact_id, artifact in artifacts_to_sell:
            self.player.remove_from_collection(artifact_id)
            
        # Add credits to player
        self.player.add_credits(total_value)
        
        # Update stats
        self.player.stats["artifacts_sold"] += len(artifacts_to_sell)
        
        print(f"\nSale complete! You now have {self.player.credits} credits.")
        input("\nPress Enter to return to the main menu...")
    
    def display_end_game_summary(self):
        """Display a summary when the game ends"""
        self.clear_screen()
        print_box("GAME SUMMARY", width=70)
        
        print(f"Total turns played: {self.turn}")
        print(f"Final credits: {self.player.credits}")
        print(f"Collection size: {len(self.player.collection)} artifacts")
        print(f"Final reputation: {self.economy.player_reputation:.2f}x")
        print("\nStats:")
        print(f"- Artifacts generated: {self.player.stats['artifacts_generated']}")
        print(f"- Artifacts sold: {self.player.stats['artifacts_sold']}")
        print(f"- Credits earned: {self.player.stats['credits_earned']}")
        print(f"- Credits spent: {self.player.stats['credits_spent']}")
        print(f"- Legendary artifacts found: {self.player.stats['legendary_found']}")
        
        # Calculate collection value
        total_collection_value = 0
        for artifact_id, artifact in self.player.collection.items():
            total_collection_value += self.economy.calculate_value(artifact)
            
        print(f"\nTotal collection value: {total_collection_value} credits")
        print(f"Total wealth (credits + collection): {self.player.credits + total_collection_value} credits")
        
        print("\nThank you for playing The Void Artifact Trader!")
        input("\nPress Enter to exit...")
