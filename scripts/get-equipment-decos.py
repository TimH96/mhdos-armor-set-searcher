import json


def reorder_resistances(raw: list) -> list:
    return [
        raw[0],
        raw[1],
        raw[3],
        raw[2],
        raw[4],
    ]


def map_skills_map(raw: dict, skill_ids: dict) -> dict:
    skills = {}
    for s in raw:
        n = s["k"]
        id = skill_ids[n]
        try:
            v = int(s["q"])
        except:
            v = 0  # torso up
        skills[id] = v

    return skills


def map_deco(raw: dict, skill_ids: dict) -> dict:
    return {
        "name": raw["name"],
        "rarity": raw["rarity"],
        "requiredSlots": raw["slots"],
        "skills": map_skills_map(raw["skills"], skill_ids),
    }


if __name__ == "__main__":
    # read input
    with open("./raw-decos.json") as f:
        decos = list(json.loads(f.read()))
    with open("./raw-armor.json") as f:
        armor = list(json.loads(f.read()))
    with open("../data/skill-names.json") as f:
        skill_names = dict(json.loads(f.read()))

    # reverse skill names
    skill_ids = {v: int(k) for k, v in skill_names.items()}

    # decorations
    modeled_decos = [map_deco(x, skill_ids) for x in decos]

    # iterate over armor categories
    pieces_per_category = []
    for (cat_index, armor_category) in enumerate(armor):
        pieces_of_cat = []
        # iterate over pieces of that category
        for piece in armor_category["armor"]:
            # get attributes
            name = piece["name"]
            if name == "None":
                continue
            defe = piece["defense"]
            skills = piece.get("skills", [])

            # skip if unacquirable
            if piece.get("acquire", 0) or piece.get("dev", 0):
                continue

            # get type
            x = piece.get("hunterClass", "")
            type = 1 if x == "Blademaster" else 2 if x == "Gunner" else 0

            # model and push piece
            modeled_piece = {
                "category": cat_index,
                "name": name,
                "rarity": piece["rarity"],
                "skills": map_skills_map(skills, skill_ids),
                "slots": piece["slots"][-1],
                "defense": {
                    "base": defe[0],
                    "max": defe[-1],
                },
                "type": type,
                "resistance": reorder_resistances(piece["resistances"]),
            }
            pieces_of_cat.append(modeled_piece)
        pieces_per_category.append(pieces_of_cat)

    # save files
    for (i, cat_name) in enumerate(["head", "chest", "arms", "waist", "legs"]):
        with open(f"../data/{cat_name}.json", "w") as f:
            f.write(json.dumps(pieces_per_category[i], indent=4, sort_keys=True))
    with open("../data/decorations.json", "w") as f:
        f.write(json.dumps(modeled_decos, indent=4))
