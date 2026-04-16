---
name: imagen-generation
description: Generate images using Google's Imagen 4 models with auto-enhanced prompts and rate limit tracking. Features smart prompt enhancement with 10 style presets.
---

# Imagen Image Generation

Generate high-quality images using Google's Imagen 4 models with **automatic prompt enhancement** and built-in rate limit tracking.

## Available Models

| Model | Quality | Speed | Best For |
|-------|---------|-------|----------|
| `imagen-4.0-generate-001` | High | Standard | Balanced quality and speed |
| `imagen-4.0-ultra-generate-001` | Ultra High | Slower | Maximum quality, detailed images |
| `imagen-4.0-fast-generate-001` | Good | Fast | Quick iterations, drafts |

**Rate Limit: 25 requests per day per model (75 total per day)**

## Quick Start — 30 Seconds

### 1. Setup (one-time)

```bash
source ~/.openclaw/workspace/skills/imagen-generation/aliases.sh
```

Or add to `~/.bashrc` for permanent access.

### 2. Generate Images

```bash
# Simple — auto-enhanced
imagen "ein roter Apfel auf Holz"

# With style preset
imagen "eine Frau" --style portrait

# Professional quality
imagen "ein futuristisches Auto" --model ultra

# Check what's available
imgen-styles
```

## Smart Prompt Enhancement ✨

The skill **automatically improves your prompts** with professional modifiers. Type less, get better results.

### Style Presets

| Preset | Adds |
|--------|------|
| `photo` | photorealistic, professional photography, sharp focus, detailed |
| `portrait` | 35mm portrait, professional lighting, shallow depth of field |
| `product` | studio photography, soft lighting, clean background, 85mm lens |
| `landscape` | landscape photography, wide angle, dramatic sky, 4K HDR |
| `art` | digital art, highly detailed, vibrant colors, masterpiece |
| `fantasy` | fantasy art, epic scale, dramatic lighting, digital painting |
| `minimal` | minimalist, clean composition, simple background, professional |
| `vintage` | vintage photograph, film grain, nostalgic atmosphere |
| `cyberpunk` | cyberpunk aesthetic, neon lights, futuristic, 4K |
| `watercolor` | watercolor painting, soft edges, artistic |

### Examples — Before & After

| Your Input | Enhanced Prompt |
|------------|-----------------|
| `ein Apfel` | `ein Apfel, high quality, detailed` |
| `ein Apfel --style photo` | `ein Apfel, photorealistic, professional photography, sharp focus, detailed, high quality` |
| `ein Apfel --style portrait` | `ein Apfel, 35mm portrait, professional lighting, shallow depth of field, bokeh, high quality` |

### Preview Enhancement

See what the AI will use **before generating**:

```bash
imagen "eine Katze" --style photo --enhance
# Shows: eine Katze, photorealistic, professional photography, sharp focus, detailed, high quality
```

## Commands Reference

| Command | Description |
|---------|-------------|
| `imagen "prompt"` | Generate with auto-enhancement |
| `imagen "prompt" --style photo` | Apply style preset |
| `imagen "prompt" --enhance` | Show enhanced prompt only |
| `imgen-styles` | List all style presets |
| `imgen-limits` | Check rate limits |
| `imagen "prompt" --model ultra` | Use ultra quality model |

### Parameters

- `--style [preset]` — Apply style preset (see list above)
- `--model [generate|ultra|fast]` — Select model variant
- `--count [1-4]` — Number of images (default: 1)
- `--aspect [1:1|3:4|4:3|9:16|16:9]` — Aspect ratio (default: 1:1)
- `--size [1K|2K]` — Image size (ultra/generate only)
- `--no-quality` — Skip auto-quality boosters
- `--enhance` — Show enhanced prompt without generating

## Full Examples

```bash
# Portrait photography
imagen "eine Frau im Café" --style portrait --aspect 9:16

# Product shot
imagen "eine Uhr" --style product --model ultra

# Landscape
imagen "Berge bei Sonnenaufgang" --style landscape --aspect 16:9

# Fantasy art
imagen "eine schwebende Burg" --style fantasy

# Cyberpunk city
imagen "eine Neon-Stadt" --style cyberpunk --model ultra

# Fast draft (for testing)
img "Logo-Idee: Berg" --model fast
```

## Python API

```python
from skills.imagen_generation.scripts.imagen_client import ImagenClient, PromptEnhancer

client = ImagenClient()

# Auto-enhance and generate
result = client.generate(
    prompt="A beautiful garden",
    model="generate",
    style="photo",  # Auto-applies style preset
    count=2,
    aspect_ratio="16:9"
)

# Manual enhancement
enhanced = PromptEnhancer.enhance(
    "ein Apfel",
    style="product",
    quality=True
)
print(enhanced)  # "ein Apfel, studio photography, soft lighting..."

# Check limits
limits = client.get_rate_limits()
```

## Rate Limit Tracking

```bash
imgen-limits
```

Output:
```
Model: imagen-4.0-generate-001
  Used today: 12/25
  Remaining: 13
  Resets: 2026-04-13 00:00:00

Model: imagen-4.0-ultra-generate-001
  Used today: 5/25
  Remaining: 20
```

## Configuration

### API Key

```bash
# In ~/.openclaw/config/gemini.env:
GEMINI_API_KEY=your-key-here
```

### Person Generation

```bash
# Default (adults only)
imagen "prompt"

# No people
imagen "prompt" --person-generation dont_allow

# Adults and children (not EU/UK/CH)
imagen "prompt" --person-generation allow_all
```

## File Structure

```
~/.openclaw/workspace/skills/imagen-generation/
├── SKILL.md                    # This documentation
├── aliases.sh                  # Shell aliases
└── scripts/
    ├── imagen_client.py        # Python client with PromptEnhancer
    └── ...
```

## Tips

1. **Start simple** — Let the enhancer do the work
2. **Use styles** — Pick the closest preset for your needs
3. **Test first** — Use `--model fast` for quick drafts
4. **Preview** — Use `--enhance` to see what the AI gets
5. **Iterate** — Try different styles on the same base prompt

---

*Auto-enhancement: Every prompt gets professional modifiers automatically. Just type what you want, the skill makes it better.*
