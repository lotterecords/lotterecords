import subprocess
from datetime import datetime
import os

# Config
repo_path = "/home/nickdelc/lotterecords"  # adjust if your git repo is elsewhere
log_file = os.path.join(repo_path, "daily_neologisms.txt")
model_path = "../models/tinyllama-1.1b-chat.q4_K_M.gguf"
build_path = os.path.join(repo_path, "build")

# Read neologism
with open("/home/nickdelc/lotterecords/neologism.txt", "r") as f:
    word = f.read().strip()

# Build llama-run command (as raw args)
prompt = [
    "Break", "down", "the", "neologism", word + ":",
    "provide", "etymology", "(breaking", "down", "all", "parts", "of", "the", "word,", "not", "only", "the", "root),",
    "part", "of", "speech,", "definition,", "and", "an", "example", "sentence."
]
command = ["./bin/llama-run", "--ngl", "999", model_path] + prompt

# Run inference
result = subprocess.run(command, cwd=build_path, capture_output=True, text=True)

# Format output with timestamp
timestamp = datetime.now().strftime("%Y-%m-%d")
entry = f"\n[{timestamp}] {word.upper()}\n{result.stdout.strip()}\n"

# Append to log file
with open(log_file, "a") as f:
    f.write(entry)

# Git add/commit/push
subprocess.run(["git", "add", "daily_neologisms.txt"], cwd=repo_path)
subprocess.run(["git", "commit", "-m", f"Add definition for {word} ({timestamp})"], cwd=repo_path)
subprocess.run(["git", "push"], cwd=repo_path)

print(f"Definition for '{word}' appended and pushed to GitHub.")
