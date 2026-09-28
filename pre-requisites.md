# Prérequis — édition Claude Code

## Connaissances

Une pratique concrète de Power BI suffit : connexion aux données, création d'un rapport, tables, relations, mesures et DAX. Aucune connaissance préalable de l'agentique, de Claude Code ou de MCP n'est nécessaire.

## Poste de travail

| Lab | Windows | Linux / macOS |
| --- | --- | --- |
| Lab 1 (navigateur) | ✅ | ✅ |
| Lab 2 — Partie 1 (PBIP + Power BI Desktop) | ✅ | ❌ Power BI Desktop n'existe que sous Windows. Utilisez une VM Windows ou un autre poste. |
| Lab 2 — Partie 2 (Fabric + MCP distant) | ✅ | ✅ |
| Lab 3 (Fabric Data Apps) | ✅ | ✅ Remplacez les commandes PowerShell par leur équivalent bash |

## Logiciels

| Outil | Windows | Linux / macOS |
| --- | --- | --- |
| [Claude Code](https://code.claude.com/docs/en/setup) | `irm https://claude.ai/install.ps1 \| iex` | `curl -fsSL https://claude.ai/install.sh \| bash` |
| [Power BI Desktop (août 2026 ou plus récent)](https://pbi.onl/download) | winget `Microsoft.PowerBI` | — |
| [Git](https://git-scm.com/) | [Git for Windows](https://gitforwindows.org/) (Claude Code l'utilise aussi sous Windows) | gestionnaire de paquets |
| [Node.js et npm](https://nodejs.org/en/download/) | winget `OpenJS.NodeJS.LTS` | gestionnaire de paquets / nvm |
| [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) | winget `Microsoft.AzureCLI` | Fedora : `sudo dnf install azure-cli` · autres : [guide Linux](https://learn.microsoft.com/cli/azure/install-azure-cli-linux) |
| [Visual Studio Code](https://code.visualstudio.com/download) (facultatif) | winget `Microsoft.VisualStudioCode` | paquet officiel |

GitHub Copilot CLI et la GitHub Copilot app ne sont **pas** nécessaires.

### Installation automatique

- **Windows** : [resources/install-prerequisites.ps1](resources/install-prerequisites.ps1)

  ```powershell
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\resources\install-prerequisites.ps1
  ```

- **Linux / macOS** : [resources/install-prerequisites.sh](resources/install-prerequisites.sh). Il installe Claude Code et vérifie que les autres outils sont présents.

  ```bash
  ./resources/install-prerequisites.sh
  ```

> [!TIP]
> Des erreurs pour des logiciels déjà installés peuvent apparaître. Vous pouvez les ignorer si l'outil est bien présent et à jour.

> [!IMPORTANT]
> **Extension VS Code seule ≠ CLI.** L'extension Claude Code pour VS Code embarque son propre binaire, qui n'est pas ajouté au `PATH`. Le lab utilise des commandes `claude …` dans le terminal. Sans CLI installée, vous obtenez `claude: command not found`. Installez-la avec le script ci-dessus (elle va dans `~/.local/bin`). Dépannage : binaire de l'extension dans `~/.vscode/extensions/anthropic.claude-code-*/resources/native-binary/claude`.

## Compte Claude

Il faut un accès à Claude Code : abonnement Claude Pro, Max, Team ou Enterprise, ou une clé API Anthropic Console.

1. Lancez `claude` dans un terminal.
2. Suivez la connexion dans le navigateur.
3. Vérifiez avec `/status`.

> [!NOTE]
> La licence GitHub Copilot fournie par l'atelier ne sert pas dans cette version. Vous n'avez pas besoin de rejoindre l'organisation GitHub de l'atelier. Le compte **Fabric** fourni reste nécessaire.

## Compte et tenant Fabric

Le compte Fabric est fourni le jour de l'atelier. Si vous utilisez votre propre tenant, activez ces paramètres :

- **Users can use the Power BI Model Context Protocol server endpoint**
- **Allow XMLA endpoints and Analyze in Excel with on-premises semantic models**
- **Enable Fabric App Items**

> [!IMPORTANT]
> Le compte Fabric de l'atelier est valable le jour même et supprimé quelques jours après.

## Vérification rapide

```bash
claude --version
git --version
node --version
az --version
```
