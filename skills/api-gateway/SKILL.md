---
name: api-gateway
description: Design, implement, and manage API gateways. Use when building REST APIs, GraphQL endpoints, webhook handlers, or API middleware. Includes patterns for authentication, rate limiting, caching, and API documentation.
---

# API Gateway Skill

This skill provides patterns and best practices for designing and implementing API gateways.

## When to Use

- Building REST APIs
- Creating GraphQL endpoints
- Setting up webhook handlers
- Implementing API middleware
- Designing microservices architecture
- Adding authentication/authorization to APIs

## Core Patterns

### 1. REST API Design

#### URL Structure
```
/api/v1/resources          # List all
/api/v1/resources/{id}     # Get one
/api/v1/resources          # POST create
/api/v1/resources/{id}     # PUT update
/api/v1/resources/{id}     # DELETE remove
```

#### Response Format
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 100
  }
}
```

#### Error Format
```json
{
  "success": false,
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource was not found",
    "details": { ... }
  }
}
```

### 2. Authentication Patterns

#### JWT Authentication
```javascript
// Verify JWT middleware
const verifyJWT = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ error: 'No token' });
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (err) {
    res.status(401).json({ error: 'Invalid token' });
  }
};
```

#### API Key Authentication
```javascript
const verifyAPIKey = (req, res, next) => {
  const apiKey = req.headers['x-api-key'];
  if (!apiKey || !validKeys.includes(apiKey)) {
    return res.status(401).json({ error: 'Invalid API key' });
  }
  next();
};
```

### 3. Rate Limiting

#### Simple In-Memory
```javascript
const requests = new Map();

const rateLimit = (req, res, next) => {
  const key = req.ip;
  const now = Date.now();
  const windowStart = now - 60000; // 1 minute
  
  const userRequests = requests.get(key) || [];
  const recentRequests = userRequests.filter(t => t > windowStart);
  
  if (recentRequests.length >= 100) {
    return res.status(429).json({ error: 'Rate limit exceeded' });
  }
  
  recentRequests.push(now);
  requests.set(key, recentRequests);
  next();
};
```

### 4. Caching Strategies

#### Response Caching
```javascript
const cache = new Map();

const cacheMiddleware = (duration = 300) => {
  return (req, res, next) => {
    const key = req.originalUrl;
    const cached = cache.get(key);
    
    if (cached && cached.expiry > Date.now()) {
      return res.json(cached.data);
    }
    
    // Override res.json to cache response
    const originalJson = res.json.bind(res);
    res.json = (data) => {
      cache.set(key, { data, expiry: Date.now() + duration * 1000 });
      return originalJson(data);
    };
    
    next();
  };
};
```

## Implementation Examples

### Express.js Gateway
```javascript
const express = require('express');
const app = express();

// Middleware
app.use(express.json());
app.use(rateLimit);
app.use(verifyJWT);

// Routes
app.get('/api/v1/users', cacheMiddleware(60), async (req, res) => {
  const users = await db.users.findAll();
  res.json({ success: true, data: users });
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ 
    success: false, 
    error: { code: 'INTERNAL_ERROR', message: 'Something went wrong' }
  });
});
```

### Webhook Handler
```javascript
app.post('/webhooks/:service', async (req, res) => {
  const signature = req.headers['x-webhook-signature'];
  
  // Verify signature
  if (!verifySignature(req.body, signature)) {
    return res.status(401).json({ error: 'Invalid signature' });
  }
  
  // Process webhook
  await processWebhook(req.params.service, req.body);
  
  res.json({ success: true });
});
```

## Security Best Practices

1. **Always use HTTPS** in production
2. **Validate input** - Use Joi, Yup, or Zod
3. **Sanitize output** - Prevent XSS
4. **Rate limit** - Prevent abuse
5. **Log requests** - For debugging and monitoring
6. **Use CORS** - Control cross-origin access
7. **Version your API** - /v1/, /v2/

## Tools & Libraries

- **Express.js** - Node.js framework
- **Fastify** - High-performance alternative
- **Helmet** - Security headers
- **CORS** - Cross-origin handling
- **Rate-limiter-flexible** - Advanced rate limiting
- **Swagger/OpenAPI** - API documentation

## Related Skills

- `code` - General coding patterns
- `frontend-design` - API consumption patterns
