# Shared helpers for the scripts in this folder. Source it, don't run it.

# ./AI/Beginner 1 -> ai-beginner-1. Gives every challenge its own compose project, since
# many folders share a basename (Beginner, Advanced) and "Beginner 1" has a space in it.
project_name() {
  echo "${1#./}" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g'
}
