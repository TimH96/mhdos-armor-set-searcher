import json

CATEGORIES = []

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
        category = 0

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
