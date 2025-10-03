"use client"

import type React from "react"
import Layout from "../../../components/Layout"
import ProtectedRoute from "../../../components/ProtectedRoute"
import { useState, useEffect } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { useRouter } from "next/navigation"
import { useAuth } from "../../../contexts/AuthContext"
import { ProfileFormData, DocumentRecord } from "@/types/api"
import { apiService } from "@/services/api"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { CheckCircle, AlertCircle, Upload, FileText, Hash } from "lucide-react"

// Validation schema
const profileSchema = z.object({
  firstName: z.string().min(2, "First name must be at least 2 characters"),
  lastName: z.string().min(2, "Last name must be at least 2 characters"),
  dateOfBirth: z.string().min(1, "Date of birth is required"),
  mobile: z.string().min(10, "Mobile number must be at least 10 digits"),
  address: z.string().min(10, "Address must be at least 10 characters"),
  jobDesignation: z.string().min(2, "Job designation is required"),
  department: z.string().min(2, "Department is required"),
})

export default function ProfileEditPage() {
  const router = useRouter()
  const { userProfile, credentials, refreshProfile } = useAuth()
  const [step, setStep] = useState<"personal" | "contact" | "employment">("personal")
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isHashing, setIsHashing] = useState(false)
  const [txStatus, setTxStatus] = useState<string>("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null)
  const [documentHistory, setDocumentHistory] = useState<DocumentRecord[]>([])

  const form = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    defaultValues: {
      firstName: "",
      lastName: "",
      dateOfBirth: "",
      mobile: "",
      address: "",
      jobDesignation: "",
      department: "",
    },
  })

  const { formState: { errors, isValid }, watch, setValue } = form
  const watchedValues = watch()

  useEffect(() => {
    // Load data from AuthContext or localStorage
    const profileData = userProfile || JSON.parse(localStorage.getItem("profile") || "{}")
    
    if (profileData) {
      // Reset form with saved data
      Object.keys(profileData).forEach(key => {
        if (key in profileData && key !== "documentHash" && key !== "userHash" && key !== "empId") {
          setValue(key as keyof ProfileFormData, profileData[key])
        }
      })
    }

    // Load document history
    const savedDocs = localStorage.getItem("documentHistory")
    if (savedDocs) {
      setDocumentHistory(JSON.parse(savedDocs))
    }
  }, [setValue, userProfile])

  const onNext = () => {
    if (step === "personal") {
      // Validate personal fields before proceeding
      const personalFields = ["firstName", "lastName", "dateOfBirth"]
      const hasErrors = personalFields.some(field => errors[field as keyof ProfileFormData])
      if (!hasErrors) setStep("contact")
    } else if (step === "contact") {
      // Validate contact fields before proceeding
      const contactFields = ["mobile", "address"]
      const hasErrors = contactFields.some(field => errors[field as keyof ProfileFormData])
      if (!hasErrors) setStep("employment")
    }
  }

  const onSave = async (data: ProfileFormData) => {
    setIsSubmitting(true)
    setMessage(null)
    
    try {
      // Update profile via API
      const response = await apiService.updateProfile(data)
      
      console.log("Profile update response:", response)
      
      if (response.success && response.data) {
        setMessage({ type: "success", text: "Profile updated successfully!" })
        setTxStatus("Profile saved to database")
        
        // Try to refresh profile, but don't fail if it doesn't work
        try {
          await refreshProfile()
        } catch (refreshError) {
          console.warn("Profile refresh failed, but update was successful:", refreshError)
        }
        
        // Navigate to profile view after successful save
        setTimeout(() => {
          router.push("/profile/info")
        }, 1500) // Give user time to see success message
      } else {
        console.log("Profile update failed:", response)
        throw new Error(response.error || "Failed to update profile")
      }
    } catch (error) {
      console.error("Error saving profile:", error)
      setMessage({ type: "error", text: "Failed to save profile. Please try again." })
    } finally {
      setIsSubmitting(false)
    }
  }

  const onFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    
    if (file.type !== "application/pdf") {
      setMessage({ type: "error", text: "Please select a PDF file" })
      return
    }
    
    setSelectedFile(file)
    setIsHashing(true)
    setMessage(null)
    
    try {
      // Upload document via API
      const response = await apiService.uploadDocument(file)
      
      if (response.success && response.data) {
        const documentData = response.data
        
        // Check if this is an update or new upload
        const isUpdate = documentHistory.some(doc => doc.docHash === documentData.docHash)
        
        // Update document history
        if (isUpdate) {
          // Replace existing document in history
          const updatedHistory = documentHistory.map(doc => 
            doc.docHash === documentData.docHash ? documentData : doc
          )
          setDocumentHistory(updatedHistory)
          // Update localStorage
          localStorage.setItem("documentHistory", JSON.stringify(updatedHistory))
          setMessage({ type: "success", text: "Document updated successfully!" })
        } else {
          // Add new document to history
          const newHistory = [...documentHistory, documentData]
          setDocumentHistory(newHistory)
          // Update localStorage
          localStorage.setItem("documentHistory", JSON.stringify(newHistory))
          setMessage({ type: "success", text: "Document uploaded successfully!" })
        }
      } else {
        throw new Error(response.error || "Failed to upload document")
      }
    } catch (error) {
      console.error("Error uploading file:", error)
      
      // Handle specific error cases
      let errorMessage = "Failed to upload file. Please try again."
      
      if (error instanceof Error) {
        const errorText = error.message.toLowerCase()
        
        if (errorText.includes('already exists') && errorText.includes('another user')) {
          errorMessage = "This document belongs to another user and cannot be uploaded."
        } else if (errorText.includes('already exists') || errorText.includes('duplicate')) {
          errorMessage = "This document has already been uploaded. Each document must be unique."
        } else if (errorText.includes('file too large')) {
          errorMessage = "File is too large. Please choose a smaller file."
        } else if (errorText.includes('invalid file type')) {
          errorMessage = "Invalid file type. Please upload a PDF file."
        } else if (errorText.includes('validation failed')) {
          errorMessage = "Document validation failed. Please check the file and try again."
        }
      }
      
      setMessage({ type: "error", text: errorMessage })
    } finally {
      setIsHashing(false)
    }
  }

  const issueRecord = async () => {
    const documentHash = localStorage.getItem("documentHash")
    const employeeId = credentials?.empId
    
    if (!documentHash || !employeeId) {
      setMessage({ type: "error", text: "Upload a document and ensure you have valid credentials" })
      return
    }
    
    setTxStatus("Issuing record to blockchain...")
    setMessage(null)
    
    setTimeout(() => {
      const txHash = "0x" + Math.random().toString(16).slice(2).padEnd(64, "0").slice(0, 64)
      setTxStatus(`Record issued successfully! Transaction: ${txHash}`)
      setMessage({ type: "success", text: "Record issued to blockchain successfully!" })
      
      // Save mapping for verification demo
      const records = JSON.parse(localStorage.getItem("blockchainRecords") || "{}")
      records[employeeId] = documentHash
      localStorage.setItem("blockchainRecords", JSON.stringify(records))
    }, 2000)
  }

  const getProgressPercentage = () => {
    const steps = ["personal", "contact", "employment"]
    const currentStepIndex = steps.indexOf(step)
    return ((currentStepIndex + 1) / steps.length) * 100
  }

  return (
    <ProtectedRoute>
      <Layout>
        <div className="container max-w-4xl mx-auto py-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold">Edit Profile</h1>
            <p className="text-gray-600 mt-2">Complete your profile information step by step</p>
          </div>

          {/* Progress Bar */}
          <div className="mb-8">
            <div className="flex justify-between text-sm text-gray-600 mb-2">
              <span>Step {step === "personal" ? 1 : step === "contact" ? 2 : 3} of 3</span>
              <span>{Math.round(getProgressPercentage())}% Complete</span>
            </div>
            <Progress value={getProgressPercentage()} className="h-2" />
          </div>

          {/* Step Navigation */}
          <div className="flex space-x-1 mb-8 border-b">
            {[
              { id: "personal", label: "Personal Info", icon: "👤" },
              { id: "contact", label: "Contact Details", icon: "📞" },
              { id: "employment", label: "Employment", icon: "💼" },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setStep(tab.id as any)}
                className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
                  step === tab.id
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700"
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>

          {/* Messages */}
          {message && (
            <Alert className={`mb-6 ${message.type === "success" ? "border-green-200 bg-green-50" : "border-red-200 bg-red-50"}`}>
              {message.type === "success" ? (
                <CheckCircle className="h-4 w-4 text-green-600" />
              ) : (
                <AlertCircle className="h-4 w-4 text-red-600" />
              )}
              <AlertDescription className={message.type === "success" ? "text-green-800" : "text-red-800"}>
                {message.text}
              </AlertDescription>
            </Alert>
          )}

          <form onSubmit={form.handleSubmit(onSave)}>
            {/* Personal Information Step */}
            {step === "personal" && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <span className="mr-2">👤</span>
                    Personal Information
                  </CardTitle>
                  <CardDescription>
                    Tell us about yourself - this information will be used for verification
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <Label htmlFor="firstName">First Name *</Label>
                      <Input
                        id="firstName"
                        {...form.register("firstName")}
                        className={errors.firstName ? "border-red-500" : ""}
                        placeholder="Enter your first name"
                      />
                      {errors.firstName && (
                        <p className="text-red-500 text-sm mt-1">{errors.firstName.message}</p>
                      )}
                    </div>
                    <div>
                      <Label htmlFor="lastName">Last Name *</Label>
                      <Input
                        id="lastName"
                        {...form.register("lastName")}
                        className={errors.lastName ? "border-red-500" : ""}
                        placeholder="Enter your last name"
                      />
                      {errors.lastName && (
                        <p className="text-red-500 text-sm mt-1">{errors.lastName.message}</p>
                      )}
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="dateOfBirth">Date of Birth *</Label>
                    <Input
                      id="dateOfBirth"
                      type="date"
                      {...form.register("dateOfBirth")}
                      className={errors.dateOfBirth ? "border-red-500" : ""}
                    />
                    {errors.dateOfBirth && (
                      <p className="text-red-500 text-sm mt-1">{errors.dateOfBirth.message}</p>
                    )}
                  </div>

                  <div className="flex justify-end">
                    <Button type="button" onClick={onNext} className="px-8">
                      Next Step
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Contact Information Step */}
            {step === "contact" && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <span className="mr-2">📞</span>
                    Contact Details
                  </CardTitle>
                  <CardDescription>
                    How can we reach you? This information is crucial for verification
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div>
                    <Label htmlFor="mobile">Mobile Number *</Label>
                    <Input
                      id="mobile"
                      {...form.register("mobile")}
                      className={errors.mobile ? "border-red-500" : ""}
                      placeholder="Enter your mobile number"
                    />
                    {errors.mobile && (
                      <p className="text-red-500 text-sm mt-1">{errors.mobile.message}</p>
                    )}
                  </div>

                  {/* Email Display (Read-only) */}
                  {credentials && (
                    <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <Label className="text-sm font-medium text-blue-800">Email Address</Label>
                        <Badge variant="secondary" className="text-xs">Immutable</Badge>
                      </div>
                      <code className="text-sm font-mono text-blue-700 bg-white px-2 py-1 rounded">
                        {credentials.email}
                      </code>
                      <p className="text-xs text-blue-600 mt-1">
                        This email was set during registration and cannot be changed
                      </p>
                    </div>
                  )}

                  <div>
                    <Label htmlFor="address">Address *</Label>
                    <Input
                      id="address"
                      {...form.register("address")}
                      className={errors.address ? "border-red-500" : ""}
                      placeholder="Enter your full address"
                    />
                    {errors.address && (
                      <p className="text-red-500 text-sm mt-1">{errors.address.message}</p>
                    )}
                  </div>

                  <div className="flex justify-between">
                    <Button type="button" variant="outline" onClick={() => setStep("personal")}>
                      Previous
                    </Button>
                    <Button type="button" onClick={onNext} className="px-8">
                      Next Step
                    </Button>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Employment Information Step */}
            {step === "employment" && (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <span className="mr-2">💼</span>
                    Employment Information
                  </CardTitle>
                  <CardDescription>
                    Your employment details and document verification
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <Label htmlFor="jobDesignation">Job Designation *</Label>
                      <Input
                        id="jobDesignation"
                        {...form.register("jobDesignation")}
                        className={errors.jobDesignation ? "border-red-500" : ""}
                        placeholder="e.g., Software Engineer"
                      />
                      {errors.jobDesignation && (
                        <p className="text-red-500 text-sm mt-1">{errors.jobDesignation.message}</p>
                      )}
                    </div>
                    <div>
                      <Label htmlFor="department">Department *</Label>
                      <Input
                        id="department"
                        {...form.register("department")}
                        className={errors.department ? "border-red-500" : ""}
                        placeholder="e.g., Engineering"
                      />
                      {errors.department && (
                        <p className="text-red-500 text-sm mt-1">{errors.department.message}</p>
                      )}
                    </div>
                  </div>

                  {/* Employee ID Display (Read-only) */}
                  {credentials && (
                    <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <Label className="text-sm font-medium text-blue-800">Employee ID</Label>
                        <Badge variant="secondary" className="text-xs">Auto-generated</Badge>
                      </div>
                      <code className="text-sm font-mono text-blue-700 bg-white px-2 py-1 rounded">
                        {credentials.empId}
                      </code>
                      <p className="text-xs text-blue-600 mt-1">
                        This ID is automatically generated and cannot be changed
                      </p>
                    </div>
                  )}

                  {/* Document Upload Section */}
                  <div className="border-t pt-6">
                    <h3 className="text-lg font-medium mb-4 flex items-center">
                      <FileText className="mr-2" size={20} />
                      Document Verification
                    </h3>
                    
                    <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                      <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                      <div className="text-sm text-gray-600">
                        <label htmlFor="file-upload" className="cursor-pointer">
                          <span className="font-medium text-blue-600 hover:text-blue-500">
                            Upload a PDF document
                          </span>
                          <input
                            id="file-upload"
                            type="file"
                            accept=".pdf"
                            onChange={onFile}
                            className="sr-only"
                          />
                        </label>
                        <p className="mt-1">or drag and drop</p>
                        <p className="text-xs text-gray-500 mt-2">PDF files only, max 10MB</p>
                      </div>
                    </div>

                    {isHashing && (
                      <div className="flex items-center justify-center mt-4 text-blue-600">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-2"></div>
                        Computing SHA-256 hash...
                      </div>
                    )}

                    {/* Document History Display */}
                    <div className="mt-6">
                      <h4 className="text-md font-medium mb-3 text-gray-800">Uploaded Documents</h4>
                      {documentHistory.length > 0 ? (
                        <div className="space-y-3">
                          {documentHistory.map((doc, index) => (
                            <div key={doc.docHash || index} className="p-3 bg-gray-50 border border-gray-200 rounded-lg">
                              <div className="flex items-center justify-between">
                                <div className="flex items-center">
                                  <FileText className="h-4 w-4 text-blue-600 mr-2" />
                                  <div>
                                    <p className="text-sm font-medium text-gray-800">{doc.fileName}</p>
                                    <p className="text-xs text-gray-500">
                                      {doc.fileSize ? `${(doc.fileSize / 1024).toFixed(1)} KB` : 'Unknown size'} • 
                                      {doc.fileType?.toUpperCase() || 'PDF'}
                                    </p>
                                  </div>
                                </div>
                                <div className="flex items-center">
                                  {doc.isOriginal && (
                                    <Badge variant="default" className="text-xs mr-2">Original</Badge>
                                  )}
                                  <CheckCircle className="h-4 w-4 text-green-600" />
                                </div>
                              </div>
                              <div className="mt-2">
                                <p className="text-xs text-gray-600 font-mono break-all">
                                  Hash: {doc.docHash}
                                </p>
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg text-center">
                          <FileText className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                          <p className="text-sm text-gray-600">No documents uploaded yet</p>
                          <p className="text-xs text-gray-500 mt-1">Upload a PDF document above to get started</p>
                        </div>
                      )}
                    </div>

                    {localStorage.getItem("documentHash") && (
                      <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
                        <div className="flex items-center mb-2">
                          <Hash className="h-4 w-4 text-green-600 mr-2" />
                          <span className="text-sm font-medium text-green-800">Document Hash Generated</span>
                        </div>
                        <code className="text-xs text-green-700 break-all block">
                          {localStorage.getItem("documentHash")}
                        </code>
                      </div>
                    )}
                  </div>

                  <div className="flex justify-between">
                    <Button type="button" variant="outline" onClick={() => setStep("contact")}>
                      Previous
                    </Button>
                    <Button type="submit" disabled={isSubmitting} className="px-8">
                      {isSubmitting ? "Saving..." : "Save Profile"}
                    </Button>
                  </div>

                  {/* Blockchain Issue Section */}
                  <div className="border-t pt-6">
                    <h3 className="text-lg font-medium mb-4">Blockchain Record</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Issue your employment record to the blockchain for immutable verification
                    </p>
                    <Button
                      type="button"
                      variant="secondary"
                      onClick={issueRecord}
                      disabled={!credentials?.empId || !localStorage.getItem("documentHash") || txStatus.includes("Issuing")}
                      className="w-full"
                    >
                      {txStatus.includes("Issuing") ? "Issuing to Blockchain..." : "Issue Record to Blockchain"}
                    </Button>

                    {txStatus && (
                      <Alert className={`mt-4 ${txStatus.includes("successfully") ? "border-green-200 bg-green-50" : "border-blue-200 bg-blue-50"}`}>
                        <AlertCircle className="h-4 w-4 text-blue-600" />
                        <AlertDescription className="text-blue-800">
                          {txStatus}
                        </AlertDescription>
                      </Alert>
                    )}
                  </div>
                </CardContent>
              </Card>
            )}
          </form>
        </div>
      </Layout>
    </ProtectedRoute>
  )
}
