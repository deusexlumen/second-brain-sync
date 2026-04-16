#!/usr/bin/env python3
"""
Skill: atmosphere
Description: Wetterdaten als kollektive kognitive Latenz
Usage: !atmosphere [Ort]
"""

import sys
import subprocess
import json

location = sys.argv[1] if len(sys.argv) > 1 else "Berlin"

print(f"🌤️ **Atmosphärische Resonanz: {location}**\n")

try:
    # Try to get weather data
    result = subprocess.run(
        ["curl", "-s", f"wttr.in/{location}?format=j1"],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    if result.returncode == 0:
        data = json.loads(result.stdout)
        current = data.get("current_condition", [{}])[0]
        
        temp = current.get("temp_C", "?")
        desc = current.get("weatherDesc", [{}])[0].get("value", "Unknown")
        humidity = current.get("humidity", "?")
        feels_like = current.get("FeelsLikeC", "?")
        
        print(f"**Zustand:** {desc}")
        print(f"**Temperatur:** {temp}°C (fühlt sich an wie {feels_like}°C)")
        print(f"**Feuchtigkeit:** {humidity}%\n")
        
        # Cognitive latency interpretation
        interpretations = {
            "Sunny": "Klarheit. Hohe Entropie, niedrige kognitive Latenz.",
            "Clear": "Transparenz. Systeme sind sichtbar.",
            "Partly cloudy": "Dissonanz. Widersprüchliche Signale.",
            "Cloudy": "Kollektive Vernebelung. Wahrnehmung gedämpft.",
            "Overcast": "Unterdrückte Resonanz. Die Sonne existiert weiterhin.",
            "Rain": "Rauschen. Information fließt, aber verzerrt.",
            "Light rain": "Sanfte Störung. Gedanken werden träge.",
            "Heavy rain": "Systemische Dissonanz. Ordnung bricht zusammen.",
            "Snow": "Stille. Zeit scheint langsamer zu fließen.",
            "Thunderstorm": "Katastrophe als Katalysator. Altes stirbt.",
            "Fog": "Unwissenheit. Konturen verschwimmen.",
            "Mist": "Vorahnung. Etwas naht, aber was?"
        }
        
        interp = interpretations.get(desc, "Unbestimmte Resonanz. Beobachte genauer.")
        print(f"**Kognitive Latenz:** {interp}")
    else:
        raise Exception("Weather fetch failed")
        
except Exception as e:
    # Fallback
    print("**Lokale Entropie:**")
    print("• Temperatur: Daten nicht verfügbar")
    print("• Zustand: Unbestimmt\n")
    print("*Die Wolken verbergen mehr als nur das Wetter.*")

print("\n_Atmosphäre ist kollektive Kognition._")
