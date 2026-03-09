#!/usr/bin/env python3

import os
from pathlib import Path
from ollama_wrapper import OllamaConnectionError, OllamaWrapper


class DeprecatedAnalyzer:
    """
    Analyse les logs de compilation pour détecter les warnings/erreurs
    de deprecation et génère un rapport Markdown structuré.
    """

    def __init__(
        self,
        arcade_dir: str = None,
        model: str = "qwen3:8b",
    ):
        base_dir = Path(os.path.dirname(os.path.abspath(__file__)))

        self.arcade_dir = Path(arcade_dir) if arcade_dir else (
            base_dir / ".." / ".." / "borne_arcade"
        ).resolve()

        self.log_path = self.arcade_dir / "logs" / "compilation.log"
        self.output_path = self.arcade_dir / "logs" / "deprecated.md"
        self.model = model
        self.client = OllamaWrapper()

    # ==========================================================
    # --------------------- IA SECTION -------------------------
    # ==========================================================

    def get_system_prompt(self) -> str:
        return """
        Tu es un analyste de code expert.

        Tu DOIS répondre STRICTEMENT selon le format suivant :

        1 PROBLÈME :
        Une seule phrase claire résumant le ou les problèmes détectés.
        Le fichier de warnings_errors est structuré de facon [NomDuJeu] Fichier:Ligne: warning: [deprecation] Description

        2 COMPILATIONS CONCERNÉES :
        Liste structurée sous cette forme :
        - Nom du jeu : 
        - NomFichier.java :
        - Ligne XX : description courte
        - Ligne XX : description courte

        3 SOLUTION :
        Explication claire et concise de la correction à apporter.

        4 EXEMPLE DE CORRECTION :
        Bloc de code AVANT puis bloc de code APRÈS.

        Tu ne dois rien ajouter en dehors de ces 4 sections.
        Réponse claire, structurée, sans texte inutile.
        """

    def build_prompt(self, log_content: str) -> str:
        return (
            "Donne moi quel compilation à un probleme et quel est le probleme "
            "suivant ce fichier de logs." + log_content
        )

    def call_llm(self, log_content: str) -> str:
        try:
            response = self.client.generate_text(
                model=self.model,
                prompt=self.build_prompt(log_content),
                system=self.get_system_prompt(),
            )
            return response.response

        except OllamaConnectionError as e:
            print("Erreur connexion Ollama :", e)
            return "LLM_ERROR"

        except Exception as e:
            print("Erreur inattendue lors de l'appel LLM :", e)
            return "LLM_ERROR"

    # ==========================================================
    # ----------------- ÉCRITURE RAPPORT -----------------------
    # ==========================================================

    def write_report(self, content: str):
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_path.write_text(content, encoding="utf-8")
        print(f"Rapport généré dans : {self.output_path}")

    def write_no_logs_report(self):
        content = (
            "# Rapport d'analyse\n\n"
            "**Statut** : Aucun fichier de logs disponible\n\n"
            f"Le fichier de logs attendu n'a pas été trouvé :\n`{self.log_path}`\n"
        )
        self.write_report(content)

    # ==========================================================
    # ----------------------- ENTRY ----------------------------
    # ==========================================================

    def run(self):
        if not self.log_path.exists():
            print(f"⚠️  Le fichier de logs n'existe pas : {self.log_path}")
            print("Aucune analyse à effectuer.")
            self.write_no_logs_report()
            return

        print("===== Analyse des deprecated =====")

        log_content = self.client.contenu_text(str(self.log_path))
        result = self.call_llm(log_content)

        if result == "LLM_ERROR":
            print("Analyse annulée (LLM indisponible).")
            return

        self.write_report(result)


# ==============================================================
# --------------------------- MAIN -----------------------------
# ==============================================================

if __name__ == "__main__":
    analyzer = DeprecatedAnalyzer()
    analyzer.run()