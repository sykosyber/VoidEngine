import os
import openai
import anthropic
from utils import Rarity, Category, generate_id
import random
import re

class APIClient:
    """Wrapper for AI API clients (OpenAI or Anthropic)"""
    
    def __init__(self, api_key=None, provider="openai"):
        self.api_key = api_key
        self.provider = provider.lower()
        self.setup_client()
        
    def setup_client(self):
        """Set up the appropriate API client"""
        if self.provider == "openai":
            if self.api_key:
                openai.api_key = self.api_key
            elif "OPENAI_API_KEY" in os.environ:
                openai.api_key = os.environ["OPENAI_API_KEY"]
            else:
                raise ValueError("OpenAI API key not provided")
                
        elif self.provider == "anthropic":
            if self.api_key:
                self.anthropic_client = anthropic.Anthropic(api_key=self.api_key)
            elif "ANTHROPIC_API_KEY" in os.environ:
                self.anthropic_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
            else:
                raise ValueError("Anthropic API key not provided")
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
            
    def generate(self, prompt, max_tokens=2000, temperature=0.7):
        """Generate content using the appropriate API"""
        try:
            if self.provider == "openai":
                return self._generate_openai(prompt, max_tokens, temperature)
            elif self.provider == "anthropic":
                return self._generate_anthropic(prompt, max_tokens, temperature)
        except Exception as e:
            print(f"API Error: {str(e)}")
            raise
    
    def _generate_openai(self, prompt, max_tokens=2000, temperature=0.7):
        """Generate content using OpenAI API"""
        try:
            # Try using newer OpenAI client
            if hasattr(openai, 'chat'):
                # Newer version of the OpenAI library
                response = openai.chat.completions.create(
                    model="gpt-4",  # You can also use "gpt-3.5-turbo" for a less expensive option
                    messages=[
                        {"role": "system", "content": "You are a creative system that generates unique artifacts with ASCII art and detailed descriptions"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content
            else:
                # Older version of the OpenAI library
                response = openai.ChatCompletion.create(
                    model="gpt-4",  # You can also use "gpt-3.5-turbo" for a less expensive option
                    messages=[
                        {"role": "system", "content": "You are a creative system that generates unique artifacts with ASCII art and detailed descriptions"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message['content']
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            raise
    
    def _generate_anthropic(self, prompt, max_tokens=2000, temperature=0.7):
        """Generate content using Anthropic API"""
        try:
            system_prompt = "You are a creative system that generates unique artifacts with ASCII art and detailed descriptions."
            
            # Call the API using Messages API (newer versions)
            try:
                response = self.anthropic_client.messages.create(
                    model="claude-3-opus-20240229",
                    system=system_prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text
            except (AttributeError, TypeError) as e:
                # For older versions of the Anthropic client, try completions API
                print("Falling back to older Anthropic API format")
                response = self.anthropic_client.completions.create(
                    model="claude-3-opus-20240229",
                    prompt=f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}",
                    max_tokens_to_sample=max_tokens,
                    temperature=temperature
                )
                return response.completion
        except Exception as e:
            print(f"Anthropic API Error: {str(e)}")
            raise

class DeepVoid:
    """Generates artifacts from the void using AI APIs"""
    
    def __init__(self, api_client):
        """Initialize with an API client"""
        from prompt_library import PromptLibrary
        
        self.api_client = api_client
        self.prompt_library = PromptLibrary()
        
    def generate_single(self, rarity=None, category=None):
        """Generate a single artifact"""
        if rarity is None:
            rarity = Rarity.weighted_random()
            
        if category is None:
            category = Category.get_random()
            
        # Get prompt for the specified rarity and category
        prompt_template = self.prompt_library.get_prompt_for_category_and_rarity(category, rarity)
        
        # Generate content
        response = self.api_client.generate(prompt_template["prompt"])
        
        # Parse the response
        artifact = self._parse_artifact_response(response)
        
        # Add metadata
        if not artifact.get("id"):
            artifact["id"] = generate_id()
        if not artifact.get("rarity"):
            artifact["rarity"] = rarity.value if isinstance(rarity, Rarity) else rarity
        if not artifact.get("category"):
            artifact["category"] = category.value if isinstance(category, Category) else category
            
        # Calculate value based on rarity
        artifact["value"] = self._calculate_value(artifact)
        
        return artifact
    
    def generate_batch(self, num_artifacts=5, rarities=None):
        """Generate multiple artifacts in a single API call"""
        # Determine rarities if not specified
        if rarities is None:
            rarities = [Rarity.weighted_random() for _ in range(num_artifacts)]
            
        # Create batch prompt
        batch_prompt = self.prompt_library.create_batch_prompt(num_artifacts, rarities)
        
        # Generate content
        response = self.api_client.generate(batch_prompt)
        
        # Parse batch response
        artifacts = self._parse_batch_response(response)
        
        # Add metadata and calculate values
        for i, artifact in enumerate(artifacts):
            if not artifact.get("id"):
                artifact["id"] = generate_id()
            if not artifact.get("rarity") and i < len(rarities):
                rarity = rarities[i]
                artifact["rarity"] = rarity.value if isinstance(rarity, Rarity) else rarity
            artifact["value"] = self._calculate_value(artifact)
            
        return artifacts
    
    def _parse_artifact_response(self, response):
        """Parse a single artifact from API response using structured markers."""
        artifact = {}

        # Use regex to find sections based on the new format
        name_match = re.search(r'^NAME:\s*(.+)$', response, re.MULTILINE)
        if name_match:
            artifact["name"] = name_match.group(1).strip()

        category_match = re.search(r'^CATEGORY:\s*(.+)$', response, re.MULTILINE)
        if category_match:
            artifact["category"] = category_match.group(1).strip()

        rarity_match = re.search(r'^RARITY:\s*(.+)$', response, re.MULTILINE)
        if rarity_match:
            artifact["rarity"] = rarity_match.group(1).strip()

        # Find the ASCII block using the fences
        ascii_match = re.search(r'^ASCII_ART:\s*\n```ascii\n(.+?)\n```', response, re.DOTALL | re.MULTILINE)
        if ascii_match:
            artifact["ascii_art"] = ascii_match.group(1).strip()

        # Find the Description block
        # Look for DESCRIPTION: followed by potentially whitespace and then the content
        description_match = re.search(r'^DESCRIPTION:\s*\n(.+)', response, re.DOTALL | re.MULTILINE)
        if description_match:
            artifact["description"] = description_match.group(1).strip()

        # Basic validation - ensure required fields are present
        if not artifact.get("name") or not artifact.get("ascii_art") or not artifact.get("description"):
            print("Warning: Failed to parse complete artifact. Missing required fields.")
            print("--- Raw Response ---")
            print(response)
            print("--------------------")
            return {} # Return empty dict for incomplete artifacts

        return artifact

    def _parse_batch_response(self, response):
        """Parse multiple artifacts from a batch response, split by divider."""
        # Split by the divider defined in create_batch_prompt
        sections = response.split('----------')

        artifacts = []
        for section in sections:
            if not section.strip():
                continue

            # Parse each section as a single artifact response
            artifact = self._parse_artifact_response(section)
            if artifact:  # Only add successfully parsed artifacts
                artifacts.append(artifact)

        return artifacts

    
    def _calculate_value(self, artifact):
        """Calculate the value of an artifact based on rarity"""
        rarity_str = artifact.get("rarity", "common")
        
        # Convert string to Rarity enum if needed
        rarity = None
        for r in Rarity:
            if r.value == rarity_str:
                rarity = r
                break
                
        if not rarity:
            rarity = Rarity.COMMON
            
        # Get value range for the rarity
        min_val, max_val = Rarity.get_value_range(rarity)
        
        # Random value within range
        base_value = random.randint(min_val, max_val)
        
        # Apply modifier based on text length and complexity
        description = artifact.get("description", "")
        ascii_art = artifact.get("ascii_art", "")
        
        # Simple complexity estimation
        art_complexity = min(1.5, len(ascii_art) / 500)
        desc_complexity = min(1.5, len(description) / 1000)
        
        complexity_modifier = (art_complexity + desc_complexity) / 2
        
        # Calculate final value
        value = int(base_value * complexity_modifier)
        
        return max(1, value)  # Ensure minimum value of 1