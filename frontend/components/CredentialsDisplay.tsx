"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Copy, CheckCircle, AlertTriangle, QrCode, Share2 } from "lucide-react"
import { UserCredentials } from "@/types/api"

interface CredentialsDisplayProps {
  credentials: UserCredentials
  showQR?: boolean
  showWarning?: boolean
}

export default function CredentialsDisplay({ 
  credentials, 
  showQR = true, 
  showWarning = true 
}: CredentialsDisplayProps) {
  const [copiedField, setCopiedField] = useState<string | null>(null)

  const copyToClipboard = async (text: string, field: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedField(field)
      setTimeout(() => setCopiedField(null), 2000)
    } catch (error) {
      console.error("Failed to copy:", error)
    }
  }

  const shareCredentials = async () => {
    const shareData = {
      title: "BlockHire Credentials",
      text: `Employee ID: ${credentials.empId}\nUser Hash: ${credentials.userHash}`,
      url: window.location.origin
    }

    if (navigator.share) {
      try {
        await navigator.share(shareData)
      } catch (error) {
        console.error("Error sharing:", error)
      }
    } else {
      // Fallback to copying to clipboard
      await copyToClipboard(
        `Employee ID: ${credentials.empId}\nUser Hash: ${credentials.userHash}`,
        'all'
      )
    }
  }

  return (
    <div className="space-y-6">
      {showWarning && (
        <Alert className="border-amber-200 bg-amber-50">
          <AlertTriangle className="h-4 w-4 text-amber-600" />
          <AlertDescription className="text-amber-800">
            <strong>Important:</strong> These credentials are immutable and cannot be changed once generated. 
            Keep them secure and share only with authorized issuers.
          </AlertDescription>
        </Alert>
      )}

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <QrCode className="mr-2" size={20} />
            Your Credentials
          </CardTitle>
          <CardDescription>
            Share these credentials with issuers to grant them access to your employment records
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Employee ID */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-gray-700">Employee ID</label>
              <Badge variant="secondary" className="text-xs">Immutable</Badge>
            </div>
            <div className="flex items-center space-x-2">
              <code className="flex-1 p-3 bg-gray-100 rounded-lg font-mono text-sm break-all">
                {credentials.empId}
              </code>
              <Button
                size="sm"
                variant="outline"
                onClick={() => copyToClipboard(credentials.empId, 'empId')}
                className="shrink-0"
              >
                {copiedField === 'empId' ? (
                  <CheckCircle className="h-4 w-4 text-green-600" />
                ) : (
                  <Copy className="h-4 w-4" />
                )}
              </Button>
            </div>
          </div>

          {/* User Hash */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-gray-700">User Hash</label>
              <Badge variant="secondary" className="text-xs">Immutable</Badge>
            </div>
            <div className="flex items-center space-x-2">
              <code className="flex-1 p-3 bg-gray-100 rounded-lg font-mono text-xs break-all">
                {credentials.userHash}
              </code>
              <Button
                size="sm"
                variant="outline"
                onClick={() => copyToClipboard(credentials.userHash, 'userHash')}
                className="shrink-0"
              >
                {copiedField === 'userHash' ? (
                  <CheckCircle className="h-4 w-4 text-green-600" />
                ) : (
                  <Copy className="h-4 w-4" />
                )}
              </Button>
            </div>
          </div>

          {/* Email */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-sm font-medium text-gray-700">Email Address</label>
              <Badge variant="secondary" className="text-xs">Immutable</Badge>
            </div>
            <div className="flex items-center space-x-2">
              <code className="flex-1 p-3 bg-gray-100 rounded-lg font-mono text-sm">
                {credentials.email}
              </code>
              <Button
                size="sm"
                variant="outline"
                onClick={() => copyToClipboard(credentials.email, 'email')}
                className="shrink-0"
              >
                {copiedField === 'email' ? (
                  <CheckCircle className="h-4 w-4 text-green-600" />
                ) : (
                  <Copy className="h-4 w-4" />
                )}
              </Button>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-3 pt-4 border-t">
            <Button
              onClick={shareCredentials}
              className="flex items-center"
              variant="outline"
            >
              <Share2 className="mr-2" size={16} />
              Share Credentials
            </Button>
            
            {showQR && (
              <Button
                onClick={() => {/* TODO: Implement QR code modal */}}
                className="flex items-center"
                variant="outline"
              >
                <QrCode className="mr-2" size={16} />
                Show QR Code
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Instructions */}
      <Card className="bg-blue-50 border-blue-200">
        <CardContent className="pt-6">
          <h3 className="font-semibold text-blue-900 mb-2">How to use these credentials:</h3>
          <ol className="text-sm text-blue-800 space-y-1 list-decimal list-inside">
            <li>Share your Employee ID and User Hash with authorized issuers (HR departments)</li>
            <li>Issuers will use these credentials to grant permission to access your records</li>
            <li>Once authorized, issuers can verify your employment documents</li>
            <li>Keep these credentials secure and don't share with unauthorized parties</li>
          </ol>
        </CardContent>
      </Card>
    </div>
  )
}
