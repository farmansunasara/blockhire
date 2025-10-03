"use client"

import { usePathname } from "next/navigation"
import { useAuth } from "../contexts/AuthContext"
import { CheckCircle, Circle, User, FileText, Shield, Search } from "lucide-react"

interface NavigationStep {
  id: string
  label: string
  path: string
  icon: React.ReactNode
  completed: boolean
  current: boolean
}

export default function NavigationProgress() {
  const pathname = usePathname()
  const { user, userProfile } = useAuth()
  
  if (!user) return null
  
  const steps: NavigationStep[] = [
    {
      id: 'profile',
      label: 'Profile Setup',
      path: '/profile/edit',
      icon: <User size={16} />,
      completed: userProfile?.isProfileComplete || false,
      current: pathname === '/profile/edit' || pathname === '/profile/info'
    },
    {
      id: 'documents',
      label: 'Document Upload',
      path: '/profile/edit',
      icon: <FileText size={16} />,
      completed: Boolean(userProfile?.docHash),
      current: pathname === '/profile/edit' && Boolean(userProfile?.docHash)
    },
    {
      id: 'verification',
      label: 'Verification',
      path: '/verify',
      icon: <Shield size={16} />,
      completed: false,
      current: pathname === '/verify'
    },
    {
      id: 'issuer',
      label: 'Issuer Portal',
      path: '/issuer',
      icon: <Search size={16} />,
      completed: false,
      current: pathname === '/issuer'
    }
  ]
  
  return (
    <div className="navigation-progress">
      <div className="container">
        <div className="progress-steps">
          {steps.map((step, index) => (
            <div key={step.id} className={`step ${step.completed ? 'completed' : ''} ${step.current ? 'current' : ''}`}>
              <div className="step-icon">
                {step.completed ? (
                  <CheckCircle className="text-green-600" size={20} />
                ) : (
                  <Circle className={step.current ? 'text-blue-600' : 'text-gray-400'} size={20} />
                )}
              </div>
              <div className="step-content">
                <div className="step-label">{step.label}</div>
                <div className="step-status">
                  {step.completed ? 'Completed' : step.current ? 'Current' : 'Pending'}
                </div>
              </div>
              {index < steps.length - 1 && (
                <div className={`step-connector ${step.completed ? 'completed' : ''}`} />
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
