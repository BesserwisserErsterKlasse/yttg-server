# yttg-server

## Prerequisites

- [Python](https://www.python.org/) 3.14 or newer

## Installation

First, clone the repo to the target machine

```shell
git clone https://github.com/BesserwisserErsterKlasse/yttg-server
```

Change into the project directory

```shell
cd yttg-server
```

Create a virtual environment

```shell
python3.14 -m venv .venv
```

And activate it

- On Linux / macOS

```shell
source .venv/bin/activate
```

- On Windows (PowerShell)

```shell
.venv\Scripts\Activate.ps1
```

Install the dependencies

```shell
pip install -e ".[optimize]"
```

**Note:** `[optimize]` is an optional dependency — you can omit it and run `pip install -e .`

## Run

### Environment Variables

Create `.env` file in the project's root and define 3 environment variables

```env
TELEGRAM__API_ID="your-telegram-app-id"
TELEGRAM__API_HASH="your-telegram-app-hash"
CRYPTO__PRE_SHARED_SECRET="your-random-shared-secret"
```

- `TELEGRAM__API_ID` and `TELEGRAM__API_HASH` are required to authenticate with Telegram
- `CRYPTO__PRE_SHARED_SECRET` is a shared secret used internally by the service

### Create a Telegram App

`yttg-server` relies on Pyrogram, and to use Pyrogram, you have to register a Telegram application:

1. Go to the [official Telegram website](https://my.telegram.org)
2. Log in with your Telegram account
3. Navigate to **API Development Tools**
4. Create a new application if you don't have one

After creation, you will receive:

- **API ID:** An integer roughly 10 digits long
- **API HASH:** A hexadecimal string 32 characters long

Use these values in your `.env` file

### Generate a Pre-Shared Secret

The value of `CRYPTO__PRE_SHARED_SECRET` should be a securely generated random string. It is used as a pre-shared secret for cryptographic operations.

For example, you can use this command to generate it

```shell
openssl rand -hex 32
```

**Important:** The exact same secret must be configured on both the client and the server.

Run the `main.py` file

```shell
python -O src/main.py
```

**Note:** `-O` is an optional flag that removes unnecessary `assert`s — you can omit it and run `python src/main.py`

On first startup, `yttg-server` will prompt you to authorize via QR code and enter your cloud password if you have 2FA enabled

**Note:** A session file will be created locally to persist authentication

## Configuration

### Cryptographic Standard

Select the cryptographic standardused to establish a secure TCP connection via the `CRYPTO__ML_KEM` environment variable

```env
CRYPTO__ML_KEM="512"
```

Supported values are `512` *(default)*, `768` and `1024`

## License

yttg-server is a free, open-source software distributed under the [AGPLv3 License](LICENSE.txt)
