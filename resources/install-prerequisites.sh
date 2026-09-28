#!/usr/bin/env bash
# Prerequisites check/install for Linux and macOS.
# Power BI Desktop is Windows-only and is not installed here.

set -u
failed=0

check() {
    local name="$1" cmd="$2" hint="$3"
    if command -v "$cmd" >/dev/null 2>&1; then
        printf '\033[32m%s: OK\033[0m\n' "$name"
    else
        printf '\033[31m%s: MISSING - %s\033[0m\n' "$name" "$hint"
        failed=$((failed + 1))
    fi
}

if ! command -v claude >/dev/null 2>&1; then
    curl -fsSL https://claude.ai/install.sh | bash
fi

check "Claude Code" claude "curl -fsSL https://claude.ai/install.sh | bash"
check "Git" git "install with your package manager (dnf/apt/brew install git)"
check "Node.js" node "https://nodejs.org/en/download/"
check "npm" npm "https://nodejs.org/en/download/"
check "Azure CLI" az "https://learn.microsoft.com/cli/azure/install-azure-cli-linux"
check "VS Code" code "https://code.visualstudio.com/download (optional)"

exit $((failed > 0))
