#!/bin/bash
set -e

echo "Updating API endpoints in frontend code..."
cd frontend/src

# Find all files with hardcoded localhost:5000 URLs and replace them
grep -r "http://localhost:5000" --include="*.jsx" --include="*.js" . | cut -d: -f1 | sort | uniq > /tmp/files_to_update.txt

if [ -s "/tmp/files_to_update.txt" ]; then
  echo "Found files with hardcoded API endpoints:"
  cat /tmp/files_to_update.txt

  # First, add the import statement where needed
  for file in $(cat /tmp/files_to_update.txt); do
    # Check if the import is already there
    if ! grep -q "import { apiUrl } from '@/lib/api-config'" "$file"; then
      # Find the last import line
      lastImport=$(grep -n "import" "$file" | tail -1 | cut -d: -f1)
      if [ ! -z "$lastImport" ]; then
        # Add our import after the last import
        sed -i "${lastImport}a import { apiUrl } from '@/lib/api-config';" "$file"
        echo "Added API config import to $file"
      fi
    fi
  done

  # Then replace all hardcoded URLs with apiUrl function calls
  for file in $(cat /tmp/files_to_update.txt); do
    # Use sed to replace hardcoded URLs
    sed -i 's|http://localhost:5000/api|apiUrl("/api"|g' "$file"
    # Fix the missing closing parenthesis
    sed -i 's|apiUrl("/api/\([^"]*\)")|apiUrl("/api/\1")|g' "$file"
    echo "Updated API endpoints in $file"
  done
else
  echo "No files with hardcoded API endpoints found."
fi

cd ../..
echo "API endpoint update complete!"
