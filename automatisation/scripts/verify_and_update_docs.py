import subprocess
from pathlib import Path
from typing import Dict, Set
from ollama_wrapper import OllamaConnectionError, OllamaWrapper


SUPPORTED_EXTENSIONS = {".java", ".lua", ".py"}

LANGUAGE_MAP = {
    ".py": "python",
    ".java": "java",
    ".lua": "lua",
}

SYSTEM_PROMPTS = {
    "python": """
Tu es un expert Python. Tu reçois un fichier Python et tu dois y ajouter des docstrings Google Style complètes.

Règles STRICTES :
- Ajoute une docstring de module en haut du fichier si absente
- Ajoute des docstrings à chaque classe, méthode et fonction
- Les docstrings doivent être précises, en français, et décrire paramètres (Args:), retours (Returns:) et exceptions (Raises:) si applicable
- Tu peux ajouter des commentaires inline pour clarifier des sections complexes, mais privilégie les docstrings
- NE modifie PAS la logique du code, uniquement la documentation
- Renvoie UNIQUEMENT le fichier Python complet, sans aucun commentaire, sans balises markdown, sans explication
""",

    "java": """
Tu es un expert Java. Tu reçois un fichier Java et tu dois y ajouter des Javadocs complètes.

Règles STRICTES :
- Ajoute une Javadoc à chaque classe, interface, méthode et attribut public
- Utilise les tags @param, @return, @throws selon les cas
- Les commentaires doivent être précis, en français
- NE modifie PAS la logique du code, uniquement la documentation
- Renvoie UNIQUEMENT le fichier Java complet, sans aucun commentaire, sans balises markdown, sans explication
""",

    "lua": """
Tu es un expert Lua. Tu reçois un fichier Lua et tu dois y ajouter des commentaires de documentation LuaDoc complètes.

Règles STRICTES :
- Ajoute un bloc de commentaire de module en haut du fichier si absent
- Documente chaque fonction avec les tags LuaDoc : --- description, @param, @return
- Les commentaires doivent être précis, en français
- NE modifie PAS la logique du code, uniquement la documentation
- Renvoie UNIQUEMENT le fichier Lua complet, sans aucun commentaire, sans balises markdown, sans explication
""",
}


class DocsManager:
    """
    Gestionnaire d'audit et de mise à jour automatique de la documentation
    inline des fichiers source (.py, .java, .lua) dans borne_arcade/projet.

    Modes :
    - Normal : met à jour uniquement les fichiers des projets modifiés via git
    - Force : met à jour TOUS les fichiers éligibles en ignorant git
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
            "__pycache__", ".git", ".idea", ".vscode",
            "node_modules", ".mypy_cache", ".pytest_cache",
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

    def get_file_diff(self, file_path: Path) -> str:
        """
        Retourne le diff git pour un fichier spécifique.
        """
        if self.force_update:
            return "FORCED_UPDATE"

        try:
            diff = subprocess.check_output(
                ["git", "diff", "HEAD", "--", str(file_path)]
            ).decode()
            return diff
        except subprocess.CalledProcessError:
            return ""

    # ==========================================================
    # ---------------- ANALYSE FICHIER -------------------------
    # ==========================================================

    def collect_source_files(self, project_path: Path):
        """
        Génère tous les fichiers source supportés (.py, .java, .lua)
        dans un projet, en ignorant les patterns exclus.
        """
        for path in project_path.rglob("*"):
            if not path.is_file():
                continue

            relative = path.relative_to(project_path)
            parts = relative.parts

            if any(part in self.IGNORED_PATTERNS for part in parts):
                continue

            if path.suffix in SUPPORTED_EXTENSIONS:
                yield path

    # ==========================================================
    # --------------------- IA SECTION -------------------------
    # ==========================================================

    def get_system_prompt(self, lang: str) -> str:
        return SYSTEM_PROMPTS.get(lang, "")

    def build_prompt(self, file_path: Path, source_code: str) -> str:
        return f"""
        Fichier : {file_path.name}

        Voici le contenu du fichier :

        {source_code}
        """

    def call_llm(self, prompt: str, lang: str) -> str:
        try:
            response = self.client.generate_text(
                model=self.model,
                prompt=prompt,
                system=self.get_system_prompt(lang),
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

    def verify_and_update_file(self, file_path: Path):
        diff = self.get_file_diff(file_path)

        if not self.force_update and not diff.strip():
            print(f"  {file_path.name} : aucun changement détecté")
            return

        lang = LANGUAGE_MAP.get(file_path.suffix)
        if not lang:
            return

        source_code = file_path.read_text(encoding="utf-8")
        prompt = self.build_prompt(file_path, source_code)

        result = self.call_llm(prompt, lang)

        if result == "LLM_ERROR":
            print(f"  {file_path.name} : mise à jour annulée (LLM indisponible)")
            return

        print(f"  Mise à jour docs : {file_path.name}")
        result = self.strip_markdown_fences(result)
        file_path.write_text(result, encoding="utf-8")

    def process_project(self, project_path: Path):
        print(f"\nProjet : {project_path.name}")
        source_files = list(self.collect_source_files(project_path))

        if not source_files:
            print("  Aucun fichier source trouvé.")
            return

        for file_path in source_files:
            self.verify_and_update_file(file_path)
            
    def strip_markdown_fences(self, content: str) -> str:
        """Supprimer les ``` au début et a la fin si present dans le document.

        Args:
            content (str): Le fichier a verifier

        Returns:
            str: Le fichier nettoyer
        """
        lines = content.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        return "\n".join(lines)
    
    def update_file_doc(self, project_name: str, filename: str):
        """Met a jour un document spécifique

        Args:
            project_name (str): Le nom du projet
            filename (str): Le nom du fichier.
        """
        file_path = self.projects_dir / project_name / filename

        if not file_path.exists():
            print(f"Fichier introuvable : {file_path}")
            return

        if file_path.suffix not in SUPPORTED_EXTENSIONS:
            print(f"Extension non supportée : {file_path.suffix}")
            return

        self.verify_and_update_file(file_path)

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
                self.process_project(project)


# ==============================================================
# --------------------------- MAIN -----------------------------
# ==============================================================

if __name__ == "__main__":
    manager = DocsManager(force_update=False)
    manager.run()
    # manager.update_file_doc("ball-blast", "main.py")
