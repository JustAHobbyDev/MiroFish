#!/usr/bin/env bash

set -euo pipefail

REMOTE="${REMOTE:-upstream}"
UPSTREAM_BRANCH="${UPSTREAM_BRANCH:-main}"
MODE="${1:-status}"

usage() {
  cat <<'EOF'
Usage:
  ./scripts/sync-upstream.sh            # fetch upstream and show sync status
  ./scripts/sync-upstream.sh status     # same as default
  ./scripts/sync-upstream.sh ff         # fast-forward current branch to upstream/main

Environment overrides:
  REMOTE=upstream
  UPSTREAM_BRANCH=main
EOF
}

require_git_repo() {
  git rev-parse --is-inside-work-tree >/dev/null 2>&1 || {
    echo "Not inside a git repository." >&2
    exit 1
  }
}

require_remote() {
  git remote get-url "$REMOTE" >/dev/null 2>&1 || {
    echo "Remote '$REMOTE' is not configured." >&2
    exit 1
  }
}

current_branch() {
  git branch --show-current
}

fetch_upstream() {
  git fetch "$REMOTE"
}

print_status() {
  local branch ref counts ahead behind head_sha upstream_sha
  branch="$(current_branch)"
  ref="$REMOTE/$UPSTREAM_BRANCH"
  counts="$(git rev-list --left-right --count "HEAD...$ref")"
  ahead="$(printf '%s' "$counts" | awk '{print $1}')"
  behind="$(printf '%s' "$counts" | awk '{print $2}')"
  head_sha="$(git rev-parse --short HEAD)"
  upstream_sha="$(git rev-parse --short "$ref")"

  echo "Current branch: $branch"
  echo "Tracking against: $ref"
  echo "HEAD: $head_sha"
  echo "$ref: $upstream_sha"
  echo "Ahead: $ahead"
  echo "Behind: $behind"

  if [[ "$ahead" == "0" && "$behind" == "0" ]]; then
    echo "Status: in sync"
  elif [[ "$ahead" == "0" ]]; then
    echo "Status: behind upstream"
    echo "Next step: ./scripts/sync-upstream.sh ff"
  elif [[ "$behind" == "0" ]]; then
    echo "Status: ahead of upstream"
    echo "Next step: push or keep working"
  else
    echo "Status: diverged"
    echo "Next step: merge or rebase upstream manually"
    echo "  git merge $ref"
    echo "  or"
    echo "  git rebase $ref"
  fi
}

fast_forward() {
  local ref branch counts ahead behind dirty
  branch="$(current_branch)"
  ref="$REMOTE/$UPSTREAM_BRANCH"
  counts="$(git rev-list --left-right --count "HEAD...$ref")"
  ahead="$(printf '%s' "$counts" | awk '{print $1}')"
  behind="$(printf '%s' "$counts" | awk '{print $2}')"
  dirty="$(git status --porcelain)"

  if [[ -n "$dirty" ]]; then
    echo "Refusing fast-forward with uncommitted changes." >&2
    echo "Commit or stash your work first." >&2
    exit 1
  fi

  if [[ "$behind" == "0" ]]; then
    echo "Nothing to fast-forward. Branch '$branch' is not behind $ref."
    return
  fi

  if [[ "$ahead" != "0" ]]; then
    echo "Cannot fast-forward because '$branch' has local commits not in $ref." >&2
    echo "Use a merge or rebase instead." >&2
    exit 1
  fi

  git merge --ff-only "$ref"
  print_status
}

main() {
  require_git_repo
  require_remote

  case "$MODE" in
    status)
      fetch_upstream
      print_status
      ;;
    ff)
      fetch_upstream
      fast_forward
      ;;
    -h|--help|help)
      usage
      ;;
    *)
      echo "Unknown mode: $MODE" >&2
      usage >&2
      exit 1
      ;;
  esac
}

main
