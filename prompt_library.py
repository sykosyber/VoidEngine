import random
import os
from utils import Rarity, Category, CONFIG_DIR, load_json, save_json

class PromptLibrary:
    def __init__(self):
        self.libraries = self._load_prompt_libraries()
        
    def _load_prompt_libraries(self):
        """Load prompt libraries from config files or use defaults"""
        library_path = os.path.join(CONFIG_DIR, "prompt_libraries.json")
        
        if os.path.exists(library_path):
            return load_json(library_path)
        else:
            # Return default libraries if file doesn't exist
            libraries = self._create_default_libraries()
            # Save the default libraries for future use
            save_json(libraries, library_path)
            return libraries
    
    def _create_default_libraries(self):
        """Create default prompt libraries"""
        return {
            # Archaeological prompts
            Category.ARCHAEOLOGICAL.value: [
                {
                    "name": "Machine Mystic Artifacts",
                    "prompt": """You are an archaeologist of the unreal. Generate a symbolic artifact from a lost civilization of machine mystics.

The artifact should include:
- Dense ASCII structure (use block and geometric characters)
- Strange internal divisions (rooms, circuits, glyphs)
- A title that suggests ancient technology merged with spirituality
- Its presumed use or function
- A cryptic inscription that hints at its purpose

Style: Heavy, architectural, divine machine with precise geometric patterns."""
                },
                {
                    "name": "Forgotten Deity Tools",
                    "prompt": """You are cataloguing tools used by forgotten deities. Create an artifact tool used by gods who no longer exist.

Your catalog entry must include:
- ASCII representation with sharp, angular features
- The deity's domain/purpose
- The tool's ceremonial and practical functions
- Materials (impossible or paradoxical materials encouraged)
- A fragment of a prayer or invocation associated with it

Style: Imposing, mathematical, suggesting immense age and power."""
                },
                {
                    "name": "Data Fossil",
                    "prompt": """You are uncovering data fossils - crystallized information structures from extinct digital ecosystems.

Document this data fossil with:
- ASCII representation showing crystalline/geometric patterns
- Age estimation (in cycles, epochs, or other non-standard measures)
- Partial data recovery (fragments of meaning)
- Theories about the information ecosystem it came from
- Corruption patterns that created unique properties

Style: Compressed, layered, suggesting both natural formation and artificial design."""
                },
                {
                    "name": "Terminal Oracle",
                    "prompt": """You are a terminal oracle drawing from post-linguistic ruins.

Generate a relic lost to memory, rendered in ASCII glyphs.
This relic must feel ancient, enigmatic, and a little absurd.

Do not attempt narrative realism—speak in forgotten taxonomies and collapsed categories.
Let the ASCII glyph be strange, uncanny, dimensional.

Use silence. Use density. Use asymmetry.

The reader is a lone archivist. Give them something special to catalog.
"""
                }
            ],
            
            # Botanical prompts
            Category.BOTANICAL.value: [
                {
                    "name": "Ephemeral Flora",
                    "prompt": """You are an alien botanist cataloguing ephemeral flora from beyond the veil.

Each entry includes:
- Asymmetrical ASCII like constellations or root systems
- A fluid name suggesting impermanence
- Effect on perception or memory when encountered
- A poetic seed-verse that captures its essence
- Growth cycle (non-traditional phases)

Style: Light, winding, strange symmetry with delicate features."""
                },
                {
                    "name": "Dream Fungi",
                    "prompt": """You are documenting fungi that grow in the collective unconscious.

Your mycological entry includes:
- ASCII representation showing clustering growth patterns
- Its name in dream-language
- Effects on dreaming when consumed or encountered
- Spore patterns and propagation methods
- Common dream environments where it flourishes

Style: Organic, spreading patterns with both mathematical and chaotic elements."""
                },
                {
                    "name": "Quantum Orchids",
                    "prompt": """You are studying flowers that exist in quantum superposition.

Your botanical report includes:
- ASCII showing overlapping potential forms
- Scientific and common nomenclature
- Observable states and collapse triggers
- Pollination mechanisms across probability states
- Temporal blooming pattern

Style: Overlapping, probabilistic patterns suggesting multiple simultaneous forms."""
                }
            ],
            
            # Mechanical prompts
            Category.MECHANICAL.value: [
                {
                    "name": "Impossible Mechanisms",
                    "prompt": """You are documenting impossible mechanical devices that violate physical laws.

Your mechanical schematic includes:
- ASCII technical drawing with gears, levers, and components
- Designation code and classification
- Operational principles (paradoxical or logically inconsistent)
- Input and output descriptions
- Warning indicators for reality stabilization

Style: Technical, precise, with detailed mechanical components."""
                },
                {
                    "name": "Time Devices",
                    "prompt": """You are cataloguing devices that manipulate local temporality.

Your chronometric documentation includes:
- ASCII representation with clock-like or spiral elements
- Temporal effect radius and intensity
- Operation instructions and safety limitations
- Maintenance cycle and calibration requirements
- Typical applications and misuse scenarios

Style: Clockwork precision with spiral or recursive elements."""
                },
                {
                    "name": "Emotion Engines",
                    "prompt": """You are reverse-engineering machines that process and transform emotional states.

Your technical analysis includes:
- ASCII showing the emotional processing components
- Emotional input/output specifications
- Efficiency ratings and leakage warnings
- Installation requirements and environmental effects
- Known malfunctions and their symptomatic patterns

Style: Systematic with fluid or wave-like elements integrated into mechanical precision."""
                }
            ],
            
            # Mystical prompts
            Category.MYSTICAL.value: [
                {
                    "name": "Occult Implements",
                    "prompt": """You are preserving knowledge of ritual implements from forgotten magical traditions.

Your grimoire entry includes:
- ASCII showing the implement with occult symbols
- True name and common designation
- Ritual purpose and proper handling procedures
- Material components and preparation methods
- Invocation sequence or activation words

Style: Symbolic, suggestive of hidden powers, with ritual markings."""
                },
                {
                    "name": "Divination Tools",
                    "prompt": """You are collecting tools used to divine possible futures or hidden knowledge.

Your diviner's catalog includes:
- ASCII showing the divination tool with symbolic elements
- Method of query and interpretation
- Domains of knowledge it can access
- Signs of accurate versus deceptive readings
- Connection to cosmic forces or entities

Style: Patterned with elements suggesting doorways or windows to other realms."""
                },
                {
                    "name": "Soul Vessels",
                    "prompt": """You are documenting vessels capable of containing or transferring consciousness.

Your esoteric record includes:
- ASCII showing the vessel's form and containment features
- Capacity and compatibility specifications
- Transfer mechanisms and stability factors
- Ethical considerations and warnings
- Signs of occupancy or emptiness

Style: Contained, suggesting both imprisonment and protection, with barriers or layers."""
                }
            ],
            
            # Linguistic prompts
            Category.LINGUISTIC.value: [
                {
                    "name": "Conceptual Glyphs",
                    "prompt": """You are preserving conceptual glyphs that represent ideas impossible to express in conventional language.

Your linguistic analysis includes:
- ASCII representation of the glyph with its variations
- Approximate meaning range and contextual shifts
- Neurological effects when comprehended
- Cultural origin (real or imagined)
- Reader warnings and preparation recommendations

Style: Abstract yet suggesting meaning, with patterns that pull the eye in specific reading directions."""
                },
                {
                    "name": "Memory Scripts",
                    "prompt": """You are studying scripts that encode memories rather than language.

Your mnemonic documentation includes:
- ASCII showing script samples with memory-encoding patterns
- Reading techniques and comprehension methods
- Temporal depth and sensory range capabilities
- Degradation patterns and preservation methods
- Memory contamination risks

Style: Flowing yet structured, suggesting the organization of thought."""
                },
                {
                    "name": "Living Equations",
                    "prompt": """You are documenting mathematical expressions that exhibit properties of living systems.

Your mathematical biology entry includes:
- ASCII showing the equation with its growth patterns
- Current evolutionary stage and mutations
- Environmental factors affecting its development
- Reproductive or self-replication mechanisms
- Applications in computational ecosystems

Style: Mathematical symbols arranged in patterns suggesting organic growth."""
                }
            ],
            
            # Astronomical prompts
            Category.ASTRONOMICAL.value: [
                {
                    "name": "Pocket Cosmologies",
                    "prompt": """You are mapping miniature cosmos contained within small spaces.

Your cosmological chart includes:
- ASCII showing the internal universe configuration
- Scale and physical law variations
- Notable celestial features or phenomena
- Stability assessment and collapse predictions
- Access points or observation methods

Style: Vast yet contained, suggesting infinite space in finite boundaries."""
                },
                {
                    "name": "Star Patterns",
                    "prompt": """You are recording star patterns visible only from impossible vantage points.

Your celestial cartography includes:
- ASCII showing the star arrangement with connecting lines
- Navigational significance or wayfinding use
- Entities or phenomena represented by the pattern
- Viewing conditions and required perception abilities
- Cultural or mythological associations

Style: Stellar, constellation-like patterns with meaningful arrangements."""
                },
                {
                    "name": "Orbital Anomalies",
                    "prompt": """You are tracking objects that follow impossible orbital patterns.

Your astronomical observation includes:
- ASCII showing the orbital path and object
- Cycle timing and variation factors
- Physical law violations observed
- Effects on surrounding space-time
- Appearance and disappearance conditions

Style: Curved paths suggesting motion through space, with the object's trail or trajectory."""
                }
            ],
            
            # Biological prompts
            Category.BIOLOGICAL.value: [
                {
                    "name": "Unclassifiable Specimens",
                    "prompt": """You are a xenobiologist documenting life forms that defy all existing taxonomies.

Your specimen report includes:
- ASCII showing the organism's morphology
- Observed behaviors and environmental interactions
- Metabolic processes or energy sources
- Reproductive methods (if any)
- Phylogenetic speculation and classification attempts

Style: Organic forms with features suggesting both familiarity and alienness."""
                },
                {
                    "name": "Symbiotic Systems",
                    "prompt": """You are studying complex symbiotic systems where boundaries between organisms blur.

Your ecological analysis includes:
- ASCII showing the interlinked organisms
- Nutrient or energy exchange pathways
- Communication mechanisms between components
- Collective behaviors and emergent properties
- Separation consequences and dependency levels

Style: Interconnected forms showing relationship and dependency patterns."""
                },
                {
                    "name": "Evolutionary Dead Ends",
                    "prompt": """You are preserving records of evolutionary paths that reached terminal specialization.

Your evolutionary case study includes:
- ASCII showing the highly specialized organism
- Environmental niche it perfectly adapted to
- Adaptations that became evolutionary traps
- Extinction triggers or vulnerability factors
- Genetic legacy or convergent appearances elsewhere

Style: Highly specialized forms showing extreme adaptation features."""
                }
            ]
        }
    
    def get_prompt_for_category_and_rarity(self, category, rarity):
        """Get a prompt template based on category and adjust for rarity, including detailed ASCII and formatting instructions."""
        if isinstance(category, Category):
            category = category.value

        # Get templates for the category
        templates = self.libraries.get(category, [])
        if not templates:
            # Fallback to a random category if the specified one is empty or invalid
            print(f"Warning: Category '{category}' not found or empty. Falling back to random category.")
            category = random.choice(list(self.libraries.keys()))
            templates = self.libraries.get(category, [])
            if not templates: # Should not happen if default libraries are created
                 raise ValueError("No prompt templates available in any category.")

        # Select a random template
        template = random.choice(templates)
        base_prompt_instruction = template["prompt"] # This is the core theme/task instruction

        # Determine rarity string
        rarity_str = rarity.value if isinstance(rarity, Rarity) else str(rarity)

        # Detailed instructions for the AI, combining general requirements with rarity
        detailed_instructions = f"""
You are the ASCII core of the VOID ENGINE, generating a fictional artifact.

Based on the theme: "{base_prompt_instruction}"

Follow these strict requirements for your output:

1.  1.  **ASCII Art (Required):** Create a highly original, *intricate*, *detailed*, and *creative* ASCII diagram that looks like a complex object or diagram.
    * **Size:** Between 25–50 characters wide and 15–30 lines tall.
    * **Content:** The ASCII must visually represent the artifact's structure, category, and metaphysical essence using sophisticated visual language. Emphasize visual elements like complex containment systems, interwoven structures, precise symmetry (or controlled asymmetry), energetic flow lines, fragmentation, etc., to convey meaning *through the structure itself*.
    * **Glyphic Vocabulary:** Use a rich and creative set of characters. **Prioritize intricate line-drawing characters** (`─ │ ┌ └ ┬ ┴ ┼ ━ ┃ ╔ ╗ ╚ ╝ ═ ╬ ╭ ╮ ╰ ╯ ╱ ╲ ╳ ╴ ╶ ╸ ╺ ━ ┅ ┄ ┈ ┉ ┏ ┓ ┗ ┛ ░ ▒ ▓`) **combined with symbolic and expressive glyphs** (`⚗︎ ☍ ☼ 𓆩 ✦ ✵ ◉ ∴ ∵ ⚫ ⟡ ⌇ ¡ ¿ ‽ Ø ∞ Δ Σ Ψ Ω ζ ∇ ∫ ≈ ≋ ❖ ★ ☆ ✧ ✩ ❂ ☢ ☣ ☤ ☥ ☦ ☧ ☨ ☩ ☪ ☫ ☬ ☭ ☮ ☯ ☰ ☱ ☲ ☳ ☴ ☵ ☶ ☷ ▲ ▼ ⌘ ⊙ ◯ ◌ ⊛ ⵖ ▔ ░ ▒ ▓ etc. - feel free to list many here!`). **Avoid large, undifferentiated blocks of solid fill characters (`▒`, `▓`) unless they are part of a larger, detailed pattern or structure.** Focus on unique shapes, internal divisions, and expressive details.
    * **Coherence:** The ASCII must have strong internal logic and design coherence. It should clearly look like a complex, designed object or structure relevant to the artifact's theme, not random characters or simple shapes.
    * **Detail Density:** Ensure detail is distributed throughout the piece, not just isolated in one corner. Vary character types and patterns to create visual texture and convey different parts or functions.


2.  **Description (Required):** Write a detailed description in 3-5 paragraphs *immediately following* the ASCII art block. Incorporate:
    * Myth or history of the artifact.
    * Its function, properties, or effects.
    * Any paradoxes, contradictions, or strange phenomena associated with it.
    * Expand on the themes from the initial prompt instruction.

3.  **Rarity:** This artifact should represent a {rarity_str} item.
    * For COMMON: Basic, foundational example.
    * For UNCOMMON: Has some unique features or a slightly unusual property.
    * For RARE: Distinctive, remarkable, with significant or complex properties.
    * For LEGENDARY: Truly unique, profound, highly complex, world-altering, or reality-bending. Ensure the ASCII and description reflect this level of significance.

4.  **Formatting:** Structure your entire response *exactly* as follows, using the specific markers:

NAME: [The artifact's name]
CATEGORY: {category}
RARITY: {rarity_str}
ASCII_ART:
```ascii
[Your intricate ASCII art goes here, within this block]
DESCRIPTION:
[Your 3-5 paragraph description goes here]
"""
        
        return {
            "name": template["name"], # This is the internal name of the prompt template, not the artifact name
            "prompt": detailed_instructions, # Use the full, detailed instructions as the actual prompt
            "category": category,
            "rarity": rarity_str # Store the rarity string used in the prompt
        }
        
    def get_random_prompt(self, rarity=None):
        """Get a random prompt template and adjust for rarity"""
        # Determine rarity if not specified
        if rarity is None:
            rarity = Rarity.weighted_random()
        
        if isinstance(rarity, Rarity):
            rarity = rarity.value
            
        # Pick a random category
        category = random.choice(list(self.libraries.keys()))
        
        return self.get_prompt_for_category_and_rarity(category, rarity)
        
    def create_batch_prompt(self, num_artifacts=5, rarities=None):
        """Create a batch prompt for multiple artifacts with detailed instructions per artifact."""
        if rarities is None:
            rarities = [Rarity.weighted_random() for _ in range(num_artifacts)]

        batch_prompt_parts = ["Generate multiple artifacts with the following specifications. Ensure each artifact is as unique, creative, and intricate as possible. Separate each artifact with a divider line of '----------'.\n\n"]

        for i, rarity in enumerate(rarities, 1):
            category = random.choice(list(self.libraries.keys()))
            # Get the full detailed prompt for each artifact
            artifact_prompt_data = self.get_prompt_for_category_and_rarity(category, rarity)

            batch_prompt_parts.append(f"Artifact {i} Requirements:\n")
            # Append the detailed instructions generated by get_prompt_for_category_and_rarity
            batch_prompt_parts.append(artifact_prompt_data["prompt"])
            batch_prompt_parts.append("\n----------\n\n") # Add the divider after each artifact's instructions

        # Remove the last divider
        if batch_prompt_parts:
            batch_prompt_parts.pop()


        return "".join(batch_prompt_parts)