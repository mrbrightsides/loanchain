# 🔌 Third-Party API Integration Guide

Comprehensive documentation for external service integrations in LoanChain Ledger.

Repository: [https://github.com/mrbrightsides/loanchain](https://github.com/mrbrightsides/loanchain)

---

## Overview

LoanChain Ledger integrates with multiple third-party services to provide AI assistance, decentralized storage, blockchain functionality, and microfinance data access. This document outlines integration patterns, configuration requirements, and usage guidelines.

---

## 🤖 OpenAI API Integration

### Purpose

Provides intelligent conversational AI for user onboarding, feature guidance, and contextual assistance throughout the platform.

### Implementation Location

**File**: `src/app/api/ai-chat/route.ts`

**Type**: Server-side API route (Next.js)

### Configuration

```typescript
const OPENAI_API_KEY = process.env.OPENAI_API_KEY || 'configure-api-key';
```

### API Specifications

| Parameter | Value |
|-----------|-------|
| **Endpoint** | `https://api.openai.com/v1/chat/completions` |
| **Model** | `gpt-4o-mini` |
| **Authentication** | Bearer token (API key) |
| **Method** | POST |
| **Content-Type** | application/json |

### Request Structure

```typescript
{
  model: 'gpt-4o-mini',
  messages: [
    { role: 'system', content: 'System prompt defining AI behavior' },
    { role: 'user', content: 'User message' }
  ],
  temperature: 0.7,
  max_tokens: 800
}
```

### Response Handling

```typescript
const completion = await openai.chat.completions.create(requestBody);
const aiResponse = completion.choices[0].message.content;
```

### Features

- **Context-Aware Responses**: AI understands LoanChain features and provides relevant guidance
- **Quick Prompts**: Pre-configured questions for common user queries
- **Conversation History**: Maintains context across user interactions
- **Error Handling**: Graceful degradation on API failures

### Rate Limits

- Tier-dependent (check OpenAI account tier)
- Implement request throttling for production
- Monitor token usage to optimize costs

### Security Considerations

- API key stored server-side only
- Never expose key in client-side code
- Use environment variables for credential management
- Implement request validation to prevent abuse

### Obtaining API Key

1. Create account at https://platform.openai.com
2. Navigate to API Keys section
3. Generate new API key
4. Store securely in environment variables

---

## ☁️ Pinata IPFS Integration

### Purpose

Provides decentralized, immutable document storage using InterPlanetary File System (IPFS), ensuring tamper-proof audit trails for loan documents.

### Implementation Location

**File**: `src/app/api/pinata/route.ts`

**Type**: Server-side API route (Next.js)

### Configuration

```typescript
const PINATA_JWT = process.env.PINATA_JWT || 'configure-jwt-token';
```

### API Specifications

| Parameter | Value |
|-----------|-------|
| **Upload Endpoint** | `https://uploads.pinata.cloud/v3/files` |
| **Gateway** | `https://gateway.pinata.cloud/ipfs/{CID}` |
| **Authentication** | JWT Bearer token |
| **Method** | POST |
| **Content-Type** | multipart/form-data |

### Upload Implementation

```typescript
const formData = new FormData();
files.forEach((file) => {
  formData.append('file', file);
});
formData.append('name', documentName);
formData.append('group_id', groupId);

const response = await fetch('https://uploads.pinata.cloud/v3/files', {
  method: 'POST',
  headers: { Authorization: `Bearer ${PINATA_JWT}` },
  body: formData
});
```

### Response Structure

```typescript
{
  data: {
    id: "unique-file-id",
    name: "document.pdf",
    cid: "QmXxx...",
    size: 1024,
    created_at: "2024-01-01T00:00:00.000Z",
    group_id: "group-uuid"
  }
}
```

### Features

- **Batch Upload**: Multiple documents in single request
- **CID Generation**: Content-addressable identifiers for file retrieval
- **Group Management**: Organize uploads by loan or user
- **Gateway Access**: Public IPFS access via Pinata gateway
- **Immutable Storage**: Permanent, tamper-proof document records

### File Size Limits

- Single file: 50MB
- Batch upload: 50MB total
- Larger files require chunked uploads (not implemented)

### Security Considerations

- JWT token stored server-side only
- Files publicly accessible via IPFS once uploaded
- Do not upload sensitive PII without encryption
- Implement file validation before upload

### Gateway URL Pattern

```
https://gateway.pinata.cloud/ipfs/{CID}
```

**Example:**
```
https://gateway.pinata.cloud/ipfs/QmXYZ123abc456def789
```

### Obtaining API Credentials

1. Create account at https://pinata.cloud
2. Navigate to API Keys section
3. Generate new JWT token
4. Store securely in environment variables

---

## ⛓️ OnchainKit (Base Blockchain)

### Purpose

Provides comprehensive Base blockchain integration including smart wallets, token operations, identity resolution, and on-chain transaction management.

### Implementation Locations

**Configuration**: `src/app/config/onchainkit.ts`  
**API Helpers**: `src/app/types/api.ts`  
**Providers**: `src/app/providers.tsx`  
**Wagmi Config**: `src/lib/wagmi.ts`

### Configuration

```typescript
// src/app/config/onchainkit.ts
export const ONCHAINKIT_PROJECT_ID = process.env.NEXT_PUBLIC_ONCHAINKIT_PROJECT_ID || 'configure-project-id';
export const ONCHAINKIT_API_KEY = process.env.ONCHAINKIT_API_KEY || 'configure-api-key';
```

### API Specifications

| Parameter | Value |
|-----------|-------|
| **Version** | 1.1.1 |
| **Supported Chains** | Base (8453), Base Sepolia (84532) |
| **Package** | `@coinbase/onchainkit` |
| **Dependencies** | wagmi 2.18.2+, viem 2.38.4+ |

### Provider Setup

```typescript
<OnchainKitProvider
  apiKey={ONCHAINKIT_API_KEY}
  projectId={ONCHAINKIT_PROJECT_ID}
  chain={activeChain}
  config={{
    appearance: {
      name: 'LoanChain Ledger',
      logo: 'logo-url',
      mode: 'auto',
      theme: 'default',
    },
  }}
>
  {children}
</OnchainKitProvider>
```

### Core Features

#### 1. Wallet Integration

**Supported Wallets:**
- Coinbase Wallet (Smart Wallet + EOA)
- MetaMask
- Phantom
- Rabby
- Trust Wallet

**Implementation:**
```typescript
import { useAccount, useConnect } from 'wagmi';

const { address, status } = useAccount();
const { connect, connectors } = useConnect();
```

#### 2. Token Operations

**Get Token Information:**
```typescript
import { getTokens, unwrapOnchainKitResponse } from '@/app/types/api';

const response = await getTokens({ search: 'USDC', limit: '10' });
const tokens = unwrapOnchainKitResponse(response);
```

**Swap Tokens:**
```typescript
import { getSwapQuote, buildSwapTransaction } from '@/app/types/api';

const quote = unwrapOnchainKitResponse(await getSwapQuote({
  amount: '1',
  from: tokenA,
  to: tokenB,
  useAggregator: false,
}));

const swapTx = unwrapOnchainKitResponse(await buildSwapTransaction({
  ...quoteParams,
  fromAddress: userAddress,
}));
```

#### 3. Portfolio & Pricing

**Get Portfolio:**
```typescript
import { getPortfolios } from '@/app/types/api';

const portfolios = unwrapOnchainKitResponse(
  await getPortfolios({ addresses: [walletAddress] })
);
```

**Get Price Quote:**
```typescript
import { getPriceQuote } from '@/app/types/api';

const priceQuote = unwrapOnchainKitResponse(
  await getPriceQuote({ tokens: ['ETH', '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913'] })
);
```

#### 4. Identity Resolution

```typescript
import { getName, getAvatar, getAddresses } from '@coinbase/onchainkit/identity';

const displayName = await getName({ address: '0x...' });
const avatar = await getAvatar({ address: '0x...' });
const addressList = await getAddresses({ names: ['alice.base.eth'] });
```

### Error Handling

```typescript
import { isApiError, unwrapOnchainKitResponse } from '@/app/types/api';

const response = await getTokens({ search: 'USDC' });

if (isApiError(response)) {
  console.error('API Error:', response.message);
  // Handle error
} else {
  // Use response
}

// Or use unwrap (throws on error)
try {
  const tokens = unwrapOnchainKitResponse(response);
} catch (error) {
  console.error('API Error:', error.message);
}
```

### Network Configuration

```typescript
// src/lib/wagmi.ts
const chainId = process.env.NEXT_PUBLIC_SDK_CHAIN_ID
  ? Number(process.env.NEXT_PUBLIC_SDK_CHAIN_ID)
  : baseSepolia.id;
  
export const activeChain = chainId === 84532 ? baseSepolia : base;
```

### Security Considerations

- API key required for certain operations
- Project ID can be public (used client-side)
- Always validate addresses before transactions
- Implement transaction confirmations for high-value operations
- Use testnet (Base Sepolia) for development

### Obtaining API Credentials

1. Create account at https://portal.cdp.coinbase.com
2. Create new project
3. Copy Project ID and API Key
4. Configure in environment variables

---

## 🌱 GreenLend API Integration

### Purpose

Provides real-time microfinance data integration, enabling LoanChain Ledger to bridge institutional syndicated loans with grassroots lending opportunities.

### Implementation Location

**File**: `src/lib/greenlend-integration.ts`  
**Hook**: `src/hooks/useGreenLendPortfolio.ts`

### API Specifications

| Parameter | Value |
|-----------|-------|
| **Base URL** | `https://api-staging.greenlend.xyz` |
| **Environment** | Staging (no authentication required) |
| **Method** | GET |
| **Content-Type** | application/json |

### Available Endpoints

#### 1. Portfolio Data

**Endpoint**: `/portfolios`

**Response Structure:**
```typescript
{
  portfolios: [
    {
      id: "portfolio-uuid",
      name: "Microfinance Portfolio A",
      totalValue: 50000,
      loanCount: 120,
      averageRisk: 3.2,
      region: "Southeast Asia",
      borrowers: [...]
    }
  ]
}
```

#### 2. Risk Metrics

**Endpoint**: `/risk-assessment`

**Response Structure:**
```typescript
{
  overallRisk: 2.8,
  riskFactors: [
    { factor: "Credit History", score: 3.1 },
    { factor: "Regional Stability", score: 2.5 }
  ],
  recommendations: [...]
}
```

### Integration Implementation

```typescript
// src/lib/greenlend-integration.ts
export async function fetchGreenLendPortfolios() {
  const response = await fetch('https://api-staging.greenlend.xyz/portfolios', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' }
  });
  
  if (!response.ok) {
    throw new Error('Failed to fetch GreenLend data');
  }
  
  return await response.json();
}
```

### React Hook Usage

```typescript
// src/hooks/useGreenLendPortfolio.ts
import { useState, useEffect } from 'react';
import { fetchGreenLendPortfolios } from '@/lib/greenlend-integration';

export function useGreenLendPortfolio() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    fetchGreenLendPortfolios()
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);
  
  return { data, loading, error };
}
```

### Features

- **Real-Time Data**: Access to current microfinance portfolios
- **Risk Assessment**: Quantitative risk scoring
- **Borrower Profiles**: Detailed microfinance borrower information
- **Regional Insights**: Geographic distribution of loans
- **Performance Metrics**: Historical loan performance data

### Rate Limits

- Staging environment: No rate limits
- Production environment: TBD (requires API credentials)

### Security Considerations

- Staging API requires no authentication
- Production deployment requires API key
- Data cached client-side for performance
- Implement error handling for API unavailability

### Production Configuration

```typescript
// Future production implementation
const GREENLEND_API_KEY = process.env.GREENLEND_API_KEY;
const GREENLEND_BASE_URL = process.env.GREENLEND_API_URL || 'https://api.greenlend.xyz';

const response = await fetch(`${GREENLEND_BASE_URL}/portfolios`, {
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${GREENLEND_API_KEY}`
  }
});
```

---

## 🔒 Security Best Practices

### API Key Management

1. **Never commit API keys to version control**
   ```bash
   # Add to .gitignore
   .env.local
   .env*.local
   ```

2. **Use environment variables**
   ```typescript
   const API_KEY = process.env.API_KEY || 'fallback-for-dev';
   ```

3. **Server-side only for sensitive keys**
   - OpenAI API keys
   - Pinata JWT tokens
   - OnchainKit API keys (not Project IDs)

4. **Rotate keys regularly**
   - Implement key rotation policy
   - Monitor for unauthorized usage

### Request Validation

```typescript
// Example validation middleware
function validateApiRequest(req: Request) {
  // Validate request origin
  const origin = req.headers.get('origin');
  if (!isAllowedOrigin(origin)) {
    throw new Error('Unauthorized origin');
  }
  
  // Validate request format
  if (!req.body || typeof req.body !== 'object') {
    throw new Error('Invalid request format');
  }
  
  return true;
}
```

### Rate Limiting

```typescript
// Example rate limiting implementation
import { Ratelimit } from '@upstash/ratelimit';

const ratelimit = new Ratelimit({
  redis: redisClient,
  limiter: Ratelimit.slidingWindow(10, '10 s'),
});

async function handleRequest(req: Request) {
  const identifier = getClientIdentifier(req);
  const { success } = await ratelimit.limit(identifier);
  
  if (!success) {
    return new Response('Too Many Requests', { status: 429 });
  }
  
  // Process request
}
```

---

## 📊 Error Handling Patterns

### Standardized Error Response

```typescript
interface ApiError {
  error: string;
  message: string;
  code: string;
  status: number;
}

function createErrorResponse(error: unknown): ApiError {
  return {
    error: error instanceof Error ? error.message : 'Unknown error',
    message: 'API request failed',
    code: 'API_ERROR',
    status: 500
  };
}
```

### Client-Side Error Handling

```typescript
async function safeApiCall<T>(apiFunction: () => Promise<T>): Promise<T | null> {
  try {
    return await apiFunction();
  } catch (error) {
    console.error('API Error:', error);
    // Show user-friendly error message
    toast.error('Unable to complete request. Please try again.');
    return null;
  }
}
```

---

## 🧪 Testing API Integrations

### Environment Setup

```bash
# Create test environment file
cp .env.local .env.test.local

# Configure test API keys (use sandbox/test accounts)
```

### Integration Tests

```typescript
// Example test structure
describe('OpenAI Integration', () => {
  it('should return AI response', async () => {
    const response = await fetch('/api/ai-chat', {
      method: 'POST',
      body: JSON.stringify({ message: 'Test message' })
    });
    
    expect(response.ok).toBe(true);
    const data = await response.json();
    expect(data.response).toBeDefined();
  });
});
```

---

## 📚 Additional Resources

### API Documentation

- **OpenAI**: https://platform.openai.com/docs/api-reference
- **Pinata**: https://docs.pinata.cloud/api-reference
- **OnchainKit**: https://onchainkit.xyz/api
- **GreenLend**: Contact for production API documentation

### Support

For API integration issues:
1. Review error messages in browser console
2. Check API service status pages
3. Verify API credentials are configured correctly
4. Submit issues to GitHub repository
