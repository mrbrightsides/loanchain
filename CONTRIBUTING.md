# Contributing to LoanChain Ledger

Thank you for your interest in contributing to LoanChain Ledger! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Project Structure](#project-structure)
- [Making Changes](#making-changes)
- [Testing Guidelines](#testing-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)
- [Documentation](#documentation)
- [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors. We expect all participants to:

- Be respectful and considerate
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other contributors

### Unacceptable Behavior

- Harassment, discrimination, or trolling
- Publishing others' private information
- Offensive comments or personal attacks
- Any conduct that could reasonably be considered inappropriate

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

1. **Read the documentation**:
   - [README.md](./README.md) - Project overview
   - [SETUP.md](./SETUP.md) - Setup instructions
   - [THIRD-PARTY-APIS.md](./THIRD-PARTY-APIS.md) - API documentation

2. **Development environment**:
   - Node.js 18+ installed
   - pnpm package manager
   - Git configured
   - Code editor (VS Code recommended)

3. **Fork and clone**:
   ```bash
   # Fork the repository on GitHub
   # Clone your fork
   git clone https://github.com/mrbrightsides/loanchain.git
   cd loanchain-ledger
   
   # Add upstream remote
   git remote add upstream https://github.com/ORIGINAL_OWNER/loanchain-ledger.git
   ```

4. **Install dependencies**:
   ```bash
   pnpm install
   ```

5. **Verify setup**:
   ```bash
   pnpm dev
   # Open http://localhost:3000
   ```

---

## Development Workflow

### 1. Create a Feature Branch

Always create a new branch for your work:

```bash
# Update main branch
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 2. Branch Naming Convention

- `feature/` - New features (e.g., `feature/nft-minting`)
- `fix/` - Bug fixes (e.g., `fix/ipfs-upload-error`)
- `docs/` - Documentation updates (e.g., `docs/api-guide`)
- `refactor/` - Code refactoring (e.g., `refactor/loan-service`)
- `test/` - Adding tests (e.g., `test/obligations-unit`)
- `chore/` - Maintenance tasks (e.g., `chore/update-deps`)

### 3. Make Your Changes

- Follow [Coding Standards](#coding-standards)
- Write clean, readable code
- Add comments for complex logic
- Update documentation if needed

### 4. Test Your Changes

```bash
# Run development server
pnpm dev

# Build for production
pnpm build

# Test all features manually:
# - AI Chatbot
# - IPFS Upload
# - Wallet Connection
# - GreenLend Integration
```

### 5. Commit Your Changes

Follow [Commit Message Guidelines](#commit-message-guidelines):

```bash
git add .
git commit -m "feat: add batch document upload to IPFS"
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

---

## Coding Standards

### TypeScript Guidelines

#### 1. Strict Typing (CRITICAL)

```typescript
// ✅ GOOD - Explicit types
interface LoanData {
  id: string;
  amount: number;
  borrower: string;
}

function createLoan(data: LoanData): Promise<Loan> {
  // ...
}

// ❌ BAD - Implicit any
function createLoan(data) {
  // ...
}
```

#### 2. No Implicit `any`

```typescript
// ✅ GOOD - Proper typing for dynamic access
const config: Record<string, string | number> = {
  api: 'url',
  timeout: 5000
};

function getValue<T extends Record<string, unknown>>(
  obj: T,
  key: keyof T
): T[keyof T] {
  return obj[key];
}

// ❌ BAD - Implicit any
const value = config[userInput]; // Error!
```

#### 3. Interface Definitions

```typescript
// ✅ GOOD - Clear interface at top of file
interface Obligation {
  id: string;
  loanId: string;
  type: 'payment' | 'covenant' | 'document' | 'status';
  dueDate: string;
  status: 'overdue' | 'due_soon' | 'upcoming' | 'completed';
  priority: 'critical' | 'high' | 'medium' | 'low';
  amount?: number;
  description: string;
  blockchainVerified: boolean;
}

// ❌ BAD - Inline types
function processObligation(obligation: {
  id: string;
  loanId: string;
  // ... many fields
}) {
  // ...
}
```

#### 4. Type Imports

```typescript
// ✅ GOOD - Type-only imports
import type { Loan } from '@/types/loan';
import { type User, type Account } from '@/types/auth';

// ❌ BAD - Runtime imports for types
import { Loan } from '@/types/loan';
```

### React & Next.js Guidelines

#### 1. Client Components

```typescript
// ✅ GOOD - 'use client' at the very top
'use client';

import { useState } from 'react';
import type { FC } from 'react';

interface Props {
  initialValue: string;
}

const MyComponent: FC<Props> = ({ initialValue }) => {
  // ...
};
```

#### 2. Server Components (Default)

```typescript
// ✅ GOOD - No 'use client', async allowed
import { fetchLoans } from '@/lib/api';
import type { Loan } from '@/types/loan';

interface Props {
  loanId: string;
}

async function LoanDetails({ loanId }: Props) {
  const loan = await fetchLoans(loanId);
  return <div>{loan.borrower}</div>;
}
```

#### 3. API Routes

```typescript
// ✅ GOOD - Proper Next.js API route structure
import { NextRequest, NextResponse } from 'next/server';

interface RequestBody {
  loanId: string;
  amount: number;
}

export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    const body: RequestBody = await request.json();
    
    // Process request
    const result = await processLoan(body);
    
    return NextResponse.json({ success: true, data: result });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: 'Failed to process loan' },
      { status: 500 }
    );
  }
}
```

### Styling Guidelines

#### 1. Tailwind CSS

```tsx
// ✅ GOOD - Tailwind utility classes
<div className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg shadow-lg">
  <span className="text-white font-semibold">Loan Details</span>
</div>

// ❌ BAD - Inline styles (avoid unless necessary)
<div style={{ display: 'flex', padding: '16px' }}>
  <span style={{ color: 'white' }}>Loan Details</span>
</div>
```

#### 2. Responsive Design

```tsx
// ✅ GOOD - Mobile-first responsive
<div className="w-full md:w-1/2 lg:w-1/3 p-4 sm:p-6 lg:p-8">
  <h1 className="text-xl md:text-2xl lg:text-3xl">Title</h1>
</div>
```

#### 3. Animations (Framer Motion)

```tsx
// ✅ GOOD - Smooth animations
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  Content
</motion.div>
```

### File Organization

#### 1. Import Order

```typescript
// ✅ GOOD - Organized imports
// 1. React & Next.js
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

// 2. External libraries
import { motion } from 'framer-motion';
import { useAccount } from 'wagmi';

// 3. Internal utilities & types
import { uploadToIPFS } from '@/lib/ipfs';
import type { Loan } from '@/types/loan';

// 4. Components
import { Button } from '@/components/ui/button';
import { LoanCard } from '@/components/loans/LoanCard';

// 5. Styles (if any)
import styles from './styles.module.css';
```

#### 2. Component Structure

```typescript
// ✅ GOOD - Clear component structure
'use client';

import { useState } from 'react';
import type { FC } from 'react';

// Types
interface Props {
  loanId: string;
  onUpdate?: (loan: Loan) => void;
}

interface Loan {
  id: string;
  amount: number;
  borrower: string;
}

// Component
export const LoanEditor: FC<Props> = ({ loanId, onUpdate }) => {
  // 1. Hooks
  const [loan, setLoan] = useState<Loan | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  
  // 2. Effects
  useEffect(() => {
    fetchLoan();
  }, [loanId]);
  
  // 3. Handlers
  const fetchLoan = async (): Promise<void> => {
    // ...
  };
  
  const handleUpdate = async (): Promise<void> => {
    // ...
  };
  
  // 4. Render
  return (
    <div>
      {/* Component JSX */}
    </div>
  );
};
```

### Error Handling

```typescript
// ✅ GOOD - Comprehensive error handling
async function uploadDocument(file: File): Promise<{ cid: string }> {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch('/api/pinata', {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }
    
    const data = await response.json();
    
    if (!data.IpfsHash) {
      throw new Error('IPFS hash not returned');
    }
    
    return { cid: data.IpfsHash };
  } catch (error) {
    console.error('Document upload error:', error);
    throw error instanceof Error 
      ? error 
      : new Error('Unknown upload error');
  }
}
```

---

## Project Structure

### Key Directories

```
src/
├── app/                      # Next.js app directory
│   ├── page.tsx             # Main dashboard
│   ├── layout.tsx           # Root layout with providers
│   └── api/                 # API routes
│       ├── ai-chat/         # OpenAI chatbot endpoint
│       ├── pinata/          # IPFS upload endpoint
│       └── greenlend/       # Microfinance API proxy
├── components/              # React components
│   ├── ui/                  # Reusable UI components
│   ├── loans/               # Loan-related components
│   ├── obligations/         # Obligation-related components
│   └── documents/           # Document-related components
├── lib/                     # Utility functions
│   ├── ipfs.ts             # IPFS helpers
│   ├── blockchain.ts       # Blockchain utilities
│   └── wagmi.ts            # Wagmi configuration
├── types/                   # TypeScript type definitions
│   ├── loan.ts
│   ├── obligation.ts
│   └── document.ts
└── hooks/                   # Custom React hooks
    ├── useAddMiniApp.ts
    ├── useQuickAuth.tsx
    └── useIsInFarcaster.ts
```

### Adding New Features

#### Example: Adding a New Tab

1. **Create component**: `src/components/newtab/NewTab.tsx`
2. **Define types**: `src/types/newtab.ts`
3. **Add utilities**: `src/lib/newtab.ts` (if needed)
4. **Create API route**: `src/app/api/newtab/route.ts` (if needed)
5. **Import in main page**: `src/app/page.tsx`
6. **Update documentation**: `README.md`

---

## Making Changes

### Before You Start

- [ ] Check existing issues and PRs to avoid duplicates
- [ ] Discuss major changes in an issue first
- [ ] Read related documentation
- [ ] Ensure you understand the feature area

### While Working

- [ ] Write clean, readable code
- [ ] Follow TypeScript strict typing
- [ ] Add comments for complex logic
- [ ] Keep components small and focused
- [ ] Extract reusable logic into utilities
- [ ] Update types when adding new data structures

### Before Committing

- [ ] Test your changes locally
- [ ] Run `pnpm build` to check for errors
- [ ] Verify all features still work
- [ ] Check for TypeScript errors
- [ ] Review your own code
- [ ] Update documentation if needed

---

## Testing Guidelines

### Manual Testing Checklist

Since we don't have automated tests yet, thoroughly test:

#### Dashboard
- [ ] All tabs load correctly
- [ ] Navigation between tabs works
- [ ] Data displays properly
- [ ] No console errors

#### Loans Tab
- [ ] Loan list displays
- [ ] Search and filters work
- [ ] Loan details modal opens
- [ ] Risk heatmap renders
- [ ] GreenLend integration works

#### Create Tab
- [ ] Form validation works
- [ ] Templates load correctly
- [ ] Live calculations update
- [ ] Loan creation succeeds
- [ ] Form clears properly

#### Obligations Tab
- [ ] All three view modes work (List/Calendar/Timeline)
- [ ] Search and filters function
- [ ] Quick actions work (Complete/Reminder/Escalate)
- [ ] CSV export downloads
- [ ] Stats dashboard updates

#### Documents Tab
- [ ] Single file upload works
- [ ] Batch upload works
- [ ] Files upload to IPFS successfully
- [ ] IPFS CID displays correctly
- [ ] Download from IPFS works
- [ ] NFT minting works
- [ ] QR code generation works
- [ ] Search and filters function

#### AI Chatbot
- [ ] Chatbot button appears
- [ ] Chat window opens/closes
- [ ] Quick prompts work
- [ ] AI responds correctly
- [ ] Message history persists

#### Blockchain Integration
- [ ] Wallet connection works
- [ ] Base chain is selected
- [ ] OnchainKit components render
- [ ] Transactions can be initiated

### Testing New Features

When adding new features:

1. **Test happy path** - Feature works as expected
2. **Test edge cases** - Empty states, max limits, special characters
3. **Test error handling** - Network errors, invalid input, API failures
4. **Test mobile** - Responsive design, touch interactions
5. **Test browser compatibility** - Chrome, Firefox, Safari, Edge

---

## Commit Message Guidelines

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `style` - Code style changes (formatting, semicolons, etc.)
- `refactor` - Code refactoring
- `perf` - Performance improvements
- `test` - Adding tests
- `chore` - Maintenance tasks

### Scope

The area of code affected:
- `loans` - Loan-related features
- `obligations` - Obligation features
- `documents` - Document features
- `ai` - AI chatbot
- `ipfs` - IPFS integration
- `blockchain` - Blockchain/wallet features
- `ui` - UI components
- `api` - API routes
- `deps` - Dependencies

### Examples

```bash
# Good commit messages
feat(documents): add batch upload to IPFS
fix(obligations): correct calendar view date filtering
docs(readme): update setup instructions
refactor(loans): extract loan calculation logic
perf(dashboard): optimize risk heatmap rendering
chore(deps): update next to 15.3.8

# With body and footer
feat(ai): add context-aware chatbot

Implemented OpenAI GPT-4o-mini integration with:
- Quick prompts for common questions
- Context about all LoanChain features
- Smooth animations and clean UI

Closes #123
```

### Rules

1. Use imperative mood ("add" not "added")
2. Don't capitalize first letter of subject
3. No period at the end of subject
4. Subject line max 72 characters
5. Body wraps at 72 characters
6. Reference issues in footer

---

## Pull Request Process

### Before Creating PR

1. **Sync with upstream**:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. **Clean up commits** (optional):
   ```bash
   # Squash multiple commits if needed
   git rebase -i HEAD~3
   ```

3. **Push to your fork**:
   ```bash
   git push origin your-branch
   ```

### Creating the PR

1. **Go to GitHub** and create Pull Request
2. **Fill out the template**:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Changes Made
- Added batch upload to IPFS
- Updated document types
- Enhanced error handling

## Testing Done
- Tested single file upload
- Tested batch upload (5 files)
- Verified IPFS CIDs are correct
- Tested on Chrome and Firefox

## Screenshots (if applicable)
[Add screenshots]

## Related Issues
Closes #123
```

3. **Request review** from maintainers

### PR Review Process

1. **Automated checks** must pass
2. **Code review** by maintainer(s)
3. **Address feedback**:
   ```bash
   # Make changes
   git add .
   git commit -m "fix: address PR feedback"
   git push origin your-branch
   ```
4. **Approval** from at least one maintainer
5. **Merge** by maintainer

### After Merge

1. **Delete branch**:
   ```bash
   git checkout main
   git pull upstream main
   git branch -d your-branch
   git push origin --delete your-branch
   ```

2. **Celebrate** 🎉

---

## Reporting Issues

### Before Reporting

- [ ] Search existing issues
- [ ] Check if it's already fixed in latest version
- [ ] Reproduce the issue consistently

### Issue Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Screenshots
[Add screenshots if applicable]

## Environment
- Browser: Chrome 120
- OS: macOS 14.0
- Node: 18.17.0
- Next.js: 15.3.8

## Additional Context
Any other relevant information
```

---

## Feature Requests

### Template

```markdown
## Feature Description
Clear description of the proposed feature

## Problem It Solves
What problem does this feature address?

## Proposed Solution
How would you implement this?

## Alternatives Considered
What other approaches did you consider?

## Additional Context
Mockups, examples, references
```

---

## Documentation

### When to Update Documentation

Update documentation when you:
- Add new features
- Change existing behavior
- Add new API endpoints
- Add new dependencies
- Change configuration

### Documentation Files

- `README.md` - Project overview, features, architecture
- `SETUP.md` - Installation and setup instructions
- `CONTRIBUTING.md` - This file
- `THIRD-PARTY-APIS.md` - External API documentation
- Code comments - Complex logic, algorithms, workarounds

### Documentation Standards

- Use clear, simple language
- Include code examples
- Add screenshots for UI features
- Keep it up-to-date
- Use proper Markdown formatting

---

## Community

### Getting Help

- **GitHub Issues** - Report bugs, request features
- **Discussions** - Ask questions, share ideas
- **Documentation** - Read existing docs first

### Stay Updated

- Watch the repository for updates
- Check release notes for new versions
- Follow project milestones

### Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

---

## License

By contributing to LoanChain Ledger, you agree that your contributions will be licensed under the same license as the project.

---

## Questions?

If you have questions about contributing:
1. Check existing documentation
2. Search closed issues and PRs
3. Open a new discussion
4. Contact maintainers

Thank you for contributing to LoanChain Ledger! 🚀

---

**Built for LMA Edge Hackathon 2024**
