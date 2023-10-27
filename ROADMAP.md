## Core
- [X] Make its mechanics work
- [X] Add fallbacks / error handling
- [X] Clean up the code
- [X] Clean up the terminal display
- [X] Solve for when a moment cannot be found from the action
- [X] Solve for when the action is nothing
- [X] Use match function to add forgiveness to user input
- [X] Remove unnecessary parts of speech from user input
- [X] Support multiple lines in narration moments
- [X] Refactor main implementation to make Wart an import, user uses their own project file
- [X] A function for choosing where and how to load content from, for project files
- [ ] A method for authors to provide a hook that override's error state (a hook named * means we override an error state with the moments tied to that hook
if choice from links fails, check the links for a hook that starts with '*', if exists, use that hook and try again), I just can't find a clean way to impliment this in the main loop.
- [X] Support 'nons' in the same files as story
- [ ] Cleaner, more readable refactor of the story formatting, mostly symbols
- [ ] Strengthen example content to ~100 lines and demonstrate the flexibility
- [ ] Documentation
