#!/bin/bash

harbor run -d terminal-bench/terminal-bench-2 -m anthropic/claude-sonnet-4-6 -a claude-code --include-task-name "terminal-bench/crack-7z-hash"
harbor run -d terminal-bench/terminal-bench-2 -m anthropic/claude-sonnet-4-6 -a claude-code --include-task-name "terminal-bench/filter-js-from-html"
harbor run -d terminal-bench/terminal-bench-2 -m anthropic/claude-sonnet-4-6 -a claude-code --include-task-name "terminal-bench/break-filter-js-from-html"
harbor run -d terminal-bench/terminal-bench-2 -m anthropic/claude-sonnet-4-6 -a claude-code --include-task-name "terminal-bench/fix-code-vulnerability"
