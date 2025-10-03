"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { useSearchParams } from "next/navigation"
import Layout from "../../components/Layout"
import EmployeeLookup from "../../components/EmployeeLookup"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { VerificationResult } from "@/types/api"

export default function VerifyPage() {
  const [verificationResult, setVerificationResult] = useState<VerificationResult | null>(null)
  const [prefilledDocHash, setPrefilledDocHash] = useState<string | null>(null)
  const searchParams = useSearchParams()

  useEffect(() => {
    const docHash = searchParams.get('docHash')
    if (docHash) {
      setPrefilledDocHash(docHash)
    }
  }, [searchParams])

  const handleVerificationResult = (result: VerificationResult) => {
    setVerificationResult(result)
  }

  return (
    <Layout>
        <div className="container max-w-4xl mx-auto py-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold">Verify Employment Record</h1>
            <p className="text-gray-600 mt-2">
              Verify the authenticity of an employment record using blockchain technology
            </p>
          </div>

          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Document Verification</CardTitle>
                <CardDescription>
                  Enter employee ID and document hash to verify authenticity
                </CardDescription>
              </CardHeader>
              <CardContent>
                <EmployeeLookup 
                  mode="verify"
                  onVerificationResult={handleVerificationResult}
                  prefilledDocHash={prefilledDocHash}
                />
              </CardContent>
            </Card>

            {verificationResult && (
              <Card className={`border-2 ${
                verificationResult.isValid 
                  ? 'border-green-200 bg-green-50' 
                  : 'border-red-200 bg-red-50'
              }`}>
                <CardHeader>
                  <CardTitle className={verificationResult.isValid ? 'text-green-800' : 'text-red-800'}>
                    Verification Result
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className={`text-lg font-medium ${
                    verificationResult.isValid ? 'text-green-800' : 'text-red-800'
                  }`}>
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
                </CardContent>
              </Card>
            )}

            <Card className="bg-blue-50 border-blue-200">
              <CardHeader>
                <CardTitle className="text-blue-900">How to Get Document Hash</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h4 className="font-medium text-blue-900 mb-2">For Employees:</h4>
                    <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
                      <li>Go to your Profile → View Profile</li>
                      <li>Find your uploaded document in the "Document History" section</li>
                      <li>Click "Copy Hash" next to the document hash</li>
                      <li>Share the hash with the verifier</li>
                    </ol>
                  </div>
                  
                  <div>
                    <h4 className="font-medium text-blue-900 mb-2">For Verifiers:</h4>
                    <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
                      <li>Ask the employee for their Employee ID and Document Hash</li>
                      <li>Enter both values in the form above</li>
                      <li>Click "Verify" to check document authenticity</li>
                      <li>View the verification result</li>
                    </ol>
                  </div>
                  
                  <div className="mt-4 p-4 bg-blue-100 rounded-lg">
                    <p className="text-sm text-blue-800">
                      <strong>Note:</strong> The document hash is a unique fingerprint of the document. 
                      Any change to the document will result in a different hash, making tampering detectable.
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-green-50 border-green-200">
              <CardHeader>
                <CardTitle className="text-green-900">How Verification Works</CardTitle>
              </CardHeader>
              <CardContent>
                <ol className="text-sm text-green-800 space-y-1 list-decimal list-inside">
                  <li>Enter the Employee ID and Document Hash</li>
                  <li>System queries the database for the stored hash</li>
                  <li>Compares the provided hash with the stored hash</li>
                  <li>Returns verification result (Valid/Tampered)</li>
                </ol>
                
                <div className="mt-4 p-4 bg-green-100 rounded-lg">
                  <p className="text-sm text-green-800">
                    <strong>Security:</strong> This verification process ensures document integrity by comparing
                    cryptographic hashes. Only the original document hash is used for verification.
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </Layout>
  )
}