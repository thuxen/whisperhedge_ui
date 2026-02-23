# Webhooks (Coming Soon)

Receive real-time notifications via webhooks.

## Planned Events

### Position Events
- Position health change
- IL threshold exceeded
- Value change alert
- Fee milestone reached

### Account Events
- Plan limit warning
- Subscription change
- API key rotation reminder

## Webhook Format

```json
{
  "event": "position.health.critical",
  "timestamp": "2024-02-23T12:00:00Z",
  "data": {
    "position_id": "abc123",
    "health_score": 25,
    "il_percentage": -15.5
  }
}
```

## Security

- HMAC signature verification
- HTTPS only
- Retry logic
- Event deduplication

## Coming Soon

Full webhook documentation will be available with API launch.

[Express interest →](../troubleshooting/contact-support.md)
