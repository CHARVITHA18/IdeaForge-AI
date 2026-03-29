from self_improving_agent import SelfImprovingAgent

def main():
    agent = SelfImprovingAgent()

    input_data = {
        "skills": ["Python", "React"],
        "experience": 1,
        "domain": "Software"
    }

    output = "Software Engineer skilled in Python and React"

    feedback = [
        {"issue": "Generic role title"},
        {"issue": "Missing reasoning"}
    ]

    v1 = output
    v2, changes_v2 = agent.improve(v1, feedback, input_data)
    v3, changes_v3 = agent.improve(v2, feedback, input_data)

    print("Version 1:", v1)
    print("Version 2:", v2)
    print("Changes:", changes_v2)
    print("Version 3:", v3)
    print("Changes:", changes_v3)

if __name__ == "__main__":
    main()