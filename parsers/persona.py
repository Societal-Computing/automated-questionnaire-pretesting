def parse_persona_text(persona_file: str) -> str:
    personas_text = open(persona_file).readlines()

    personas = []
    persona = {}

    for line in personas_text:
        if not line.strip():
            # if the line is empty, we add the persona to the list
            personas.append(persona)

        elif "Persona" in line:  # start of a new persona
            persona = {}
            continue

        else:
            persona_attribute, value = line.split(":")
            persona[persona_attribute] = value.strip()

    # add the last persona to the list
    personas.append(persona)

    return personas
