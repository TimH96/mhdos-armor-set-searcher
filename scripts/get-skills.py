import json

CATEGORIES = [
    ["Status", "Expert", "Attack", "Potential", "Defense", "Protection"],
    ["Health", "Recover Speed", "Stamina", "Hunger"],
    ["Evasion", "Guard", "Auto-Guard"],
    [
        "Heat Resistance",
        "Cold Resistance",
        "Stun",
        "Vocal Chords",
        "Tremor Resistance",
        "Terrain",
        "Snow Resistance",
        "Earplugs",
        "Fire Resistance",
        "Water Resistance",
        "Ice Resistance",
        "Thunder Resistance",
        "Dragon Resistance",
        "Element Resistance",
        "Wind Pressure",
        "Paralysis",
        "Poison",
        "Sleep",
        "Antiseptic",
    ],
    [
        "Alchemy",
        "Wide-Range",
        "Combo Rate",
        "Cooking",
        "Fishing",
        "Lasting Power",
        "Bomb Boost",
        "Fisher",
        "Eating",
        "Whim",
        "Gluttony",
        "Throw",
        "Recovery Items",
        "Artillery",
    ],
    ["Sharpness", "Handicraft", "Speed Sharpening"],
    [
        "Normal S Up",
        "Normal S+",
        "Pellet S Up",
        "Pellet S+",
        "Pierce S Up",
        "Pierce S+",
        "Clust S+",
        "Crag S+",
        "Precision",
        "Rapid-Fire",
        "Recoil",
        "Reload Speed",
        "Ammo Maker",
        "Load",
    ],
    [
        "Sense",
        "Psychic",
        "Gathering",
        "Speed Gathering",
        "Carving",
        "Transporter",
        "Monster",
        "Map",
        "Fate",
        "Anti-Theft",
    ],
]


def find_category(skill_name: str) -> int:
    for (i, cat) in enumerate(CATEGORIES):
        if skill_name in cat:
            return i

    return 8


def clean_name(s: str) -> str:
    return s.split("<")[0]


if __name__ == "__main__":
    # read input
    with open("./raw-skills.json") as f:
        skills = list(json.loads(f.read()))

    # init output
    skill_names = {}
    skill_activations = {}
    id_mapping = {}

    # iterate over skills
    activations_id = 0

    for (id, skill) in enumerate(skills):
        # get attributes
        name = skill["name"]
        category = find_category(name)

        # init skill map and skill names map
        acts = []
        skill_names[id] = name

        # handle torso up
        if name == "Torso Up":
            skill_activations[id] = []
            continue

        # iterate over activations of this skill
        for activation in skill["stagesFormatted"]:
            # bump activations id
            a_id = activations_id
            activations_id += 1

            # get attributes
            points = int(activation["points"])
            is_positive = bool(points > 0)
            a_name = clean_name(activation["name"])

            # model and push object
            modeled_activation = {
                "category": category,
                "id": a_id,
                "isPositive": is_positive,
                "name": a_name,
                "requiredPoints": points,
                "requiredSkill": id,
            }
            acts.append(modeled_activation)

        # reverse acts (positive acts should be first) and append to map
        acts.reverse()
        skill_activations[id] = acts

    # save files
    with open("../data/skills.json", "w") as f:
        f.write(json.dumps(skill_activations, indent=4))
    with open("../data/skill-names.json", "w") as f:
        f.write(json.dumps(skill_names, indent=4))
