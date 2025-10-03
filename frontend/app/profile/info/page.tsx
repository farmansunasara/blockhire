"use client"

import Layout from "../../../components/Layout"
import ProtectedRoute from "../../../components/ProtectedRoute"
import { useAuth } from "../../../contexts/AuthContext"
import Link from "next/link"
import { useEffect, useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { 
  User, 
  Mail, 
  Phone, 
  MapPin, 
  Briefcase, 
  Building, 
  Hash, 
  Copy, 
  CheckCircle, 
  Edit3,
  Calendar,
  IdCard,
  QrCode,
  FileText,
  AlertCircle
} from "lucide-react"
import CredentialsDisplay from "@/components/CredentialsDisplay"
import DocumentHistory from "@/components/DocumentHistory"
import { UserProfile, DocumentRecord } from "@/types/api"

// Remove duplicate interface - using imported one

export default function ProfileInfoPage() {
  const { user, userProfile, credentials, loading } = useAuth()
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [documents, setDocuments] = useState<DocumentRecord[]>([])
  const [copied, setCopied] = useState(false)

  // Debug logging
  console.log("ProfileInfoPage - user:", user)
  console.log("ProfileInfoPage - userProfile:", userProfile)
  console.log("ProfileInfoPage - credentials:", credentials)
  console.log("ProfileInfoPage - loading:", loading)

  useEffect(() => {
    // Only run when AuthContext is done loading
    if (loading) return

    // Use data from AuthContext if available, otherwise fallback to localStorage
    if (userProfile) {
      console.log("Loading profile from AuthContext:", userProfile)
      setProfile(userProfile)
    } else {
      // Try both localStorage keys for compatibility
      const savedProfile = localStorage.getItem("userProfile") || localStorage.getItem("profile")
      if (savedProfile) {
        console.log("Loading profile from localStorage:", JSON.parse(savedProfile))
        setProfile(JSON.parse(savedProfile))
      } else {
        console.log("No profile data found")
      }
    }
    
    // Load document history from API instead of localStorage
    const loadDocumentHistory = async () => {
      try {
        const response = await apiService.getDocumentHistory()
        if (response.success && response.data) {
          console.log("Loaded document history from API:", response.data)
          setDocuments(response.data)
        } else {
          console.log("No document history found or API error")
          setDocuments([])
        }
      } catch (error) {
        console.error("Error loading document history:", error)
        setDocuments([])
      }
    }
    
    // Only fetch if user is authenticated
    if (user) {
      loadDocumentHistory()
    } else {
      setDocuments([])
    }
  }, [userProfile, loading, user])

  const copyHash = async () => {
    const documentHash = localStorage.getItem("documentHash")
    if (documentHash) {
      try {
        await navigator.clipboard.writeText(documentHash)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
      } catch {
        alert("Unable to copy hash")
      }
    }
  }

  const getCompletionPercentage = () => {
    if (!profile) return 0
    const fields = [
      profile.firstName,
      profile.lastName,
      profile.dateOfBirth,
      profile.mobile,
      profile.email,
      profile.address,
      profile.jobDesignation,
      profile.department,
    ]
    const filledFields = fields.filter(field => field && field.trim() !== "").length
    return Math.round((filledFields / fields.length) * 100)
  }

  const formatDate = (dateString: string) => {
    if (!dateString) return "-"
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    })
  }

  if (loading) {
    return (
      <ProtectedRoute>
        <Layout>
          <div className="container max-w-4xl mx-auto py-8">
            <div className="flex items-center justify-center h-64">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          </div>
        </Layout>
      </ProtectedRoute>
    )
  }

  // If not loading but no user, show login prompt
  if (!user && !userProfile && !credentials) {
    return (
      <ProtectedRoute>
        <Layout>
          <div className="container max-w-4xl mx-auto py-8">
            <Card className="text-center py-12">
              <div className="mx-auto w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-6">
                <User className="w-12 h-12 text-gray-400" />
              </div>
              <h2 className="text-2xl font-semibold mb-4">Please Login First</h2>
              <p className="text-gray-600 mb-6 max-w-md mx-auto">
                You need to login or register to view your profile
              </p>
              <Link href="/login">
                <Button size="lg">
                  Go to Login
                </Button>
              </Link>
            </Card>
          </div>
        </Layout>
      </ProtectedRoute>
    )
  }

  return (
    <ProtectedRoute>
      <Layout>
        <div className="container max-w-6xl mx-auto py-8">
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
            <div>
              <h1 className="text-3xl font-bold">Your Profile</h1>
              <p className="text-gray-600 mt-2">View and manage your profile information</p>
            </div>
            <div className="mt-4 sm:mt-0 flex space-x-2">
              <Link href="/profile/edit">
                <Button className="flex items-center">
                  <Edit3 className="mr-2" size={16} />
                  Edit Profile
                </Button>
              </Link>
              <Button 
                variant="outline" 
                onClick={() => {
                  localStorage.clear()
                  window.location.reload()
                }}
                className="text-red-600 border-red-200 hover:bg-red-50"
              >
                Clear Demo Data
              </Button>
            </div>
          </div>

          {!profile ? (
            <Card className="text-center py-12">
              <div className="mx-auto w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-6">
                <User className="w-12 h-12 text-gray-400" />
              </div>
              <h2 className="text-2xl font-semibold mb-4">No Profile Found</h2>
              <p className="text-gray-600 mb-6 max-w-md mx-auto">
                Complete your profile to start using BlockHire's verification services
              </p>
              <Link href="/profile/edit">
                <Button size="lg">
                  <Edit3 className="mr-2" size={16} />
                  Complete Profile
                </Button>
              </Link>
            </Card>
          ) : (
            <div className="space-y-8">
              {/* Credentials Section */}
              {credentials ? (
                <CredentialsDisplay 
                  credentials={credentials} 
                  showQR={true}
                  showWarning={true}
                />
              ) : (
                <Card className="border-amber-200 bg-amber-50">
                  <CardContent className="pt-6">
                    <div className="flex items-center">
                      <AlertCircle className="h-5 w-5 text-amber-600 mr-2" />
                      <span className="text-amber-800">
                        No credentials found. Please complete your profile first.
                      </span>
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Document History Section */}
              <DocumentHistory
                documents={documents}
                onDownload={(docHash) => {
                  // TODO: Implement download functionality
                  console.log("Download document:", docHash)
                }}
                onView={(docHash) => {
                  // TODO: Implement view functionality
                  console.log("View document:", docHash)
                }}
                isLoading={false}
              />
              {/* Profile Completion Status */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <CheckCircle className="mr-2 text-green-600" size={20} />
                    Profile Completion
                  </CardTitle>
                  <CardDescription>
                    Your profile is {getCompletionPercentage()}% complete
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
                    <div 
                      className="bg-green-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${getCompletionPercentage()}%` }}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-600">
                    {getCompletionPercentage() < 100 
                      ? "Complete all fields to unlock full verification features"
                      : "Your profile is complete and ready for verification"
                    }
                  </p>
                </CardContent>
              </Card>

              {/* Personal Information */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <User className="mr-2" size={20} />
                    Personal Information
                  </CardTitle>
                  <CardDescription>
                    Your basic personal details
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div className="space-y-2">
                      <div className="flex items-center text-sm font-medium text-gray-500">
                        <User className="mr-2" size={16} />
                        First Name
                      </div>
                      <p className="text-lg">{profile.firstName || "-"}</p>
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center text-sm font-medium text-gray-500">
                        <User className="mr-2" size={16} />
                        Last Name
                      </div>
                      <p className="text-lg">{profile.lastName || "-"}</p>
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center text-sm font-medium text-gray-500">
                        <Calendar className="mr-2" size={16} />
                        Date of Birth
                      </div>
                      <p className="text-lg">{formatDate(profile.dateOfBirth)}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Contact Information */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Phone className="mr-2" size={20} />
                    Contact Information
                  </CardTitle>
                  <CardDescription>
                    How to reach you
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <div className="flex items-center text-sm font-medium text-gray-500">
                        <Phone className="mr-2" size={16} />
                        Mobile Number
                      </div>
                      <p className="text-lg">{profile.mobile || "-"}</p>
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center text-sm font-medium text-gray-500">
                        <Mail className="mr-2" size={16} />
                        Email Address
                      </div>
                      <p className="text-lg">{profile.email || "-"}</p>
                    </div>
                    <div className="space-y-2 md:col-span-2">
                      <div className="flex items-center text-sm font-medium text-gray-500">
                        <MapPin className="mr-2" size={16} />
                        Address
                      </div>
                      <p className="text-lg">{profile.address || "-"}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Employment Information */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Briefcase className="mr-2" size={20} />
                    Employment Information
                  </CardTitle>
                  <CardDescription>
                    Your professional details
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    <div className="space-y-2">
                      <div className="flex items-center text-sm font-medium text-gray-500">
                        <Briefcase className="mr-2" size={16} />
                        Job Designation
                      </div>
                      <p className="text-lg">{profile.jobDesignation || "-"}</p>
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center text-sm font-medium text-gray-500">
                        <Building className="mr-2" size={16} />
                        Department
                      </div>
                      <p className="text-lg">{profile.department || "-"}</p>
                    </div>
                    <div className="space-y-2">
                      <div className="flex items-center text-sm font-medium text-gray-500">
                        <IdCard className="mr-2" size={16} />
                        Employee ID
                      </div>
                      <p className="text-lg font-mono">{profile.employeeId || "-"}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Document Verification */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Hash className="mr-2" size={20} />
                    Document Verification
                  </CardTitle>
                  <CardDescription>
                    Your immutable document hash for blockchain verification
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {localStorage.getItem("documentHash") ? (
                    <div className="space-y-4">
                      <Alert className="border-green-200 bg-green-50">
                        <CheckCircle className="h-4 w-4 text-green-600" />
                        <AlertDescription className="text-green-800">
                          Document verified and hashed successfully
                        </AlertDescription>
                      </Alert>
                      
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-medium text-gray-500">Document Hash</span>
                          <Badge variant="secondary">SHA-256</Badge>
                        </div>
                        <div className="bg-gray-50 p-4 rounded-lg border">
                          <code className="text-xs text-gray-700 break-all block font-mono">
                            {localStorage.getItem("documentHash")}
                          </code>
                        </div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={copyHash}
                          className="w-full sm:w-auto"
                        >
                          {copied ? (
                            <>
                              <CheckCircle className="mr-2" size={16} />
                              Copied!
                            </>
                          ) : (
                            <>
                              <Copy className="mr-2" size={16} />
                              Copy Hash
                            </>
                          )}
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <div className="text-center py-8">
                      <Hash className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                      <h3 className="text-lg font-medium text-gray-900 mb-2">No Document Hash</h3>
                      <p className="text-gray-600 mb-4">
                        Upload a PDF document to generate an immutable hash for verification
                      </p>
                      <Link href="/profile/edit">
                        <Button>
                          <Edit3 className="mr-2" size={16} />
                          Upload Document
                        </Button>
                      </Link>
                    </div>
                  )}
                </CardContent>
              </Card>

              {/* Quick Actions */}
              <Card>
                <CardHeader>
                  <CardTitle>Quick Actions</CardTitle>
                  <CardDescription>
                    Common profile management tasks
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    <Link href="/profile/edit">
                      <Button variant="outline" className="w-full justify-start">
                        <Edit3 className="mr-2" size={16} />
                        Edit Profile
                      </Button>
                    </Link>
                    <Link href="/verify">
                      <Button variant="outline" className="w-full justify-start">
                        <CheckCircle className="mr-2" size={16} />
                        Verify Records
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </Layout>
    </ProtectedRoute>
  )
}
