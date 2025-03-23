# Instagram Follower Analyzer

This Python application analyzes an Instagram profile to find users that are not following back. It shows you a list of accounts that you follow but don't follow you back.

## Requirements

- Python 3.7 or higher
- `instaloader` package

## Installation

1. Clone this repository or download the files
2. Install the required package:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
```bash
python instagram_analyzer.py
```

2. Follow the prompts:
   - Enter the Instagram username you want to analyze
   - Specify if the account is private
   - If the account is private, you'll need to provide your Instagram login credentials

## Features

- Works with both public and private Instagram accounts
- Secure password input (hidden while typing)
- Sorted list of users who don't follow back
- Error handling for various scenarios (invalid credentials, non-existent profiles, etc.)

## Notes

- For private accounts, you need to have an Instagram account and be following the target account
- The script may take some time to run depending on the number of followers/following
- Instagram may temporarily limit requests if you analyze too many accounts in a short time
- Your login credentials are only used for authentication and are not stored anywhere

## Privacy & Security

- Your Instagram password is never stored or logged
- The script uses the official Instagram API through the `instaloader` library
- All data processing is done locally on your machine 