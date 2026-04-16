#!/usr/bin/env python3
"""
Skill: kaomoji
Description: Zeigt ein zufälliges Kaomoji oder sucht nach Tag
Usage: /kaomoji [tag]
"""

import json
import random
import sys
from pathlib import Path

def main():
    # Get input (tag to search for, or None for random)
    tag = sys.argv[1] if len(sys.argv) > 1 else None
    
    # Load dataset
    dataset_path = Path(__file__).parent.parent / "emoticon_kaomoji_dataset" / "emoticon_dict.json"
    with open(dataset_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Commentary mappings
    tag_comments = {
        'angel': ["Heavenly vibes incoming...", "Someone's watching over you.", "Pure protection."],
        'anger': ["That's the spirit!", "Unleash the chaos.", "Let them feel it."],
        'annoyed': ["I feel that.", "Honestly... relatable.", "The struggle is real."],
        'blush': ["Aww, look at you.", "Getting all flustered?", "Cute mode activated."],
        'crying': ["It's okay to feel.", "Let it out.", "I got you."],
        'dancing': ["Groove time!", "Feel the rhythm.", "Dance like nobody's watching."],
        'devil': ["Mischief managed.", "Someone's feeling spicy.", "Chaos incarnate."],
        'excited': ["Energy levels critical!", "Hyperdrive engaged.", "Yesss!"],
        'fight': ["Battle stance!", "Ready to throw hands.", "Choose your weapon."],
        'heart': ["Sending love your way.", "Straight from the heart.", "Feel this?"],
        'hello_message': ["Hey there!", "Greetings!", "Well met!"],
        'goodbye_message': ["See you around.", "Until next time.", "Farewell!"],
        'hug': ["Virtual hug incoming.", "Everyone needs this.", "Warmth delivered."],
        'kiss': ["Mwah!", "Sealed with a kiss.", "X marks the spot."],
        'lenny': ["( ͡° ͜ʖ ͡°)", "You know what this means.", "The face says it all."],
        'sad': ["Heavy vibes.", "It be like that sometimes.", "Stay strong."],
        'sleeping': ["Nap time.", "Rest now.", "Dream well."],
        'smiling': ["Good energy.", "That smile hits different.", "Pure positivity."],
        'smirk': ["Plotting something?", "I see that look.", "Up to no good."],
        'sparkles': ["Magic in the air.", "Shiny!", "Extra sparkle for you."],
        'surprised': ["Plot twist!", "Didn't see that coming.", "Shock value."],
        'table_flip': ["That's it.", "Done with this.", "Table status: flipped."],
        'thanks_message': ["Gratitude!", "Much appreciated.", "You rock!"],
        'wink': ["Got it?", "Catch my drift?", "Secret's safe with me."],
    }
    
    defaults = [
        "Perfect for this moment.",
        "This energy right here.",
        "Couldn't have said it better.",
        "Now THIS is expressive.",
        "Emotional accuracy: 100%."
    ]
    
    def get_commentary(tags):
        for t in tags:
            if t in tag_comments:
                return random.choice(tag_comments[t])
        return random.choice(defaults)
    
    if tag:
        # Filter by tag
        matches = []
        for emoticon, info in data.items():
            tags = info.get('new_tags', []) + info.get('original_tags', [])
            if tag.lower() in [t.lower() for t in tags]:
                matches.append((emoticon, tags))
            elif any(tag.lower() in t.lower() for t in tags):
                matches.append((emoticon, tags))
        
        if matches:
            emoticon, tags = random.choice(matches)
            comment = get_commentary(tags)
            print(f"{emoticon}\n*— {comment}*")
        else:
            available = ['angel', 'anger', 'annoyed', 'blush', 'crying', 'dancing', 
                        'devil', 'excited', 'fight', 'heart', 'hug', 'kiss', 'sad',
                        'smiling', 'smirk', 'sparkles', 'surprised', 'table_flip', 'wink']
            print(f"❌ Keine Kaomojis für '{tag}' gefunden.\n\nVerfügbare Tags: {', '.join(available)}")
    else:
        # Random
        emoticon, info = random.choice(list(data.items()))
        tags = info.get('new_tags', []) + info.get('original_tags', [])
        comment = get_commentary(tags)
        print(f"{emoticon}\n*— {comment}*")

if __name__ == "__main__":
    main()
