"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { ChevronRight, Home } from "lucide-react"

interface BreadcrumbItem {
  label: string
  href: string
}

export default function Breadcrumbs() {
  const pathname = usePathname()
  
  const getBreadcrumbs = (): BreadcrumbItem[] => {
    const paths = pathname.split('/').filter(Boolean)
    const breadcrumbs: BreadcrumbItem[] = [{ label: 'Home', href: '/' }]
    
    let currentPath = ''
    paths.forEach((path, index) => {
      currentPath += `/${path}`
      
      let label = path.charAt(0).toUpperCase() + path.slice(1)
      
      // Custom labels for specific routes
      if (path === 'profile') {
        label = 'Profile'
      } else if (path === 'edit') {
        label = 'Edit Profile'
      } else if (path === 'info') {
        label = 'Profile Info'
      } else if (path === 'verify') {
        label = 'Verify Document'
      } else if (path === 'issuer') {
        label = 'Issuer Portal'
      } else if (path === 'login') {
        label = 'Login'
      }
      
      breadcrumbs.push({
        label,
        href: currentPath
      })
    })
    
    return breadcrumbs
  }
  
  const breadcrumbs = getBreadcrumbs()
  
  // Don't show breadcrumbs on home page
  if (pathname === '/') return null
  
  return (
    <nav className="breadcrumbs" aria-label="Breadcrumb">
      <ol className="flex items-center space-x-2 text-sm text-gray-600">
        {breadcrumbs.map((breadcrumb, index) => (
          <li key={breadcrumb.href} className="flex items-center">
            {index > 0 && (
              <ChevronRight className="h-4 w-4 mx-2 text-gray-400" />
            )}
            {index === breadcrumbs.length - 1 ? (
              <span className="text-gray-900 font-medium" aria-current="page">
                {breadcrumb.label}
              </span>
            ) : (
              <Link 
                href={breadcrumb.href}
                className="hover:text-blue-600 transition-colors duration-200"
              >
                {breadcrumb.label}
              </Link>
            )}
          </li>
        ))}
      </ol>
    </nav>
  )
}
