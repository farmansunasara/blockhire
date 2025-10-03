"use client"

import type React from "react"

import { useState } from "react"
import Layout from "../../components/Layout"
import ProtectedRoute from "../../components/ProtectedRoute"
import { useAuth } from "../../contexts/AuthContext"
import EmployeeLookup from "../../components/EmployeeLookup"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { CheckCircle } from "lucide-react"

export default function IssuerPage() {
  const { user } = useAuth()

  return (
    <ProtectedRoute>
      <Layout>
        <div className="container max-w-6xl mx-auto py-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold">Issuer Dashboard</h1>
            <p className="text-gray-600 mt-2">Manage employee authorizations and verifications</p>
          </div>

          <div className="mb-6">
            <Card className="border-green-200 bg-green-50">
              <CardContent className="pt-6">
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
                  <span className="font-medium text-green-800">
                    Authorized Issuer: {user?.email}
                  </span>
                </div>
              </CardContent>
            </Card>
          </div>

          <Tabs defaultValue="authorize" className="space-y-6">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="authorize">Authorize Employee</TabsTrigger>
              <TabsTrigger value="verify">Verify Document</TabsTrigger>
            </TabsList>

            <TabsContent value="authorize" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Employee Authorization</CardTitle>
                  <CardDescription>
                    Grant access to employee records by entering their credentials
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <EmployeeLookup 
                    mode="authorize"
                    onEmployeeFound={(employee) => {
                      console.log("Employee found:", employee)
                    }}
                  />
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="verify" className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Document Verification</CardTitle>
                  <CardDescription>
                    Verify document authenticity using employee ID and document hash
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <EmployeeLookup 
                    mode="verify"
                    onVerificationResult={(result) => {
                      console.log("Verification result:", result)
                    }}
                  />
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          {/* Issuer Guidelines */}
          <Card className="mt-8">
            <CardHeader>
              <CardTitle>Issuer Guidelines</CardTitle>
              <CardDescription>
                Important information for authorized issuers
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm">
                <li className="flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  Verify employee identity before granting authorization
                </li>
                <li className="flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  Ensure document hashes are computed correctly using SHA-256
                </li>
                <li className="flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  Double-check employee ID and user hash for accuracy
                </li>
                <li className="flex items-start">
                  <span className="text-blue-600 mr-2">•</span>
                  Keep authorization records for audit purposes
                </li>
              </ul>

              <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
                <p className="text-sm text-amber-800">
                  <strong>Warning:</strong> Authorizations are permanent records. Once granted, 
                  they cannot be modified or deleted without proper audit trails.
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </Layout>
    </ProtectedRoute>
  )
}
