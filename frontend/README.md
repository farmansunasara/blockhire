# BlockHire Frontend

A modern, responsive frontend for the BlockHire employment verification system built with Next.js 14, React, and TypeScript.

## Features

- **User Authentication**: Registration and login with localStorage (demo mode)
- **Profile Management**: Complete profile creation and editing
- **Document Upload**: PDF upload with SHA-256 hash generation
- **Credentials Display**: Employee ID, User Hash, and Email management
- **Document History**: Track all uploaded documents
- **Issuer Dashboard**: Employee authorization and verification
- **Document Verification**: Verify document authenticity

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **UI Library**: shadcn/ui components
- **Styling**: Tailwind CSS
- **Forms**: React Hook Form with Zod validation
- **State Management**: React Context API
- **Icons**: Lucide React

## Getting Started

1. **Install Dependencies**
   ```bash
   npm install
   # or
   pnpm install
   ```

2. **Run Development Server**
   ```bash
   npm run dev
   # or
   pnpm dev
   ```

3. **Open Browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Demo Mode

The application runs in demo mode by default, using localStorage for data persistence. This means:

- No backend connection required
- All data is stored locally in the browser
- Perfect for development and testing
- Ready for Django backend integration

## Project Structure

```
frontend/
├── app/                    # Next.js app router pages
│   ├── login/             # Authentication pages
│   ├── profile/           # Profile management
│   ├── issuer/            # Issuer dashboard
│   └── verify/            # Document verification
├── components/            # Reusable UI components
│   ├── ui/               # shadcn/ui components
│   ├── Layout.tsx        # Main layout wrapper
│   ├── ProtectedRoute.tsx # Route protection
│   └── ...               # Custom components
├── contexts/             # React contexts
│   └── AuthContext.tsx   # Authentication state
├── services/             # API service layer
│   └── api.ts           # Mock API service
├── types/               # TypeScript type definitions
│   └── api.ts          # API and data types
└── lib/                # Utility functions
    └── utils.ts        # Helper utilities
```

## Key Components

### AuthContext
- Manages user authentication state
- Handles login/register/logout
- Loads user profile and credentials
- Uses localStorage for demo mode

### API Service
- Mock API service for development
- Ready for Django backend integration
- Handles all CRUD operations
- Includes proper error handling

### Profile Management
- Multi-step profile creation
- Form validation with Zod
- Document upload with hash generation
- Immutable credential display

### Issuer Dashboard
- Employee authorization workflow
- Document verification system
- Employee details lookup
- Clean tabbed interface

## Backend Integration

The frontend is designed to work with a Django backend. To integrate:

1. **Update API Service**: Replace mock calls with real API endpoints
2. **Environment Variables**: Set `NEXT_PUBLIC_API_URL`
3. **Authentication**: Implement JWT or session-based auth
4. **File Upload**: Configure cloud storage for documents

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is part of the BlockHire employment verification system.
