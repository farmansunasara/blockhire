"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { 
  FileText, 
  Download, 
  Eye, 
  Calendar, 
  Hash, 
  CheckCircle, 
  Clock,
  AlertCircle,
  Copy,
  ExternalLink
} from "lucide-react"
import { DocumentRecord } from "@/types/api"

interface DocumentHistoryProps {
  documents: DocumentRecord[]
  onDownload: (docHash: string) => void
  onView: (docHash: string) => void
  isLoading?: boolean
}

export default function DocumentHistory({ 
  documents, 
  onDownload, 
  onView, 
  isLoading = false 
}: DocumentHistoryProps) {
  const [downloading, setDownloading] = useState<string | null>(null)
  const [copiedHash, setCopiedHash] = useState<string | null>(null)

  const handleDownload = async (docHash: string) => {
    setDownloading(docHash)
    try {
      await onDownload(docHash)
    } finally {
      setDownloading(null)
    }
  }

  const handleCopyHash = async (docHash: string) => {
    try {
      await navigator.clipboard.writeText(docHash)
      setCopiedHash(docHash)
      setTimeout(() => setCopiedHash(null), 2000)
    } catch (error) {
      console.error('Failed to copy hash:', error)
    }
  }

  const handleVerifyDocument = (docHash: string) => {
    // Navigate to verification page with pre-filled document hash
    window.open(`/verify?docHash=${docHash}`, '_blank')
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    })
  }

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <FileText className="mr-2" size={20} />
            Document History
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-2 text-gray-600">Loading documents...</span>
          </div>
        </CardContent>
      </Card>
    )
  }

  if (documents.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <FileText className="mr-2" size={20} />
            Document History
          </CardTitle>
          <CardDescription>
            Your uploaded employment documents will appear here
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <FileText className="mx-auto h-12 w-12 text-gray-400 mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No Documents Yet</h3>
            <p className="text-gray-600 mb-4">
              Upload your first employment document to get started
            </p>
            <Button onClick={() => {/* TODO: Navigate to upload */}}>
              Upload Document
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <FileText className="mr-2" size={20} />
          Document History
        </CardTitle>
        <CardDescription>
          {documents.length} document{documents.length !== 1 ? 's' : ''} uploaded
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {documents.map((doc, index) => (
            <div
              key={doc.docHash}
              className="border rounded-lg p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2 mb-2">
                    <FileText className="h-5 w-5 text-blue-600 flex-shrink-0" />
                    <h4 className="font-medium text-gray-900 truncate">
                      {doc.fileName}
                    </h4>
                    {doc.isOriginal && (
                      <Badge variant="default" className="text-xs">
                        <CheckCircle className="h-3 w-3 mr-1" />
                        Original
                      </Badge>
                    )}
                  </div>
                  
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-sm text-gray-600">
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-2" />
                      <span>{formatDate(doc.uploadDate)}</span>
                    </div>
                    
                    <div className="flex items-center">
                      <Hash className="h-4 w-4 mr-2" />
                      <div className="flex items-center space-x-2">
                        <code className="text-xs bg-gray-100 px-2 py-1 rounded font-mono">
                          {doc.docHash.slice(0, 16)}...
                        </code>
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => handleCopyHash(doc.docHash)}
                          className="h-6 w-6 p-0"
                        >
                          {copiedHash === doc.docHash ? (
                            <CheckCircle className="h-3 w-3 text-green-600" />
                          ) : (
                            <Copy className="h-3 w-3" />
                          )}
                        </Button>
                      </div>
                    </div>
                    
                    <div className="flex items-center">
                      <FileText className="h-4 w-4 mr-2" />
                      <span>{formatFileSize(doc.fileSize)}</span>
                    </div>
                    
                    <div className="flex items-center">
                      <Clock className="h-4 w-4 mr-2" />
                      <span>#{index + 1}</span>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2 ml-4">
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => onView(doc.docHash)}
                    className="flex items-center"
                  >
                    <Eye className="h-4 w-4 mr-1" />
                    View
                  </Button>
                  
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleDownload(doc.docHash)}
                    disabled={downloading === doc.docHash}
                    className="flex items-center"
                  >
                    {downloading === doc.docHash ? (
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600 mr-1"></div>
                    ) : (
                      <Download className="h-4 w-4 mr-1" />
                    )}
                    Download
                  </Button>

                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleVerifyDocument(doc.docHash)}
                    className="flex items-center"
                  >
                    <ExternalLink className="h-4 w-4 mr-1" />
                    Verify
                  </Button>
                </div>
              </div>
              
              {doc.isOriginal && (
                <div className="mt-3 space-y-3">
                  <Alert className="border-green-200 bg-green-50">
                    <CheckCircle className="h-4 w-4 text-green-600" />
                    <AlertDescription className="text-green-800">
                      This is your original document. Only this document's hash is used for verification.
                    </AlertDescription>
                  </Alert>
                  
                  <div className="bg-gray-50 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="text-sm font-medium text-gray-700 flex items-center">
                        <Hash className="h-4 w-4 mr-2" />
                        Document Hash for Verification
                      </h4>
                      <Button
                        size="sm"
                        variant="outline"
                        onClick={() => handleCopyHash(doc.docHash)}
                        className="flex items-center"
                      >
                        {copiedHash === doc.docHash ? (
                          <>
                            <CheckCircle className="h-4 w-4 mr-1 text-green-600" />
                            Copied!
                          </>
                        ) : (
                          <>
                            <Copy className="h-4 w-4 mr-1" />
                            Copy Hash
                          </>
                        )}
                      </Button>
                    </div>
                    <code className="text-xs bg-white border rounded p-2 block font-mono break-all">
                      {doc.docHash}
                    </code>
                    <p className="text-xs text-gray-600 mt-2">
                      Share this hash with verifiers to confirm document authenticity
                    </p>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
        
        {documents.length > 1 && (
          <Alert className="mt-4 border-amber-200 bg-amber-50">
            <AlertCircle className="h-4 w-4 text-amber-600" />
            <AlertDescription className="text-amber-800">
              <strong>Note:</strong> Only the original document (marked above) is used for verification. 
              Additional uploads are stored for your records but don't affect verification.
            </AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  )
}
