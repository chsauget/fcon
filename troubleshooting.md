# Dépannage — édition Claude Code

### L'authentification utilise le mauvais compte Fabric

Le navigateur peut réutiliser une session professionnelle existante sans vous proposer de choisir le compte.

**Solution**

1. Ouvrez une fenêtre de navigation privée, ou un profil de navigateur dédié à l'atelier, et gardez-la ouverte toute la journée.
2. Quand `az login` ouvre une page dans le navigateur par défaut, copiez l'URL et ouvrez-la dans la fenêtre privée.
3. Connectez-vous avec le compte Fabric de l'atelier.
4. Vérifiez avec `az account show`.

### `az login` affiche « No subscriptions found »

C'est normal avec le compte Fabric de l'atelier : il n'a pas d'abonnement Azure. `az login` échoue alors, et `az account show` répond `Please run 'az login' to setup account`.

**Solution**

```bash
az login --tenant 64a5d9e8-a2d2-4914-bba4-4840b3732a7c --allow-no-subscriptions
az account get-access-token --resource https://api.fabric.microsoft.com --query expiresOn -o tsv
```

(`64a5d9e8-…` est le tenant *FabCon/SQLCon 2026 - Barcelona*. Il s'affiche aussi dans le message d'erreur de `az login`.)

Sous Linux avec Wayland, des lignes `ERROR: ... GtkSettings` ou `ozone-platform=wayland` peuvent apparaître à l'ouverture du navigateur. Elles sont sans conséquence.

### `claude: command not found` / `az: command not found`

- `claude` : seule l'extension VS Code est installée, et son binaire n'est pas dans le `PATH`. Installez la CLI :
  - Linux / macOS : `curl -fsSL https://claude.ai/install.sh | bash`
  - Windows : `irm https://claude.ai/install.ps1 | iex`
- `az` : Azure CLI n'est pas installé.
  - Fedora : `sudo dnf install azure-cli`
  - Windows : `winget install Microsoft.AzureCLI`

### Le MCP Power BI (local ou distant) n'apparaît pas ou échoue

1. Dans Claude Code, tapez `/mcp` pour voir l'état de chaque serveur.
2. Hors session, `claude mcp list` donne la même information.
3. Serveur **distant** en échec : vérifiez qu'`az account get-access-token --resource https://api.fabric.microsoft.com` renvoie bien un jeton. Le `headersHelper` du `.mcp.json` réutilise simplement la session Azure CLI.
4. Serveur **local** (`powerbi-modeling-mcp` du plugin) en échec : vérifiez que Node.js et `npx` sont dans le `PATH`, puis relancez `claude`.
5. Après une installation ou une mise à jour du plugin, **redémarrez** `claude`. Les serveurs MCP sont chargés au démarrage.

> [!NOTE]
> Le problème OAuth de l'atelier d'origine (`COPILOT_ENTRA_DISABLE_ONEAUTH`) ne concerne que GitHub Copilot. Claude Code s'appuie sur le jeton Azure CLI, donc c'est bien le compte de `az login` qui est utilisé.

### Claude ne trouve pas les skills du plugin

```bash
claude plugin marketplace update fabric-collection
claude plugin install powerbi-authoring@fabric-collection
```

Relancez `claude`. Dans une session, `/plugin` affiche les plugins installés.

### Le serveur `.mcp.json` du projet n'est pas chargé

Claude Code demande d'approuver les serveurs MCP déclarés dans le `.mcp.json` d'un projet au premier lancement. Si vous avez refusé, lancez `claude mcp reset-project-choices` depuis le dossier, puis relancez `claude`.
