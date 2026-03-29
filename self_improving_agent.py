import time

def divider(char="─", width=60):
    print(char * width)
 
def section(title: str):
    divider()
    print(f"  {title}")
    divider()

class SelfImprovingAgent:
    def __init__(self):
        self.history = []
 
   
    def generate(self, input_data: dict) -> str:
        """Produce an initial (deliberately rough) decision."""
        primary_skill = input_data["skills"][0] if input_data["skills"] else "Programming"
        level = input_data["experience"]
        domain = input_data.get("domain", "Software")
        return (
            f"Candidate is suitable for {domain} Engineer role "
            f"(experience: {level}, skill: {primary_skill})."
        )
 
    
    def evaluate(self, output: str, input_data: dict) -> list[dict]:
        """
        Return a list of feedback items.
        Each item: {"issue": str, "reason": str}
        """
        feedback = []
        skills   = [s.lower() for s in input_data["skills"]]
        level    = input_data["experience"].lower()
        domain   = input_data.get("domain", "Software").lower()
 
        
        if "engineer" in output.lower() and not any(
            spec in output.lower()
            for spec in ["backend", "frontend", "fullstack", "data", "ml", "devops", "mobile"]
        ):
            feedback.append({
                "issue": "Generic role title",
                "reason": "Role title is too broad; should reflect the candidate's actual skill stack."
            })
 
        
        if "because" not in output.lower():
            feedback.append({
                "issue": "Missing reasoning",
                "reason": "Decision lacks a justification sentence explaining why this role fits."
            })
 
        
        highlighted = ["python", "javascript", "java", "react", "node", "sql",
                       "machine learning", "ml", "docker", "kubernetes", "aws"]
        matched = [s for s in skills if any(h in s for h in highlighted)]
        if matched and not any(s in output.lower() for s in matched):
            feedback.append({
                "issue": "Key skills not referenced",
                "reason": f"Skills {matched} are strong signals but absent from the recommendation."
            })
 
        
        if level in ["fresher", "junior", "0-1 year", "< 1 year"] and "junior" not in output.lower():
            feedback.append({
                "issue": "Experience level not addressed",
                "reason": "Entry-level context should appear in the recommendation."
            })
 
        
        data_keywords = ["data", "ml", "machine learning", "analytics", "ai"]
        web_keywords  = ["react", "javascript", "html", "css", "node"]
        if any(d in skills for d in data_keywords) and "data" not in output.lower():
            feedback.append({
                "issue": "Domain mismatch",
                "reason": "Candidate has data/ML skills; recommendation should reflect a data-oriented role."
            })
        if any(w in skills for w in web_keywords) and "frontend" not in output.lower() and "fullstack" not in output.lower():
            if not any(d in skills for d in data_keywords):          # only if not already data-flagged
                feedback.append({
                    "issue": "Domain mismatch",
                    "reason": "Candidate has web skills; recommendation should reflect a frontend/fullstack role."
                })
 
        return feedback
 
 
    def improve(self, output: str, feedback: list[dict], input_data: dict) -> tuple[str, list[str]]:
        """
        Apply targeted patches based on feedback.
        Returns (improved_output, list_of_changes_made).
        """
        improved = output
        changes  = []
        skills   = [s.lower() for s in input_data["skills"]]
        level    = input_data["experience"]
        domain   = input_data.get("domain", "Software")
 
        issues = [f["issue"] for f in feedback]
 
        if "Generic role title" in issues or "Domain mismatch" in issues:
            data_kw = ["data", "ml", "machine learning", "analytics", "ai"]
            web_kw  = ["react", "javascript", "html", "node"]
            devops_kw = ["docker", "kubernetes", "aws", "linux", "ci/cd"]
 
            if any(d in skills for d in data_kw):
                specialised = "Data / ML Engineer"
            elif any(w in skills for w in web_kw) and "python" in skills:
                specialised = "Full-Stack Developer (Python + Web)"
            elif any(w in skills for w in web_kw):
                specialised = "Frontend Developer"
            elif any(d in skills for d in devops_kw):
                specialised = "DevOps / Cloud Engineer"
            elif "python" in skills:
                specialised = "Backend Developer (Python)"
            elif "java" in skills:
                specialised = "Backend Developer (Java)"
            else:
                specialised = f"{domain} Specialist"
 
            old_role = f"{domain} Engineer"
            if old_role in improved:
                improved = improved.replace(old_role, specialised)
                changes.append(f'Role title narrowed: "{old_role}" → "{specialised}"')
 
        if "Missing reasoning" in issues:
            top_skills = ", ".join(input_data["skills"][:3])
            improved += f" Because the candidate demonstrates proficiency in {top_skills}."
            changes.append("Added a reasoning sentence listing top skills.")
 
        if "Key skills not referenced" in issues:
            highlighted = ["python", "javascript", "react", "sql", "docker", "aws",
                           "machine learning", "node"]
            matched = [s for s in skills if any(h in s for h in highlighted)]
            if matched:
                skill_str = " & ".join(s.title() for s in matched[:2])
                improved += f" Strongest technical signals: {skill_str}."
                changes.append(f"Injected key skill references: {matched[:2]}")
 
        if "Experience level not addressed" in issues:
            improved = improved.replace(
                "Candidate is suitable",
                f"Entry-level candidate is well-suited"
            )
            improved += " A junior role or mentored position is recommended."
            changes.append("Added entry-level / seniority context.")
 
        return improved, changes
 
    def run(self, input_data: dict, iterations: int = 3) -> str:
        output = self.generate(input_data)
 
        print("\n")
        section("INITIAL OUTPUT (Version 0 — unrefined)")
        print(f"\n  {output}\n")
        time.sleep(0.3)
 
        for i in range(iterations):
            feedback = self.evaluate(output, input_data)
 
            version_label = f"VERSION {i + 1}"
            section(version_label)
 
            if not feedback:
                print("  No issues found. Output is satisfactory — stopping early.\n")
                break
 
            print("  Issues found:")
            for fb in feedback:
                print(f"   • [{fb['issue']}] — {fb['reason']}")
            print()
 
            new_output, changes = self.improve(output, feedback, input_data)
 
            print(f"  Improved output:\n  {new_output}\n")
            print("  Changes made:")
            for c in changes:
                print(f"   → {c}")
            print()
 
            self.history.append({
                "version"   : i + 1,
                "output"    : output,
                "feedback"  : feedback,
                "improved_to": new_output,
                "changes"   : changes,
            })
 
            output = new_output
            time.sleep(0.3)
 
        return output
 

def collect_input() -> dict:
    print("\n")
    divider("═")
    print("  🤖  SELF-IMPROVING AGENT — Job Fit Recommender")
    divider("═")
    print("""
  This agent will:
    1. Generate an initial role recommendation
    2. Evaluate it against quality rules
    3. Improve it iteratively (up to 3 rounds)
    4. Show you exactly what changed and why
 
  Fill in the candidate details below.
""")
 
    
    print("  Enter candidate skills (comma-separated).")
    print("  Examples: Python, React, SQL, Docker, Machine Learning")
    raw_skills = input("  Skills: ").strip()
    skills = [s.strip() for s in raw_skills.split(",") if s.strip()] or ["Programming"]
 
    
    print("\n  Enter experience level.")
    print("  Examples: Fresher, 1-2 years, 3-5 years, Senior, 10+ years")
    experience = input("  Experience: ").strip() or "Fresher"
 
   
    print("\n  Enter the broad domain / department.")
    print("  Examples: Software, Data, DevOps, Mobile, Cloud")
    domain = input("  Domain (default: Software): ").strip() or "Software"
 
    return {
        "skills"    : skills,
        "experience": experience,
        "domain"    : domain,
    }
 
 

 
if __name__ == "__main__":
    input_data = collect_input()
 
    agent = SelfImprovingAgent()
    final = agent.run(input_data, iterations=3)
 
    section("FINAL OUTPUT")
    print(f"\n  {final}\n")
    divider("═")
 
    if agent.history:
        print(f"\n   Total iterations: {len(agent.history)}")
        print(f"   Versions stored in agent.history for audit.\n")
    else:
        print("\n  First output was already good — no iterations needed.\n")
 