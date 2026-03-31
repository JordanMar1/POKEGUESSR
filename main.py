import requests
import random
import unicodedata
from playsound import playsound


def normalize(text):
    text = text.lower()
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text

#get french data
def get_french_name(species):
    for name in species["names"]:
        if name["language"]["name"] == "fr":
            return name["name"]
    return species["name"]

def get_french_color(color_url):
    data = requests.get(color_url).json()
    for name in data["names"]:
        if name["language"]["name"] == "fr":
            return name["name"]
    return data["name"]

def get_french_abilities(abilities):
    fr_abilities = []
    for ab in abilities:
        data = requests.get(ab["ability"]["url"]).json()
        for name in data["names"]:
            if name["language"]["name"] == "fr":
                fr_abilities.append(name["name"])
                break
    return fr_abilities

def get_french_shape(shape_url):
    data = requests.get(shape_url).json()
    for name in data["names"]:
        if name["language"]["name"] == "fr":
            return name["name"]
    return data["name"]

def get_french_types(types):
    fr_types = []
    for t in types:
        type_data = requests.get(t["type"]["url"]).json()
        for name in type_data["names"]:
            if name["language"]["name"] == "fr":
                fr_types.append(name["name"])
                break
    return fr_types

def clean_description(text, pokemon_name):
    text = text.replace("\n", " ").replace("\f", " ")
    name = pokemon_name.lower()
    words = text.split()
    cleaned_words = []
    for w in words:
        if name not in w.lower():
            cleaned_words.append(w)
    return " ".join(cleaned_words)

def get_french_genera(species):
    for genus in species["genera"]:
        if genus["language"]["name"] == "fr":
            return genus["genus"]
    return "Catégorie inconnue"

def get_french_description(species, pokemon_name):
    for entry in species["flavor_text_entries"]:
        if entry["language"]["name"] == "fr":
            raw = entry["flavor_text"]
            return clean_description(raw, pokemon_name)
    return "Pas de description disponible."

def get_french_generation(gen_url):
    data = requests.get(gen_url).json()
    for name in data["names"]:
        if name["language"]["name"] == "fr":
            return name["name"]
    return data["name"]

#get random pokemon
def get_random_pokemon():
    poke_id = random.randint(1, 1005)

    pokemon = requests.get(f"https://pokeapi.co/api/v2/pokemon/{poke_id}").json()
    species = requests.get(pokemon["species"]["url"]).json()

    return {
        "name": get_french_name(species),
        "types": get_french_types(pokemon["types"]),
        "color": get_french_color(species["color"]["url"]),
        "capture_rate": species["capture_rate"],
        "generation": get_french_generation(species["generation"]["url"]),
        "description": get_french_description(species, get_french_name(species)),
        "shape": get_french_shape(species["shape"]["url"]),
        "abilities": get_french_abilities(pokemon["abilities"]),
        "genera": get_french_genera(species),
        "cry": f"https://play.pokemonshowdown.com/audio/cries/{pokemon['name']}.mp3"
    }

#downloads and plays a cry
def play_cry(url):
    filename = "cry.mp3"
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)
    playsound(filename)

#play to the game
def play():
    poke = get_random_pokemon()
    attempts = 0
    print("🎮 Devine le Pokémon !")
    play_cry(poke["cry"])
    while True:
        guess = input("Ta réponse: ")
        attempts += 1
        if normalize(guess) in ["exit", "abandon"]:
            print(f"🚪 Tu fuis. C'était {poke['name']}")
            break
        if normalize(guess) in ["sound", "replay"]:
            playsound("cry.mp3")
            attempts -= 1
            continue
        if normalize(guess) == normalize(poke["name"]):
            print(f"✅ Bien joué ! C'était {poke['name']} en {attempts} tentatives.")
            break
        if attempts % 8 == 0:
            print("👉 Description:", poke["description"])
        elif attempts % 8 == 1:
            print("👉 Forme:", poke["shape"])
        elif attempts % 8 == 2:
            print("👉 Couleur:", poke["color"])
        elif attempts % 8 == 3:
            print("👉 Taux de capture:", poke["capture_rate"])
        elif attempts % 8 == 4:
            print("👉 Génération:", poke["generation"])
        elif attempts % 8 == 5:
            print("👉 Capacités:", ", ".join(poke["abilities"]))
        elif attempts % 8 == 6:
            print("👉 Type:", ", ".join(poke["types"]))
        elif attempts % 8 == 7:
            print("👉 Catégorie:", poke["genera"])

if __name__ == "__main__":
    play()
