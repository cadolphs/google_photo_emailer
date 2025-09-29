# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Running tests
```bash
python -m pytest tests/
python -m pytest tests/test_app.py  # Run specific test file
python -m pytest tests/test_app.py::test_function_name  # Run specific test
```

### Running the application
```bash
# Send photos from a directory via email
python simple_script.py send-photos EMAIL_ADDRESS IMAGE_DIRECTORY

# Organize files into sub-folders by size limit (default 25MB per folder)
python simple_script.py chunk-files SOURCE_DIR OUTPUT_DIR [--max-size SIZE_MB]
```

### Installing dependencies
```bash
pip install -r requirements.txt
```

## Architecture

This codebase follows James Shore's "Testing Without Mocks" pattern with a focus on infrastructure wrappers and nullable versions for testing.

### Key Components

- **PhotoEmailer** (`photo_emailer/app.py`): Main application class that orchestrates the email sending workflow
- **Infrastructure Wrappers**: Thin wrappers around external dependencies (Google API, file system) located in `photo_emailer/infrastructure/`
  - Each infrastructure class has nullable versions for testing
  - Examples: `EmailSender`, `CredentialsIO`, `BrowserAuthentication`, `ImageLoader`, `Globber`
- **Logic Classes** (`photo_emailer/logic/`): Pure business logic without infrastructure dependencies
  - `Chunker`: Handles file chunking by size
  - `FileOrganizer`: Organizes files into folders
  - `Credentials`: Data class for credential management

### Testing Strategy

- Tests use nullable infrastructure to avoid external dependencies
- Infrastructure wrappers are test-driven with narrow integration tests
- Logic classes are pure and tested with unit tests
- The functional, class-less style is used for pytest tests (no test classes)

### Authentication Flow

The app uses Google OAuth2 for Gmail API access:
1. Loads stored credentials from `token.json`
2. Refreshes expired tokens automatically
3. Falls back to browser authentication if refresh fails
4. Stores updated credentials for future use