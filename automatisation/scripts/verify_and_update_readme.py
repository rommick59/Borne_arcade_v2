import subprocess
from pathlib import Path
from typing import Dict, Set
from ollama_wrapper import OllamaConnectionError, OllamaWrapper


class ReadmeManager:
    """
    Gestionnaire d'audit et de mise à jour automatique des documentations
    des projets dans borne_arcade/projet.

    Modes :
    - Normal : met à jour uniquement les projets modifiés via git
    - Force : met à jour TOUS les projets en ignorant git
    """

    def __init__(
        self,
        projects_dir: str = "borne_arcade/projet",
        model: str = "qwen3:8b",
        force_update: bool = False,
    ):
        self.projects_dir = Path(projects_dir)
        self.model = model
        self.force_update = force_update
        self.client = OllamaWrapper()
        
        self.IGNORED_PATTERNS = {
        # Dossiers
        "__pycache__", ".git", ".idea", ".vscode",
        "node_modules", ".mypy_cache", ".pytest_cache",
        # Extensions
        ".pyc", ".pyo", ".pyd", ".egg-info",
        ".DS_Store", ".env",
        }

    # ==========================================================
    # -------------------- GIT SECTION -------------------------
    # ==========================================================

    def get_changed_projects(self) -> Set[str]:
        """
        Retourne les noms des projets modifiés depuis HEAD.
        """
        try:
            diff_files = subprocess.check_output(
                ["git", "diff", "--name-only", "HEAD"]
            ).decode().splitlines()
        except subprocess.CalledProcessError:
            print("Erreur lors de la récupération du git diff.")
            return set()

        changed_projects = set()

        for file in diff_files:
            parts = Path(file).parts
            if (
                len(parts) >= 3
                and parts[0] == "borne_arcade"
                and parts[1] == "projet"
            ):
                changed_projects.add(parts[2])

        return changed_projects

    def get_project_diff(self, project_name: str) -> str:
        """
        Retourne le diff git uniquement pour un projet spécifique.
        """
        if self.force_update:
            return "FORCED_UPDATE"

        try:
            diff = subprocess.check_output(
                [
                    "git",
                    "diff",
                    "HEAD",
                    "--",
                    f"{self.projects_dir}/{project_name}",
                ]
            ).decode()
            return diff
        except subprocess.CalledProcessError:
            return ""

    # ==========================================================
    # ---------------- ANALYSE PROJET --------------------------
    # ==========================================================

    def get_structure(self, project_path: Path) -> str:
        structure = []

        for path in project_path.rglob("*"):
            relative = path.relative_to(project_path)
            parts = relative.parts

            if any(part in self.IGNORED_PATTERNS for part in parts):
                continue

            if path.suffix in self.IGNORED_PATTERNS:
                continue

            structure.append(str(relative))

        return "\n".join(sorted(structure))

    def get_doc_content(self, project_path: Path) -> str:
        readme = project_path / "README.md"
        if readme.exists():
            return readme.read_text(encoding="utf-8")
        return ""

    def analyze_project(self, project_path: Path) -> Dict:
        return {
            "name": project_path.name,
            "structure": self.get_structure(project_path),
            "doc_content": self.get_doc_content(project_path),
        }

    # ==========================================================
    # --------------------- IA SECTION -------------------------
    # ==========================================================

    def build_prompt(self, data: Dict, diff: str) -> str:
        return f"""
        PROJET : {data['name']}

        MODE FORCE : {"OUI" if self.force_update else "NON"}

        CHANGEMENTS RECENTS :
        {diff}

        STRUCTURE :
        {data['structure']}

        DOCUMENTATION ACTUELLE :
        {data['doc_content']}
        """

    def get_system_prompt(self) -> str:
        return """
        Tu es un auditeur technique STRICT et exigeant.

        Une documentation est considérée VALIDE UNIQUEMENT si :

        1) Elle est écrite en français impeccable
        2) Elle suit EXACTEMENT la structure obligatoire
        3) Chaque section contient un contenu précis et exploitable
        4) Elle correspond réellement à la structure du projet fournie
        5) Elle n'est ni vague, ni minimale, ni marketing
        6) Les sections ne sont pas vides

        Si la documentation respecte STRICTEMENT tous les critères :
        Réponds uniquement :
        DOC_OK

        Sinon :
        Renvoie uniquement la documentation complète en Markdown.
        Aucun commentaire supplémentaire.
        """

    def call_llm(self, prompt: str) -> str:
        try:
            response = self.client.generate_text(
                model=self.model,
                prompt=prompt,
                system=self.get_system_prompt(),
            )
            return response.response.strip()

        except OllamaConnectionError as e:
            print("Erreur connexion Ollama :", e)
            return "LLM_ERROR"

        except Exception as e:
            print("Erreur inattendue lors de l'appel LLM :", e)
            return "LLM_ERROR"


    # ==========================================================
    # --------------------- CORE LOGIC -------------------------
    # ==========================================================

    def verify_and_update(self, project_path: Path):
        project_name = project_path.name

        diff = self.get_project_diff(project_name)

        if not self.force_update and not diff.strip():
            print(f"{project_name} : aucun changement détecté")
            return

        data = self.analyze_project(project_path)
        prompt = self.build_prompt(data, diff)

        result = self.call_llm(prompt)

        if result == "LLM_ERROR":
            print(f"{project_name} : mise à jour annulée (LLM indisponible)")
            return

        if result == "DOC_OK":
            print(f"{project_name} : documentation OK")
        else:
            print(f"Mise à jour doc : {project_name}")
            readme_path = project_path / "README.md"
            readme_path.write_text(result, encoding="utf-8")
            
    

    # ==========================================================
    # ----------------------- ENTRY ----------------------------
    # ==========================================================

    def run(self):
        if not self.projects_dir.exists():
            print("Dossier projets introuvable.")
            return

        if self.force_update:
            print("MODE FORCE ACTIVÉ : mise à jour de tous les projets")
            projects_to_process = {
                p.name for p in self.projects_dir.iterdir() if p.is_dir()
            }
        else:
            projects_to_process = self.get_changed_projects()

            if not projects_to_process:
                print("Aucun projet modifié.")
                return

        for project in self.projects_dir.iterdir():
            if project.is_dir() and project.name in projects_to_process:
                self.verify_and_update(project)


# ==============================================================
# --------------------------- MAIN -----------------------------
# ==============================================================

if __name__ == "__main__":
    manager = ReadmeManager(force_update=False)
    manager.run()
