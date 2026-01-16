# WhisperHedge UI

A comprehensive Reflex-based web interface for managing cryptocurrency API keys, liquidity positions, and hedging strategies with Supabase authentication.

## Features

- **User Authentication**: Secure sign up, login, and logout with Supabase
- **API Key Management**: Store and manage encrypted API keys for multiple exchanges (Hyperliquid, etc.)
- **Liquidity Position Tracking**: Monitor Uniswap V3 positions across multiple networks
- **Real-time Balance Monitoring**: Fetch and display account balances from exchanges
- **Blockchain Integration**: Direct blockchain queries for position data
- **Modern UI**: Built with Reflex and Tailwind CSS
- **Responsive Design**: Works on desktop and mobile

## Setup

1. **Install dependencies:**
   ```bash
   cd web_ui
   uv pip install -r requirements.txt
   ```

2. **Configure Supabase:**
   - Create a Supabase project at https://supabase.com
   - Run the SQL setup script: `cat ../SUPABASE_SETUP.sql` in Supabase SQL Editor
   - Copy `.env.example` to `.env`
   - Add your Supabase credentials:
     ```
     SUPABASE_URL=your_supabase_project_url
     SUPABASE_KEY=your_supabase_anon_key
     ENCRYPTION_KEY=generate_with_command_below
     ```
   - Generate encryption key with: `python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'`

3. **Run the app:**
   ```bash
   reflex run
   ```

## Pages

- `/` - Landing page with sign in/sign up options
- `/login` - User login page
- `/signup` - Create new account page
- `/dashboard` - Protected dashboard with multiple sections:
  - **Overview**: Account summary and metrics
  - **API Keys**: Manage exchange API credentials
  - **LP Positions**: Track liquidity positions
  - **Bot Status**: Monitor hedging bot status
  - **Settings**: Application configuration

## Project Structure

```
web_ui/
├── web_ui/
│   ├── pages/
│   │   ├── login.py           # Login page component
│   │   ├── signup.py          # Signup page component
│   │   └── dashboard.py       # Main dashboard page
│   ├── components/
│   │   ├── api_keys.py        # API key management components
│   │   ├── lp_positions.py    # LP position components
│   │   └── sidebar.py         # Navigation sidebar
│   ├── auth.py                # Supabase client configuration
│   ├── state.py               # Authentication state management
│   ├── api_key_state.py       # API key state management
│   ├── lp_position_state.py   # LP position state management
│   ├── crypto_utils.py        # Encryption utilities
│   ├── blockchain_utils.py   # Blockchain integration
│   ├── hl_utils.py           # Hyperliquid integration
│   ├── config.py             # Application configuration
│   └── web_ui.py             # Main app and routing
├── requirements.txt
├── rxconfig.py
├── .env.example
└── .gitignore
```

## Supported Networks

- Ethereum
- Arbitrum
- Base
- Polygon
- Optimism

## Security Features

- All API keys and secrets are encrypted at rest using Fernet encryption
- Supabase Row Level Security for user data isolation
- Environment-based configuration for sensitive data
- No hardcoded credentials in source code
