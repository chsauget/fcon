# Power BI Meets Agentic AI — édition Claude Code

Adaptation pour **Claude Code** de l'atelier FabCon Barcelona 2026 [RuiRomano/workshop-fabcon-26-bcn](https://github.com/RuiRomano/workshop-fabcon-26-bcn).

L'atelier d'origine utilise GitHub Copilot (CLI, VS Code et Copilot app). Ici, tout ce qui passe par Copilot est remplacé par Claude Code. Les objectifs, les prompts et les résultats attendus ne changent pas : on suit le même déroulé que les autres participants, avec un autre agent.

> [!NOTE]
> Les prompts sont en anglais, comme dans l'atelier d'origine, pour que les résultats restent comparables avec ceux de la salle. Les consignes sont en français.

## Ce qui change par rapport à l'original

| Original (GitHub Copilot) | Cette version (Claude Code) |
| --- | --- |
| `copilot plugin marketplace add` / `copilot plugin install` | `claude plugin marketplace add` / `claude plugin install` (même marketplace `microsoft/skills-for-fabric`) |
| Copilot Chat dans VS Code, Copilot app | `claude` dans un terminal, ou l'extension Claude Code pour VS Code |
| `AGENTS.md` | `CLAUDE.md`, qui importe `AGENTS.md` (`@AGENTS.md`) |
| Skill locale dans `.github/skills/` | Skill locale dans `.claude/skills/` |
| Modèles GPT-6 Sol / Luna | Opus / Sonnet / Haiku (`/model`) |
| Interactive / Allow all / Autopilot | Mode par défaut / *accept edits* / *auto mode* (`Shift+Tab`) |
| Plan mode de Copilot | Plan mode de Claude Code (`Shift+Tab`) |
| MCP distant ajouté via l'UI + OAuth | `.mcp.json` du projet, avec un jeton Azure CLI (`headersHelper`) |
| Sessions imbriquées (subagents) | Subagents Claude Code |
| Session insights | `/cost`, `/context` |

## Démarrer

1. Suivez les [prérequis](pre-requisites.md), en particulier la partie **Claude Code**.
2. Faites les labs dans l'ordre ou indépendamment.
3. En cas de problème, consultez [troubleshooting.md](troubleshooting.md).

## Labs

### [Lab 1 - Agentic Power BI on the Web](lab1/lab.md)

Copilot **intégré à Power BI** dans le navigateur (Web Modeling Copilot, Modeling Agent). Ce lab n'utilise pas GitHub Copilot et **n'est pas modifié** : il n'y a rien à remplacer par Claude Code.

### [Lab 2 - Personalized Power BI Agents](lab2/lab.md)

Plugin `powerbi-authoring` installé dans Claude Code, PBIP + Git, `CLAUDE.md`, skill locale, MCP local puis distant, plan mode et subagents.

### [Lab 3 - Build Data Apps with Fabric](lab3/lab.md)

Génération et itération d'une Fabric Data App avec Claude Code comme agent de développement.
