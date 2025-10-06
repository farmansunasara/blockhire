"use client"

import React, { useState } from "react"
import { MobileInput } from "@/components/ui/mobile-input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { CheckCircle, XCircle } from "lucide-react"

export default function MobileValidationDemo() {
  const [mobile, setMobile] = useState("")
  const [validationResult, setValidationResult] = useState<{
    isValid: boolean
    error?: string
  } | null>(null)

  const validateMobile = (value: string) => {
    // Simple validation logic
    const cleaned = value.replace(/[^\d+]/g, '')
    
    if (!cleaned) {
      setValidationResult({ isValid: false, error: "Mobile number is required" })
      return
    }
    
    if (cleaned.startsWith('+')) {
      const digits = cleaned.substring(1)
      if (digits.length < 10) {
        setValidationResult({ isValid: false, error: "International mobile number must be at least 10 digits" })
        return
      }
      if (digits.length > 15) {
        setValidationResult({ isValid: false, error: "International mobile number cannot exceed 15 digits" })
        return
      }
      if (!/^[1-9]/.test(digits)) {
        setValidationResult({ isValid: false, error: "Mobile number cannot start with 0" })
        return
      }
    } else {
      if (cleaned.length < 10) {
        setValidationResult({ isValid: false, error: "Mobile number must be at least 10 digits" })
        return
      }
      if (cleaned.length > 15) {
        setValidationResult({ isValid: false, error: "Mobile number cannot exceed 15 digits" })
        return
      }
      if (!/^[1-9]/.test(cleaned)) {
        setValidationResult({ isValid: false, error: "Mobile number cannot start with 0" })
        return
      }
    }
    
    const phoneRegex = /^[\+]?[1-9][\d]{9,14}$/
    if (!phoneRegex.test(cleaned)) {
      setValidationResult({ isValid: false, error: "Please enter a valid mobile number" })
      return
    }
    
    setValidationResult({ isValid: true })
  }

  const handleMobileChange = (value: string) => {
    setMobile(value)
    validateMobile(value)
  }

  const testCases = [
    { input: "1234567890", expected: "Valid" },
    { input: "+1234567890", expected: "Valid" },
    { input: "123456789", expected: "Invalid - Too short" },
    { input: "0123456789", expected: "Invalid - Starts with 0" },
    { input: "1234567890123456", expected: "Invalid - Too long" },
    { input: "abc123456789", expected: "Invalid - Contains letters" },
  ]

  return (
    <div className="container max-w-4xl mx-auto py-8">
      <Card>
        <CardHeader>
          <CardTitle>Mobile Number Validation Demo</CardTitle>
          <CardDescription>
            Test the mobile number validation with different inputs
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Live Validation Demo */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Live Validation</h3>
            <MobileInput
              label="Mobile Number"
              value={mobile}
              onValueChange={handleMobileChange}
              error={validationResult?.error}
              helperText="Enter a mobile number to see validation in action"
            />
            
            {validationResult && (
              <div className="flex items-center space-x-2">
                {validationResult.isValid ? (
                  <>
                    <CheckCircle className="h-5 w-5 text-green-600" />
                    <Badge variant="default" className="bg-green-100 text-green-800">
                      Valid Mobile Number
                    </Badge>
                  </>
                ) : (
                  <>
                    <XCircle className="h-5 w-5 text-red-600" />
                    <Badge variant="destructive">
                      Invalid: {validationResult.error}
                    </Badge>
                  </>
                )}
              </div>
            )}
          </div>

          {/* Test Cases */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Test Cases</h3>
            <div className="grid gap-2">
              {testCases.map((testCase, index) => (
                <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                  <code className="text-sm font-mono">{testCase.input}</code>
                  <Badge variant={testCase.expected === "Valid" ? "default" : "secondary"}>
                    {testCase.expected}
                  </Badge>
                </div>
              ))}
            </div>
          </div>

          {/* Validation Rules */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Validation Rules</h3>
            <ul className="space-y-2 text-sm">
              <li>• Must be 10-15 digits long</li>
              <li>• Cannot start with 0</li>
              <li>• International format supported (+1234567890)</li>
              <li>• Only digits and + allowed</li>
              <li>• Automatically formats as you type</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
