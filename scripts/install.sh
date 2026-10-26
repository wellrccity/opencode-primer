#!/usr/bin/env bash
#
# Installs the opencode-primer configuration into an OpenCode config directory.
#
# Target: OPENCODE_CONFIG_DIR when set, otherwise $HOME/.config/opencode.
# Existing files are skipped unless --force is given; --force backs up the
# whole target to <target>-backup-<yyyyMMdd-HHmmss> before overwriting.
# --dry-run prints the planned actions and writes nothing.
#
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/install.sh [--force] [--dry-run] [--help]

Install the opencode-primer configuration into an OpenCode config directory.

Target directory:
  OPENCODE_CONFIG_DIR when set, otherwise $HOME/.config/opencode

Options:
  --force     Back up the target to <target>-backup-<yyyyMMdd-HHmmss>, then
              overwrite existing files.
  --dry-run   Print the planned actions without writing anything.
  -h, --help  Show this help.
EOF
}

die() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

force=0
dry_run=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --force)
      force=1
      ;;
    --dry-run)
      dry_run=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'ERROR: unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 1
      ;;
  esac
  shift
done

script_dir=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
repo_root=$(dirname -- "$script_dir")

if [ -n "${OPENCODE_CONFIG_DIR:-}" ]; then
  target=$OPENCODE_CONFIG_DIR
elif [ -n "${HOME:-}" ]; then
  target=$HOME/.config/opencode
else
  die 'Cannot resolve the home directory. Set OPENCODE_CONFIG_DIR.'
fi

target=${target%/}
[ -n "$target" ] || die 'Resolved target directory is empty.'

# source|destination|kind
mappings=(
  'config/opencode.json|opencode.json|file'
  'config/cli.json|cli.json|file'
  'config/AGENTS.md|AGENTS.md|file'
  'agents|agents|dir'
  'commands|commands|dir'
  'skills|skills|dir'
  'plugins/meta-goal|plugins/meta-goal|dir'
)

item_src=()
item_dest=()

for entry in "${mappings[@]}"; do
  IFS='|' read -r src dest kind <<< "$entry"
  src_path=$repo_root/$src
  dest_root=$target/$dest

  if [ ! -e "$src_path" ]; then
    die "Missing source: $src"
  fi

  if [ "$kind" = 'file' ]; then
    item_src+=("$src_path")
    item_dest+=("$dest_root")
  else
    while IFS= read -r file; do
      rel=${file#"$src_path"/}
      item_src+=("$file")
      item_dest+=("$dest_root/$rel")
    done < <(find "$src_path" -type f -print | LC_ALL=C sort)
  fi
done

copy_src=()
copy_dest=()
skipped=0
i=0

while [ "$i" -lt "${#item_src[@]}" ]; do
  s=${item_src[$i]}
  d=${item_dest[$i]}
  if [ -e "$d" ] && [ "$force" -eq 0 ]; then
    printf 'SKIP   %s (already exists)\n' "$d"
    skipped=$((skipped + 1))
  else
    copy_src+=("$s")
    copy_dest+=("$d")
  fi
  i=$((i + 1))
done

printf 'Source: %s\n' "$repo_root"
printf 'Target: %s\n' "$target"
if [ "$dry_run" -eq 1 ]; then
  printf 'Mode:   dry run (nothing is written)\n'
elif [ "$force" -eq 1 ]; then
  printf 'Mode:   force (target is backed up, existing files overwritten)\n'
else
  printf 'Mode:   safe (existing files are skipped)\n'
fi
printf '\n'

backup=''
if [ "$force" -eq 1 ] && [ "${#copy_src[@]}" -gt 0 ] && [ -e "$target" ]; then
  backup="${target}-backup-$(date +%Y%m%d-%H%M%S)"
fi

if [ "$dry_run" -eq 1 ]; then
  if [ -n "$backup" ]; then
    printf 'WOULD BACKUP %s -> %s\n' "$target" "$backup"
  fi
  i=0
  while [ "$i" -lt "${#copy_src[@]}" ]; do
    printf 'WOULD COPY   %s -> %s\n' "${copy_src[$i]}" "${copy_dest[$i]}"
    i=$((i + 1))
  done
  printf '\nDry run complete: %s file(s) would be installed, %s skipped.\n' "${#copy_src[@]}" "$skipped"
  exit 0
fi

if [ -n "$backup" ]; then
  [ -e "$backup" ] && die "Backup path already exists: $backup"
  printf 'BACKUP %s -> %s\n' "$target" "$backup"
  cp -R -- "$target" "$backup"
fi

i=0
while [ "$i" -lt "${#copy_src[@]}" ]; do
  s=${copy_src[$i]}
  d=${copy_dest[$i]}
  mkdir -p -- "$(dirname -- "$d")"
  cp -- "$s" "$d"
  printf 'COPY   %s -> %s\n' "$s" "$d"
  i=$((i + 1))
done

printf '\nInstalled %s file(s) into %s, %s skipped.\n' "${#copy_src[@]}" "$target" "$skipped"
