---
name: gmail
description: Interact with Gmail using the Gmail API. Use when sending emails, reading inbox, managing labels, searching messages, or automating email workflows. Requires OAuth2 authentication.
---

# Gmail Skill

This skill provides guidance for interacting with Gmail programmatically.

## When to Use

- Sending automated emails
- Reading inbox messages
- Managing labels and filters
- Searching email history
- Processing attachments
- Email automation workflows

## Authentication

### OAuth2 Setup
1. Go to Google Cloud Console
2. Enable Gmail API
3. Create OAuth2 credentials
4. Download client_secret.json

### Token Management
```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json', SCOPES)
creds = flow.run_local_server(port=0)
```

## Common Operations

### Send Email
```python
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

def send_email(service, to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    body = {'raw': raw}
    
    service.users().messages().send(userId='me', body=body).execute()
```

### Read Inbox
```python
def list_messages(service, query=''):
    results = service.users().messages().list(
        userId='me', q=query, maxResults=10).execute()
    return results.get('messages', [])

def get_message(service, msg_id):
    return service.users().messages().get(
        userId='me', id=msg_id).execute()
```

### Search Examples
```python
# Unread emails
query = 'is:unread'

# From specific sender
query = 'from:someone@example.com'

# With attachment
query = 'has:attachment'

# Specific label
query = 'label:important'

# Date range
query = 'after:2024/01/01 before:2024/12/31'
```

## Best Practices

1. **Rate limiting** - Don't exceed Gmail API quotas
2. **Batch operations** - Use batch requests for multiple actions
3. **Error handling** - Handle 401/403 errors gracefully
4. **Token refresh** - Automatically refresh expired tokens
5. **Privacy** - Don't log email content

## Tools

- **google-api-python-client** - Official Python client
- **gmail-api-wrapper** - Simplified wrapper
- **ezgmail** - Even simpler alternative

## Related Skills

- `api-gateway` - For webhook handling
- `code` - For automation scripts
