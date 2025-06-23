#!/usr/bin/env python3
import os
import sys
import argparse

def main():
    """Main entry point for the Void Artifact Trader"""
    parser = argparse.ArgumentParser(description="The Void Artifact Trader - Collect, Trade, Discover")
    
    # API configuration
    parser.add_argument("--api-key", help="API key for OpenAI or Anthropic")
    parser.add_argument("--provider", choices=["openai", "anthropic"], default="openai", help="AI provider (default: openai)")
    
    # Other options
    parser.add_argument("--debug", action="store_true", help="Enable debug mode with extra logging")
    
    args = parser.parse_args()
    
    # Check for API key in arguments, then environment variables
    api_key = args.api_key
    if not api_key:
        if args.provider == "openai" and "OPENAI_API_KEY" in os.environ:
            api_key = os.environ["OPENAI_API_KEY"]
        elif args.provider == "anthropic" and "ANTHROPIC_API_KEY" in os.environ:
            api_key = os.environ["ANTHROPIC_API_KEY"]
    
    # Print welcome message
    print("""=== THE VOID ARTIFACT TRADER ===
          
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                    ┃
┃                                                                    ┃
┃    ╔════════════════════════════════════════════════════════╗     ┃
┃    ║                                                        ║     ┃
┃    ║     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ║     ┃
┃    ║     ▓                                            ▓     ║     ┃
┃    ║     ▓   ╭────────────────────────────────────╮   ▓     ║     ┃
┃    ║     ▓   │ ╔═══════════════════════════════╗ │   ▓     ║     ┃
┃    ║     ▓   │ ║                               ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┏━━━━━━━━━━━━━━━━━━━┓     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃  ╱╲      ╱╲  ╱╲   ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃ ╱  ╲    ╱╲╱  ╲    ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃╱    ╲  ╱    ╲     ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃      ╳      ╲     ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃     ╱ ╲      ╲    ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃    ╱   ╲      ╲   ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃   ╱     ╲      ╲  ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃  ╱       ╲      ╲ ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┗━━━━━━━━━━━━━━━━━━━┛     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║        ◆  ◆  ◆  ◆  ◆         ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║                               ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┏━━━━━━━━━━━━━━━━━━━┓     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃ ⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿ ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃ ⦿               ⦿ ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃ ⦿  ┌─────────┐  ⦿ ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃ ⦿  │╭───────╮│  ⦿ ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃ ⦿  ││       ││  ⦿ ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃ ⦿  ││   ⦿   ││  ⦿ ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃ ⦿  ││       ││  ⦿ ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃ ⦿  │╰───────╯│  ⦿ ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃ ⦿  └─────────┘  ⦿ ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃ ⦿               ⦿ ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┃ ⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿⦿ ┃     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ║    ┗━━━━━━━━━━━━━━━━━━━┛     ║ │   ▓     ║     ┃
┃    ║     ▓   │ ╚═══════════════════════════════╝ │   ▓     ║     ┃
┃    ║     ▓   ╰────────────────────────────────────╯   ▓     ║     ┃
┃    ║     ▓                                            ▓     ║     ┃
┃    ║     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ║     ┃
┃    ║                                                        ║     ┃
┃    ╚════════════════════════════════════════════════════════╝     ┃
┃                                                                    ┃
┃                           VOID ENGINE                              ┃
┃                                                                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
          
          
          """)
    print("Initializing game components...")
    
    try:
        # Import game module (only import when needed to handle potential errors gracefully)
        from game import ArtifactTradingGame
        
        # Initialize and start the game
        game = ArtifactTradingGame(api_key=api_key, provider=args.provider)
        game.start_game()
        
    except ImportError as e:
        print(f"Error importing game components: {str(e)}")
        print("Please ensure you have installed the required dependencies:")
        print("  pip install openai anthropic")
        
    except Exception as e:
        print(f"Error starting game: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        
if __name__ == "__main__":
    main()
