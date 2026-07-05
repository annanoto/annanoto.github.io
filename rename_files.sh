#!/bin/bash
# Run this from the root of your annanoto.github.io repo folder.
# It renames every file with spaces/parentheses to a safe name,
# uses `git mv` so GitHub sees it as a rename (keeps history),
# and updates every reference to the old name inside index.html.

set -e

HTML_FILE="index.html"

if [ ! -f "$HTML_FILE" ]; then
  echo "Run this script from the folder containing $HTML_FILE"
  exit 1
fi

# Find every file (not directory) whose name has a space, (), or other unsafe char
find . -maxdepth 1 -type f | while read -r filepath; do
  filename=$(basename "$filepath")

  # skip the script itself and the html file
  if [ "$filename" == "$(basename "$0")" ] || [ "$filename" == "$HTML_FILE" ]; then
    continue
  fi

  # build a safe version: spaces -> underscores, remove ()
  safe=$(echo "$filename" | sed -E 's/[[:space:]]+/_/g; s/[()]//g')

  if [ "$filename" != "$safe" ]; then
    echo "Renaming: '$filename' -> '$safe'"
    git mv -- "$filename" "$safe"

    # Escape special regex chars in the old filename for sed
    escaped_old=$(printf '%s\n' "$filename" | sed 's/[.[\*^$/]/\\&/g')

    # Replace every occurrence of the old filename in index.html with the new one
    sed -i.bak "s/${escaped_old}/${safe}/g" "$HTML_FILE"
  fi
done

rm -f "${HTML_FILE}.bak"
echo ""
echo "Done. Review 'git status' and 'git diff $HTML_FILE', then commit and push."
