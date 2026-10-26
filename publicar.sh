#!/usr/bin/env bash
# Envia o master local (e as tags) para o main do GitHub com a conta turing-lucas.
# Faz o login na primeira vez (abre o navegador) e no fim volta para a conta que estava ativa antes.
set -euo pipefail
cd "$(dirname "$0")"

CONTA=turing-lucas
REPO=https://github.com/turing-lucas/mud-valinor-client-beta.git

# o repositório é público: nenhuma senha do .credenciais pode estar em algum commit
if [ -f .credenciais ]; then
  if sed -n 's/^Senha[A-Za-z]*: //p' .credenciais | grep -v '^$' > /dev/null &&
     git grep -qF -f <(sed -n 's/^Senha[A-Za-z]*: //p' .credenciais | grep -v '^$') $(git rev-list master) -- .; then
    echo "ERRO: há senha do .credenciais no histórico; nada foi enviado." >&2
    exit 1
  fi
fi

ANTES=$(gh api user --jq .login 2>/dev/null || true)
if ! gh auth status --hostname github.com 2>/dev/null | grep -q "account $CONTA "; then
  echo "Login no GitHub como $CONTA (abre o navegador)..."
  gh auth login --hostname github.com --git-protocol https --web
fi
gh auth switch --hostname github.com --user "$CONTA"
if [ -n "$ANTES" ] && [ "$ANTES" != "$CONTA" ]; then
  trap 'gh auth switch --hostname github.com --user "$ANTES" && echo "Conta ativa de volta: $ANTES"' EXIT
fi
gh auth setup-git --hostname github.com

git remote get-url origin > /dev/null 2>&1 || git remote add origin "$REPO"
git push -u origin master:main
git push origin --tags  # uma tag v* nova dispara os binários e a Release
echo "Publicado: ${REPO%.git}"
