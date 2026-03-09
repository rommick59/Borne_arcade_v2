import subprocess
from pathlib import Path
from typing import Dict, Set
from ollama_wrapper import OllamaConnectionError, OllamaWrapper


DOCS_OUTPUT = "borne_arcade/docs/USER_GUIDE.md"


class UserDocManager:
    """
    Génère et met à jour une documentation utilisateur (non technique)
    pour la borne arcade à partir :
    - Des noms de projets et leurs README dans borne_arcade/projet/
    - Des scripts .sh dans borne_arcade/ (hors projet/)

    La régénération est intelligente : le fichier n'est recréé que si
    des fichiers sources ont été ajoutés ou supprimés via git.
    """

    def __init__(
        self,
        arcade_dir: str = "borne_arcade",
        model: str = "qwen3:8b",
        force_update: bool = False,
    ):
        self.arcade_dir = Path(arcade_dir)
        self.projects_dir = self.arcade_dir / "projet"
        self.docs_output = Path(DOCS_OUTPUT)
        self.model = model
        self.force_update = force_update
        self.client = OllamaWrapper()

    # ==========================================================
    # -------------------- GIT SECTION -------------------------
    # ==========================================================

    def get_changed_files(self) -> Dict[str, Set[str]]:
        """
        Retourne les fichiers ajoutés et supprimés dans borne_arcade/
        depuis HEAD, séparés par statut.

        Returns:
            Dict avec clés 'added' et 'deleted', chacune contenant
            un ensemble de chemins de fichiers modifiés.
        """
        result = {"added": set(), "deleted": set()}

        try:
            lines = subprocess.check_output(
                ["git", "diff", "--name-status", "HEAD"]
            ).decode().splitlines()
        except subprocess.CalledProcessError:
            print("Erreur lors de la récupération du git diff.")
            return result

        for line in lines:
            parts = line.split("\t", 1)
            if len(parts) != 2:
                continue

            status, filepath = parts[0].strip(), parts[1].strip()
            path = Path(filepath)

            if path.parts[0] != "borne_arcade":
                continue

            if status == "A":
                result["added"].add(filepath)
            elif status == "D":
                result["deleted"].add(filepath)

        return result

    def needs_update(self, changed: Dict[str, Set[str]]) -> bool:
        """
        Détermine si la doc utilisateur doit être régénérée.
        On régénère uniquement si un fichier pertinent (.sh ou README.md
        d'un projet) a été ajouté ou supprimé.

        Args:
            changed: Dictionnaire des fichiers ajoutés/supprimés.

        Returns:
            True si une régénération est nécessaire, False sinon.
        """
        all_changed = changed["added"] | changed["deleted"]

        for filepath in all_changed:
            path = Path(filepath)
            parts = path.parts

            # Nouveau projet ou projet supprimé (détecté via son README)
            if (
                len(parts) >= 3
                and parts[1] == "projet"
                and parts[2] == "README.md"
            ):
                return True

            # Script .sh ajouté ou supprimé à la racine de borne_arcade/
            if path.suffix == ".sh" and len(parts) == 2:
                return True

        return False

    # ==========================================================
    # ---------------- COLLECTE DES DONNÉES --------------------
    # ==========================================================

    def collect_projects(self) -> Dict[str, str]:
        """
        Collecte les noms de projets et le contenu de leur README.

        Returns:
            Dictionnaire {nom_projet: contenu_readme}.
        """
        projects = {}

        if not self.projects_dir.exists():
            return projects

        for project_path in sorted(self.projects_dir.iterdir()):
            if not project_path.is_dir():
                continue

            readme = project_path / "README.md"
            content = readme.read_text(encoding="utf-8") if readme.exists() else ""
            projects[project_path.name] = content

        return projects

    def collect_scripts(self) -> Dict[str, str]:
        """
        Collecte les scripts .sh à la racine de borne_arcade/ (hors projet/).

        Returns:
            Dictionnaire {nom_fichier: contenu_script}.
        """
        scripts = {}

        for path in sorted(self.arcade_dir.iterdir()):
            if path.is_file() and path.suffix == ".sh":
                scripts[path.name] = path.read_text(encoding="utf-8")

        return scripts

    def get_existing_doc(self) -> str:
        if self.docs_output.exists():
            return self.docs_output.read_text(encoding="utf-8")
        return ""

    # ==========================================================
    # --------------------- IA SECTION -------------------------
    # ==========================================================

    def get_system_prompt(self) -> str:
        return """
Tu es un rédacteur de documentation utilisateur pour une borne arcade.

Ton rôle est de produire un guide utilisateur clair, agréable et accessible.

Le document doit obligatoirement contenir :

L'URL du projet : https://github.com/rommick59/borne_arcade

Une explication claire indiquant qu'après récupération du projet, il suffit de lancer :
./automatisation/install.sh
et que cette action configure automatiquement la borne, installe tout le nécessaire et vérifie que tout est à jour.

Aucune précision sur des prérequis techniques (ne rien mentionner à ce sujet), car tout est géré automatiquement par la commande ci-dessus.

Règles STRICTES :

Écris en français, dans un langage simple et non technique.

Le lecteur est un utilisateur final, pas un développeur.

Structure le document avec des titres Markdown clairs (#, ##, ###).

Explique que lors de la première installation (après récupération du projet), il suffit de lancer ./automatisation/install.sh pour que tout soit configuré automatiquement.

Pour chaque jeu/projet : explique ce que c'est, comment y jouer, et les contrôles si mentionnés.

Lorsque tu parles de ./automatisation/install.sh, présente-le comme l'action à lancer pour “installer ou mettre à jour la borne”, sans utiliser les mots techniques comme script, dépôt, git, README, fichier, dépendances, etc.

Ne jamais utiliser de jargon technique (interdiction des mots : script, repository, git, README, fichier, dépendances, configuration système, etc.).

Le document doit être complet, structuré et agréable à lire.

Renvoie UNIQUEMENT le fichier Markdown complet, sans commentaire, sans balises de code, sans explication autour."""

    def build_prompt(
        self,
        projects: Dict[str, str],
        scripts: Dict[str, str],
        existing_doc: str,
        changed: Dict[str, Set[str]],
    ) -> str:
        projects_block = ""
        for name, readme in projects.items():
            projects_block += f"\n### {name}\n"
            projects_block += readme if readme else "_Aucune description disponible._"
            projects_block += "\n"

        scripts_block = ""
        for name, content in scripts.items():
            scripts_block += f"\n### {name}\n{content}\n"

        changes_block = ""
        if changed["added"]:
            changes_block += "Éléments ajoutés :\n" + "\n".join(changed["added"]) + "\n"
        if changed["deleted"]:
            changes_block += "Éléments supprimés :\n" + "\n".join(changed["deleted"]) + "\n"

        return f"""
CHANGEMENTS DÉTECTÉS :
{changes_block if changes_block else "Aucun (forçage manuel)"}

DOCUMENTATION EXISTANTE (à mettre à jour, ne pas réécrire ce qui n'a pas changé) :
{existing_doc if existing_doc else "Aucune documentation existante, génère le document complet."}

JEUX DISPONIBLES (nom + description README) :
{projects_block}

FONCTIONNALITÉS DE LA BORNE (contenu des scripts) :
{scripts_block}

Génère la documentation utilisateur complète et mise à jour.
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

    def run(self):
        if not self.arcade_dir.exists():
            print("Dossier borne_arcade introuvable.")
            return

        changed = {"added": set(), "deleted": set()}

        if self.force_update:
            print("MODE FORCE ACTIVÉ : régénération de la doc utilisateur")
        else:
            changed = self.get_changed_files()

            if not self.needs_update(changed):
                print("Aucun changement pertinent détecté. Doc utilisateur à jour.")
                return

            print("Changements détectés, régénération de la doc utilisateur...")

        projects = self.collect_projects()
        scripts = self.collect_scripts()
        existing_doc = self.get_existing_doc()

        prompt = self.build_prompt(projects, scripts, existing_doc, changed)
        result = self.call_llm(prompt)

        if result == "LLM_ERROR":
            print("Génération annulée (LLM indisponible).")
            return

        self.docs_output.parent.mkdir(parents=True, exist_ok=True)
        self.docs_output.write_text(result, encoding="utf-8")
        print(f"Doc utilisateur mise à jour : {self.docs_output}")


# ==============================================================
# --------------------------- MAIN -----------------------------
# ==============================================================

if __name__ == "__main__":
    manager = UserDocManager(force_update=True)
    manager.run()