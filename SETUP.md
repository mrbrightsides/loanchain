# 🚀 LoanChain Ledger - Installation & Setup

Enterprise-grade blockchain platform for syndicated loan markets, built for the LMA Edge Hackathon 2026.

Repository: [https://github.com/mrbrightsides/loanchain](https://github.com/mrbrightsides/loanchain)

---

## Prerequisites

| Requirement | Version | Purpose |
|------------|---------|---------|
| Node.js | 18.x or higher | Runtime environment |
| pnpm | 8.0.0+ | Package management |
| Git | Latest | Version control |
| Browser | Latest (Chrome/Firefox/Edge/Safari) | Application interface |
| Web3 Wallet | Coinbase Wallet or MetaMask | Blockchain interactions |

### Verification Commands

```bash
node --version    # Verify Node.js installation
pnpm --version    # Verify pnpm installation

# Install pnpm if needed
npm install -g pnpm
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/mrbrightsides/loanchain.git
cd loanchain
```

### 2. Install Dependencies

```bash
pnpm install
```

**Core Dependencies:**
- Next.js 15.3.8+ (React framework)
- React 19 (UI library)
- TypeScript (Type safety)
- Tailwind CSS (Styling)
- OnchainKit 1.1.1 (Base blockchain toolkit)
- Viem 2.38.4+ & Wagmi 2.18.2+ (Ethereum interactions)
- Framer Motion (Animations)
- Additional dependencies detailed in `package.json`

---

## Configuration

### Required API Keys

LoanChain Ledger integrates with multiple third-party services. Configuration files contain placeholders for API credentials.

> **Security Note**: Never commit API keys to version control. All credentials must be configured in appropriate server-side files before deployment.

#### 1. OpenAI API (AI Assistant)

**Configuration File**: `src/app/api/ai-chat/route.ts`

```typescript
const OPENAI_API_KEY = process.env.OPENAI_API_KEY || 'your-api-key-here';
```

**Requirements:**
- OpenAI API account
- GPT-4o-mini access
- API key with chat completion permissions

**Purpose**: Context-aware AI assistant for user onboarding and support.

---

#### 2. Pinata Cloud (IPFS Storage)

**Configuration File**: `src/app/api/pinata/route.ts`

```typescript
const PINATA_JWT = process.env.PINATA_JWT || 'your-jwt-token-here';
```

**Requirements:**
- Pinata account
- JWT authentication token
- IPFS upload permissions

**Purpose**: Decentralized document storage with immutable audit trails.

**Gateway**: `https://gateway.pinata.cloud/ipfs/{CID}`

---

#### 3. OnchainKit (Base Blockchain)

**Configuration File**: `src/app/config/onchainkit.ts`

```typescript
export const ONCHAINKIT_PROJECT_ID = process.env.NEXT_PUBLIC_ONCHAINKIT_PROJECT_ID || 'your-project-id';
export const ONCHAINKIT_API_KEY = process.env.ONCHAINKIT_API_KEY || 'your-api-key';
```

**Requirements:**
- Coinbase Developer account
- OnchainKit project configuration
- API key with Base network access

**Purpose**: Smart wallet integration, token operations, and on-chain transaction verification.

**Supported Networks**: Base (mainnet), Base Sepolia (testnet)

---

#### 4. GreenLend API

**Configuration File**: `src/lib/greenlend-integration.ts`

**API Endpoint**: `https://api-staging.greenlend.xyz`

**Requirements:**
- No authentication required for staging environment
- Production deployment requires API credentials

**Purpose**: Real-time microfinance data integration for loan portfolios and risk assessment.

---

### Environment Variables (Optional)

Create `.env.local` in root directory:

```env
# Blockchain Configuration
NEXT_PUBLIC_SDK_CHAIN_ID=84532        # 84532 (Base Sepolia) | 8453 (Base mainnet)
RPC_URL=https://your-rpc-endpoint     # Custom RPC (optional)

# API Credentials (Configure as needed)
OPENAI_API_KEY=your-openai-key
PINATA_JWT=your-pinata-jwt-token
NEXT_PUBLIC_ONCHAINKIT_PROJECT_ID=your-project-id
ONCHAINKIT_API_KEY=your-api-key
```

> **Note**: Environment variables override hardcoded values. For security, always use environment variables in production.

---

## Architecture Overview

### Blockchain Infrastructure

**Wagmi Configuration** (`src/lib/wagmi.ts`)

```typescript
export const activeChain = chainId === 84532 ? baseSepolia : base;

export const config = createConfig({
  chains: [activeChain],
  connectors: [
    coinbaseWallet({ appName: 'Ohara', preference: 'all' }),
    metaMask({ dappMetadata: { name: 'Ohara' } }),
    injected({ target: 'phantom' }),
    injected({ target: 'rabby' }),
    injected({ target: 'trust' }),
  ],
  transports: {
    [activeChain.id]: http(process.env.RPC_URL),
  }
});
```

**Supported Wallets:**
- Coinbase Wallet (Smart Wallet + EOA)
- MetaMask
- Phantom
- Rabby
- Trust Wallet

---

### Provider Hierarchy

**Configuration** (`src/app/providers.tsx`)

```
WagmiProvider
  └─ QueryClientProvider
      └─ OnchainKitProvider
          └─ Application Components
```

**Capabilities:**
- Blockchain connection management
- React Query data fetching
- OnchainKit components/hooks
- Farcaster MiniKit integration

---

## Development

### Local Development Server

```bash
pnpm dev
```

Application available at: `http://localhost:3000`

**Features:**
- Hot module replacement
- Real-time updates
- Full debugging support
- Source maps enabled

---

### Production Build

```bash
# Build optimized bundle
pnpm build

# Start production server
pnpm start
```

**Build Output:**
- Optimized JavaScript bundles
- Static page generation
- API routes compilation
- Asset optimization

---

### Build Verification

Automated checks during build process:
- TypeScript compilation validation
- Next.js configuration verification
- API route testing
- Import dependency resolution

> **Note**: Peer dependency warnings for optional wallet SDKs are expected and do not affect functionality.

---

## Project Structure

```
loanchain/
├── src/
│   ├── app/
│   │   ├── api/                       # Server-side API routes
│   │   │   ├── ai-chat/               # OpenAI integration
│   │   │   ├── pinata/                # IPFS upload handler
│   │   │   ├── me/                    # Quick Auth endpoint
│   │   │   └── proxy/                 # System proxy (reserved)
│   │   ├── config/                    # Application configuration
│   │   │   └── onchainkit.ts          # Base blockchain config
│   │   ├── types/                     # TypeScript definitions
│   │   │   └── api.ts                 # OnchainKit API types
│   │   ├── whitepaper/                # Technical whitepaper
│   │   ├── layout.tsx                 # Root layout + providers
│   │   ├── page.tsx                   # Main application entry
│   │   ├── providers.tsx              # Provider configuration
│   │   └── globals.css                # Global styles
│   ├── components/
│   │   ├── loan/                      # Loan management components
│   │   ├── ui/                        # Reusable UI library
│   │   ├── wallet/                    # Wallet integration
│   │   ├── AIChatbot.tsx              # AI assistant interface
│   │   └── Farcaster*.tsx             # Farcaster integration
│   ├── hooks/                         # Custom React hooks
│   │   ├── useGreenLendPortfolio.ts   # GreenLend data fetching
│   │   ├── useLoanContract.ts         # Smart contract interactions
│   │   ├── useQuickAuth.tsx           # Farcaster authentication
│   │   └── useIsInFarcaster.ts        # Context detection
│   ├── lib/                           # Utility libraries
│   │   ├── wagmi.ts                   # Wagmi configuration
│   │   ├── contracts.ts               # Smart contract ABIs
│   │   ├── greenlend-integration.ts   # GreenLend API client
│   │   └── utils.ts                   # Helper functions
│   └── contracts/
│       └── LoanRegistry.sol           # Solidity smart contract
├── public/
│   └── .well-known/
│       └── farcaster.json             # Farcaster manifest
├── package.json                       # Dependencies
├── tsconfig.json                      # TypeScript config
├── tailwind.config.ts                 # Tailwind CSS config
├── next.config.ts                     # Next.js config
├── README.md                          # Project overview
├── SETUP.md                           # This file
└── THIRD_PARTY_APIS.md                # API integration docs
```

---

## Farcaster Integration

LoanChain Ledger includes Farcaster MiniApp capabilities with automatic build-time injection.

### Auto-Generated Components

**Build Process Creates:**
1. Farcaster manifest: `public/.well-known/farcaster.json`
2. Manifest signer: `src/components/FarcasterManifestSigner.tsx`
3. Toast manager: `src/components/FarcasterToastManager.tsx`
4. Wrapper component: `src/components/FarcasterWrapper.tsx`

**Custom Hooks:**
- `src/hooks/useAddMiniApp.ts` - MiniApp registration
- `src/hooks/useQuickAuth.tsx` - Quick Auth flow
- `src/hooks/useIsInFarcaster.ts` - Context detection

### SDK Integration

Farcaster SDK (`@farcaster/miniapp-sdk`) automatically injected into:
- `src/app/layout.tsx` - Metadata configuration
- `src/app/page.tsx` - SDK initialization

**Features:**
- Quick Auth instant sign-in
- Mini app registration
- Context detection
- Toast notifications

---

## Troubleshooting

### Port Conflict

```bash
# Terminate process using port 3000
lsof -ti:3000 | xargs kill -9

# Use alternative port
pnpm dev --port 3001
```

---

### Optional Dependencies Warning

**Expected Messages:**
```
Module not found: Can't resolve '@metamask/sdk-react'
Module not found: Can't resolve '@walletconnect/ethereum-provider'
```

**Resolution**: These are optional peer dependencies for wallet connectors. No action required.

---

### TypeScript Build Errors

```bash
# Clear build cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules pnpm-lock.yaml
pnpm install

# Rebuild application
pnpm build
```

---

### IPFS Upload Failures

**Common Causes:**
- Network connectivity issues
- File size exceeds 50MB limit
- Pinata API rate limiting

**Resolution:**
- Verify internet connection
- Reduce file size
- Retry after rate limit reset

---

### Wallet Connection Issues

**Common Causes:**
- Wallet extension not installed
- Incorrect network selected
- Browser blocking pop-ups

**Resolution:**
- Install required wallet extension
- Switch to Base or Base Sepolia network
- Enable pop-ups for application domain
- Clear browser cache and retry

---

### AI Chatbot Errors

**Common Causes:**
- OpenAI API rate limits
- Invalid API credentials
- Network connectivity

**Resolution:**
- Wait for rate limit reset
- Verify API key configuration
- Check browser console for detailed errors

---

## Testing Checklist

### Installation Verification

- [ ] Node.js 18+ installed
- [ ] pnpm installed and functional
- [ ] Dependencies installed successfully
- [ ] No critical installation errors

### Application Verification

- [ ] Development server starts without errors
- [ ] Application loads at http://localhost:3000
- [ ] All navigation tabs accessible
- [ ] No console errors or warnings

### Integration Testing

- [ ] AI chatbot responds to queries
- [ ] IPFS document upload successful
- [ ] Wallet connection functional
- [ ] GreenLend data loads correctly
- [ ] All dashboard components render

---

## Documentation

### Technical Resources

- [README.md](README.md) - Project overview and architecture
- [THIRD_PARTY_APIS.md](THIRD_PARTY_APIS.md) - Detailed API integration guide
- [Whitepaper](src/app/whitepaper/page.tsx) - Technical specifications

### External Documentation

- **Next.js**: https://nextjs.org/docs
- **OnchainKit**: https://onchainkit.xyz
- **Wagmi**: https://wagmi.sh
- **Viem**: https://viem.sh
- **Pinata**: https://docs.pinata.cloud
- **OpenAI**: https://platform.openai.com/docs
- **Base**: https://docs.base.org

---

## Support

For issues, bug reports, or feature requests:
1. Check browser DevTools console for errors
2. Review documentation and troubleshooting guides
3. Submit issues to GitHub repository
4. Contact development team

---

## License

See LICENSE file for details.

---

*LoanChain Ledger - Blockchain Syndicated Loan Platform*  
*Built for LMA Edge Hackathon 2026*  
*Repository: https://github.com/mrbrightsides/loanchain*
