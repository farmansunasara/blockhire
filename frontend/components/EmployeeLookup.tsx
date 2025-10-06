"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { 
  Search, 
  User, 
  Hash, 
  CheckCircle, 
  AlertCircle, 
  Loader2,
  Eye,
  Download
} from "lucide-react"
import { UserProfile, VerificationResult } from "@/types/api"
import { apiService } from "@/services/api"

interface EmployeeLookupProps {
  mode: 'authorize' | 'verify'
  onEmployeeFound?: (employee: UserProfile) => void
  onVerificationResult?: (result: VerificationResult) => void
  prefilledDocHash?: string | null
}

export default function EmployeeLookup({ 
  mode, 
  onEmployeeFound, 
  onVerificationResult,
  prefilledDocHash
}: EmployeeLookupProps) {
  const [empId, setEmpId] = useState("")
  const [userHash, setUserHash] = useState("")
  const [docHash, setDocHash] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const [success, setSuccess] = useState("")
  const [employee, setEmployee] = useState<UserProfile | null>(null)
  const [verificationResult, setVerificationResult] = useState<VerificationResult | null>(null)

  // Set prefilled document hash when provided
  useEffect(() => {
    if (prefilledDocHash && mode === 'verify') {
      setDocHash(prefilledDocHash)
    }
  }, [prefilledDocHash, mode])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError("")
    setSuccess("")
    setEmployee(null)
    setVerificationResult(null)

    try {
      if (mode === 'authorize') {
        // Authorization flow
        if (!empId || !userHash) {
          setError("Please enter both Employee ID and User Hash")
          return
        }

        const response = await apiService.authorizeEmployee({ empId, userHash })
        
        if (response.success) {
          setSuccess("Employee authorized successfully!")
          // Fetch employee details
          const detailsResponse = await apiService.getEmployeeDetails({ empId, userHash })
          if (detailsResponse.success && detailsResponse.data) {
            setEmployee(detailsResponse.data)
            onEmployeeFound?.(detailsResponse.data)
          }
        } else {
          setError(response.error || "Failed to authorize employee")
        }
      } else {
        // Verification flow
        if (!empId || !docHash) {
          setError("Please enter both Employee ID and Document Hash")
          return
        }

        const response = await apiService.verifyDocument({ empId, docHash })
        
        if (response.success && response.data) {
          setVerificationResult(response.data)
          onVerificationResult?.(response.data)
          
          if (response.data.isValid) {
            setSuccess("Document verified successfully!")
          } else {
            setError("Document verification failed - document may be tampered")
          }
        } else {
          setError(response.error || "Verification failed")
        }
      }
    } catch (error) {
      setError("An error occurred. Please try again.")
      console.error("Lookup error:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const resetForm = () => {
    setEmpId("")
    setUserHash("")
    setDocHash("")
    setError("")
    setSuccess("")
    setEmployee(null)
    setVerificationResult(null)
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Search className="mr-2" size={20} />
            {mode === 'authorize' ? 'Authorize Employee' : 'Verify Document'}
          </CardTitle>
          <CardDescription>
            {mode === 'authorize' 
              ? 'Enter employee credentials to grant access to their records'
              : 'Enter employee ID and document hash to verify authenticity'
            }
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="empId">Employee ID *</Label>
              <Input
                id="empId"
                value={empId}
                onChange={(e) => setEmpId(e.target.value)}
                placeholder="Enter employee ID"
                required
                className="font-mono"
              />
            </div>

            {mode === 'authorize' ? (
              <div>
                <Label htmlFor="userHash">User Hash *</Label>
                <Input
                  id="userHash"
                  value={userHash}
                  onChange={(e) => setUserHash(e.target.value)}
                  placeholder="Enter user hash"
                  required
                  className="font-mono text-sm"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Get this from the employee's credentials
                </p>
              </div>
            ) : (
              <div>
                <Label htmlFor="docHash">Document Hash *</Label>
                <Input
                  id="docHash"
                  value={docHash}
                  onChange={(e) => setDocHash(e.target.value)}
                  placeholder="Enter document hash"
                  required
                  className="font-mono text-sm"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Get this from the document's hash value
                </p>
              </div>
            )}

            {error && (
              <Alert className="border-red-200 bg-red-50">
                <AlertCircle className="h-4 w-4 text-red-600" />
                <AlertDescription className="text-red-800">
                  {error}
                </AlertDescription>
              </Alert>
            )}

            {success && (
              <Alert className="border-green-200 bg-green-50">
                <CheckCircle className="h-4 w-4 text-green-600" />
                <AlertDescription className="text-green-800">
                  {success}
                </AlertDescription>
              </Alert>
            )}

            <div className="flex space-x-3">
              <Button 
                type="submit" 
                disabled={isLoading}
                className="flex-1"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    {mode === 'authorize' ? 'Authorizing...' : 'Verifying...'}
                  </>
                ) : (
                  <>
                    <Search className="mr-2 h-4 w-4" />
                    {mode === 'authorize' ? 'Authorize' : 'Verify'}
                  </>
                )}
              </Button>
              
              {(employee || verificationResult) && (
                <Button 
                  type="button" 
                  variant="outline" 
                  onClick={resetForm}
                >
                  Reset
                </Button>
              )}
            </div>
          </form>
        </CardContent>
      </Card>

      {/* Employee Details Display */}
      {employee && (
        <Card className="border-green-200 bg-green-50">
          <CardHeader>
            <CardTitle className="flex items-center text-green-800">
              <User className="mr-2" size={20} />
              Employee Details
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label className="text-sm font-medium text-gray-700">Name</Label>
                <p className="text-lg">{employee.firstName} {employee.lastName}</p>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-700">Email</Label>
                <p className="text-lg">{employee.email}</p>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-700">Designation</Label>
                <p className="text-lg">{employee.jobDesignation}</p>
              </div>
              <div>
                <Label className="text-sm font-medium text-gray-700">Department</Label>
                <p className="text-lg">{employee.department}</p>
              </div>
            </div>
            
            <div className="pt-4 border-t border-green-200">
              <div className="flex space-x-2">
                <Button size="sm" variant="outline" className="flex items-center">
                  <Eye className="mr-2 h-4 w-4" />
                  View Full Profile
                </Button>
                <Button size="sm" variant="outline" className="flex items-center">
                  <Download className="mr-2 h-4 w-4" />
                  Download Documents
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Verification Result Display */}
      {verificationResult && (
        <Card className={`border-2 ${verificationResult.isValid ? 'border-green-200 bg-green-50' : 'border-red-200 bg-red-50'}`}>
          <CardHeader>
            <CardTitle className={`flex items-center ${verificationResult.isValid ? 'text-green-800' : 'text-red-800'}`}>
              {verificationResult.isValid ? (
                <CheckCircle className="mr-2" size={20} />
              ) : (
                <AlertCircle className="mr-2" size={20} />
              )}
              Verification Result
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className={`text-lg font-medium ${verificationResult.isValid ? 'text-green-800' : 'text-red-800'}`}>
              {verificationResult.message}
            </p>
            
            {verificationResult.isValid && verificationResult.employeeDetails && (
              <div className="mt-4 space-y-2">
                <p className="text-sm text-gray-600">
                  <strong>Employee:</strong> {verificationResult.employeeDetails.firstName} {verificationResult.employeeDetails.lastName}
                </p>
                <p className="text-sm text-gray-600">
                  <strong>Department:</strong> {verificationResult.employeeDetails.department}
                </p>
                <p className="text-sm text-gray-600">
                  <strong>Verified on:</strong> {new Date(verificationResult.verificationDate).toLocaleString()}
                </p>
              </div>
            )}
            
            {verificationResult.isValid && verificationResult.downloadLink && (
              <div className="mt-4">
                <Button 
                  className="flex items-center"
                  onClick={async () => {
                    try {
                      // Extract docHash from downloadLink or use the prefilledDocHash
                      const docHash = prefilledDocHash || verificationResult.downloadLink?.split('/').pop()
                      if (docHash) {
                        // Import and use the API service for proper authentication
                        const { apiService } = await import('../services/api')
                        const result = await apiService.downloadDocument(docHash)
                        if (!result.success) {
                          alert(`Download failed: ${result.error}`)
                        }
                      }
                    } catch (error) {
                      console.error('Download error:', error)
                      alert(`Download error: ${error}`)
                    }
                  }}
                >
                  <Download className="mr-2 h-4 w-4" />
                  Download Document
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  )
}
