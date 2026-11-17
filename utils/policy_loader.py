import os

from config import POLICY_DIR


def load_policies():
    """
    Load all policy markdown files into memory.
    """

    policy_docs = {}

    files = [
        "grading_policy.md",
        "attendance_policy.md",
        "alert_rules.md",
        "progress_milestones.md",
        "faq.md"
    ]

    for file in files:

        path = os.path.join(POLICY_DIR, file)

        if not os.path.exists(path):
            raise FileNotFoundError(f"{file} not found in {POLICY_DIR}")

        with open(path, "r", encoding="utf-8") as f:
            policy_docs[file] = f.read()

        print(f"[OK] Loaded {file}")

    return policy_docs


if __name__ == "__main__":

    docs = load_policies()

    print("\n========== POLICY SUMMARY ==========\n")

    for name, text in docs.items():
        print(f"{name}")
        print(f"Characters : {len(text)}")
        print("-" * 40)