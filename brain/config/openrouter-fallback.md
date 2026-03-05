# OPENROUTER FALLBACK CONFIGURATION

**Date:** 2026-03-05  
**Status:** ✅ ACTIVE  
**Purpose:** Avoid rate limits by using OpenRouter as fallback

---

## 🔑 API Configuration

```bash
# Set in OpenClaw config
openclaw config set env.OPENROUTER_API_KEY "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"
```

**Key:** `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`

---

## 🔄 Fallback Strategy

### Primary Model
- **Provider:** kimi-coding/k2p5
- **Use for:** Normal operations, coding tasks

### Fallback Chain
1. **kimi-coding/k2p5** (primary)
2. **openrouter/gpt-4o** (if kimi fails)
3. **openrouter/claude-3-opus** (if gpt-4o fails)
4. **openrouter/mistral-large** (final fallback)

---

## 📋 Usage

### Automatic Fallback
```javascript
// In any script, use:
const response = await fetchWithFallback({
  primary: 'kimi-coding/k2p5',
  fallback: ['openrouter/gpt-4o', 'openrouter/claude-3-opus'],
  prompt: 'Your prompt here'
});
```

### Manual OpenRouter Usage
```bash
# Direct API call
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-4o",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

## 🛡️ Rate Limit Handling

### Detection
- Monitor response headers for `x-ratelimit-*`
- Track request count per minute
- Log rate limit errors

### Response
1. **Immediate:** Switch to fallback model
2. **Short-term:** Reduce request frequency
3. **Long-term:** Implement caching

### Recovery
- Auto-retry after rate limit reset
- Exponential backoff
- Queue requests if needed

---

## 📊 Monitoring

### Metrics to Track
- Requests per minute per model
- Rate limit hits
- Fallback usage frequency
- Response times
- Error rates

### Alerts
- High rate limit usage
- Multiple fallback switches
- Sustained errors

---

## 📝 Implementation Notes

### Session Configuration
```json
{
  "models": {
    "primary": "kimi-coding/k2p5",
    "fallback": ["openrouter/gpt-4o", "openrouter/claude-3-opus"]
  },
  "rate_limits": {
    "requests_per_minute": 60,
    "requests_per_hour": 1000
  },
  "fallback": {
    "enabled": true,
    "auto_switch": true,
    "log_switches": true
  }
}
```

### Environment Variables
```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
export PRIMARY_MODEL="kimi-coding/k2p5"
export FALLBACK_MODELS="openrouter/gpt-4o,openrouter/claude-3-opus"
```

---

## 🚀 Benefits

1. **No Interruption:** Seamless fallback
2. **Cost Control:** Use cheaper models when possible
3. **Reliability:** Multiple providers
4. **Flexibility:** Easy to add new models

---

**Last Updated:** 2026-03-05  
**Next Review:** When adding new models
