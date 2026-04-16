#!/usr/bin/env python3
"""
Imagen Client with Rate Limit Tracking
Supports three models with 25 requests per day each.
"""

import os
import json
import base64
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Literal

# Rate limit configuration
RATE_LIMIT = 25
# Imagen 3 model names (latest stable version)
MODELS = {
    "generate": "imagen-3.0-generate-002",
    "ultra": "imagen-3.0-generate-002",
    "fast": "imagen-3.0-fast-generate-001"
}

ASPECT_RATIOS = ["1:1", "3:4", "4:3", "9:16", "16:9"]
PERSON_GENERATION = ["dont_allow", "allow_adult", "allow_all"]

class RateLimitTracker:
    """Tracks rate limits per model with daily reset."""
    
    def __init__(self, storage_path: Optional[str] = None):
        if storage_path is None:
            skill_dir = Path(__file__).parent.parent
            storage_path = skill_dir / "references" / "rate_limits.json"
        
        self.storage_path = Path(storage_path)
        self.data = self._load()
    
    def _load(self) -> dict:
        """Load rate limit data from file."""
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return self._init_data()
    
    def _init_data(self) -> dict:
        """Initialize fresh rate limit data."""
        return {
            model: {
                "count": 0,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "history": []
            }
            for model in MODELS.values()
        }
    
    def _save(self):
        """Save rate limit data to file."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def _check_reset(self, model: str):
        """Reset counter if it's a new day."""
        today = datetime.now().strftime("%Y-%m-%d")
        if self.data[model]["date"] != today:
            # Archive yesterday's data
            if self.data[model]["count"] > 0:
                self.data[model]["history"].append({
                    "date": self.data[model]["date"],
                    "count": self.data[model]["count"]
                })
                # Keep only last 30 days
                self.data[model]["history"] = self.data[model]["history"][-30:]
            
            self.data[model]["count"] = 0
            self.data[model]["date"] = today
            self._save()
    
    def can_request(self, model: str) -> bool:
        """Check if a request can be made for the given model."""
        self._check_reset(model)
        return self.data[model]["count"] < RATE_LIMIT
    
    def record_request(self, model: str, count: int = 1):
        """Record that requests were made."""
        self._check_reset(model)
        self.data[model]["count"] += count
        self._save()
    
    def get_status(self, model: Optional[str] = None) -> dict:
        """Get current rate limit status."""
        if model:
            self._check_reset(model)
            return {
                "used": self.data[model]["count"],
                "limit": RATE_LIMIT,
                "remaining": RATE_LIMIT - self.data[model]["count"],
                "date": self.data[model]["date"],
                "resets": self._get_reset_time()
            }
        
        return {
            key: self.get_status(full_model)
            for key, full_model in MODELS.items()
        }
    
    def _get_reset_time(self) -> str:
        """Get the time when limits reset (midnight UTC)."""
        tomorrow = datetime.now() + timedelta(days=1)
        reset = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        return reset.strftime("%Y-%m-%d %H:%M:%S")


class ImagenClient:
    """Client for generating images with Imagen models."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            # Try to load from config
            config_path = Path.home() / ".openclaw" / "config" / "gemini.env"
            if config_path.exists():
                with open(config_path) as f:
                    for line in f:
                        if line.startswith("GEMINI_API_KEY="):
                            self.api_key = line.strip().split("=", 1)[1]
                            break
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found. Set it as environment variable or in ~/.openclaw/config/gemini.env")
        
        self.rate_tracker = RateLimitTracker()
    
    def generate(
        self,
        prompt: str,
        model: Literal["generate", "ultra", "fast"] = "generate",
        count: int = 1,
        aspect_ratio: str = "1:1",
        size: Optional[str] = None,
        person_generation: str = "allow_adult",
        output_dir: Optional[str] = None
    ) -> dict:
        """
        Generate images using Imagen.
        
        Args:
            prompt: Text description of desired image
            model: Model variant to use
            count: Number of images (1-4)
            aspect_ratio: Image aspect ratio
            size: Image size (1K or 2K, ultra/generate only)
            person_generation: Person generation policy
            output_dir: Where to save images
        
        Returns:
            Dictionary with generated image paths and metadata
        """
        # Validate inputs
        if model not in MODELS:
            raise ValueError(f"Model must be one of: {list(MODELS.keys())}")
        
        if count < 1 or count > 4:
            raise ValueError("Count must be between 1 and 4")
        
        if aspect_ratio not in ASPECT_RATIOS:
            raise ValueError(f"Aspect ratio must be one of: {ASPECT_RATIOS}")
        
        if person_generation not in PERSON_GENERATION:
            raise ValueError(f"Person generation must be one of: {PERSON_GENERATION}")
        
        # Check rate limits
        full_model = MODELS[model]
        if not self.rate_tracker.can_request(full_model):
            status = self.rate_tracker.get_status(full_model)
            raise RateLimitExceeded(
                f"Rate limit exceeded for {full_model}. "
                f"Used: {status['used']}/{status['limit']}. "
                f"Resets at: {status['resets']}"
            )
        
        # Build request
        try:
            from google import genai
            from google.genai import types
        except ImportError:
            raise ImportError("google-genai package required. Install with: pip install google-genai")
        
        client = genai.Client(api_key=self.api_key)
        
        config = types.GenerateImagesConfig(
            number_of_images=count,
            aspect_ratio=aspect_ratio,
            person_generation=person_generation
        )
        
        if size and model in ["generate", "ultra"]:
            config.image_size = size
        
        # Make request
        response = client.models.generate_images(
            model=full_model,
            prompt=prompt,
            config=config
        )
        
        # Record usage
        self.rate_tracker.record_request(full_model, count)
        
        # Save images
        if output_dir is None:
            output_dir = "/tmp/imagen-output"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        saved_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for idx, generated_image in enumerate(response.generated_images):
            img_bytes = generated_image.image.image_bytes
            filename = f"imagen_{model}_{timestamp}_{idx+1}.png"
            filepath = output_path / filename
            
            with open(filepath, 'wb') as f:
                f.write(img_bytes)
            
            saved_files.append(str(filepath))
        
        return {
            "files": saved_files,
            "model": full_model,
            "prompt": prompt,
            "count": count,
            "rate_limit_status": self.rate_tracker.get_status(full_model)
        }
    
    def get_rate_limits(self) -> dict:
        """Get current rate limit status for all models."""
        return self.rate_tracker.get_status()


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""
    pass


class PromptEnhancer:
    """Enhances simple prompts with professional modifiers."""
    
    STYLE_PRESETS = {
        "photo": "photorealistic, professional photography, sharp focus, detailed",
        "portrait": "35mm portrait, professional lighting, shallow depth of field, bokeh",
        "product": "studio photography, soft lighting, clean background, 85mm lens, product shot",
        "landscape": "landscape photography, wide angle, dramatic sky, sharp focus throughout, 4K HDR",
        "art": "digital art, highly detailed, vibrant colors, masterpiece",
        "fantasy": "fantasy art, epic scale, dramatic lighting, digital painting, detailed",
        "minimal": "minimalist, clean composition, simple background, professional",
        "vintage": "vintage photograph, film grain, nostalgic atmosphere, soft colors",
        "cyberpunk": "cyberpunk aesthetic, neon lights, futuristic, highly detailed, 4K",
        "watercolor": "watercolor painting, soft edges, artistic, flowing colors"
    }
    
    QUALITY_BOOSTERS = [
        "high quality",
        "detailed",
        "professional",
        "beautiful"
    ]
    
    @classmethod
    def enhance(cls, prompt: str, style: str = None, quality: bool = True) -> str:
        """Enhance a simple prompt with style and quality modifiers."""
        enhanced = prompt.strip()
        
        # Add style preset if specified
        if style and style in cls.STYLE_PRESETS:
            enhanced += f", {cls.STYLE_PRESETS[style]}"
        
        # Add quality boosters if requested (but avoid duplicates)
        if quality:
            for booster in cls.QUALITY_BOOSTERS:
                if booster.lower() not in enhanced.lower():
                    enhanced += f", {booster}"
                    break  # Just add one to avoid overloading
        
        return enhanced
    
    @classmethod
    def list_styles(cls) -> list:
        """Return available style presets."""
        return list(cls.STYLE_PRESETS.keys())


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate images with Imagen")
    parser.add_argument("prompt", help="Image description")
    parser.add_argument("--model", choices=["generate", "ultra", "fast"], default="generate")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--aspect", choices=ASPECT_RATIOS, default="1:1")
    parser.add_argument("--size", choices=["1K", "2K"], default=None)
    parser.add_argument("--person-generation", choices=PERSON_GENERATION, default="allow_adult")
    parser.add_argument("--output", default="/tmp/imagen-output")
    parser.add_argument("--check-limits", action="store_true", help="Check rate limits only")
    parser.add_argument("--enhance", action="store_true", help="Show enhanced prompt without generating")
    parser.add_argument("--style", choices=list(PromptEnhancer.STYLE_PRESETS.keys()), 
                       help="Apply style preset to enhance prompt")
    parser.add_argument("--no-quality", action="store_true", help="Skip quality boosters")
    parser.add_argument("--list-styles", action="store_true", help="List available style presets")
    
    args = parser.parse_args()
    
    client = ImagenClient()
    
    if args.list_styles:
        print("\n=== Available Style Presets ===\n")
        for style, description in PromptEnhancer.STYLE_PRESETS.items():
            print(f"  {style:12} — {description[:50]}...")
        print("\nUsage: imagen 'your prompt' --style portrait")
        exit(0)
    
    if args.check_limits:
        limits = client.get_rate_limits()
        print("\n=== Imagen Rate Limits ===\n")
        for model_name, status in limits.items():
            print(f"Model: {MODELS[model_name]}")
            print(f"  Used today: {status['used']}/{status['limit']}")
            print(f"  Remaining: {status['remaining']}")
            print(f"  Resets: {status['resets']}")
            print()
        exit(0)
    
    # Enhance prompt if requested
    original_prompt = args.prompt
    enhanced_prompt = PromptEnhancer.enhance(
        original_prompt, 
        style=args.style,
        quality=not args.no_quality
    )
    
    if args.enhance:
        print("\n=== Prompt Enhancement ===\n")
        print(f"Original:  {original_prompt}")
        print(f"Enhanced:  {enhanced_prompt}")
        print("\nUse this enhanced prompt for better results!")
        exit(0)
    
    if enhanced_prompt != original_prompt:
        print(f"\n✨ Enhanced prompt: {enhanced_prompt}\n")
    
    # Use enhanced prompt for generation
    try:
        result = client.generate(
            prompt=enhanced_prompt,
            model=args.model,
            count=args.count,
            aspect_ratio=args.aspect,
            size=args.size,
            person_generation=args.person_generation,
            output_dir=args.output
        )
        
        print(f"\n✓ Generated {result['count']} image(s) using {result['model']}")
        print(f"\nSaved files:")
        for f in result['files']:
            print(f"  - {f}")
        
        status = result['rate_limit_status']
        print(f"\nRate limit: {status['used']}/{status['limit']} used today")
        print(f"Remaining: {status['remaining']}")
        
    except RateLimitExceeded as e:
        print(f"\n✗ {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        exit(1)
