#!/usr/bin/env python3
import sys

force = "--force" in sys.argv or "-f" in sys.argv

# Verifier les deprecated warnings et erreurs dans les logs de compilation, et generer un rapport structuré en markdown
from verif_deprecated import DeprecatedAnalyzer
DeprecatedAnalyzer().run()

# Verifier et mettre à jour les README des projets dans borne_arcade/projet
from verify_and_update_readme import ReadmeManager
ReadmeManager(force_update=force).run()

# Verifier et mettre à jour les docstrings des fichiers sources de chaque projet
from verify_and_update_docs import DocsManager
DocsManager(force_update=force).run()

# Generer et mettre à jour la documentation utilisateur globale de la borne arcade
from verify_and_update_doc_user import UserDocManager
UserDocManager(force_update=force).run()