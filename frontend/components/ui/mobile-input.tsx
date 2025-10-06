"use client"

import React, { forwardRef } from "react"
import { Input } from "./input"
import { Label } from "./label"
import { cn } from "@/lib/utils"

interface MobileInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helperText?: string
  onValueChange?: (value: string) => void
}

const MobileInput = forwardRef<HTMLInputElement, MobileInputProps>(
  ({ label, error, helperText, onValueChange, className, ...props }, ref) => {
    const formatMobileNumber = (value: string): string => {
      // Remove all non-digit characters except +
      let cleaned = value.replace(/[^\d+]/g, '')
      
      // Ensure only one + at the beginning
      if (cleaned.indexOf('+') > 0) {
        cleaned = cleaned.replace(/\+/g, '')
      }
      if (cleaned.startsWith('+') && cleaned.indexOf('+', 1) > 0) {
        cleaned = cleaned.substring(0, cleaned.indexOf('+', 1))
      }
      
      // Limit length
      if (cleaned.startsWith('+')) {
        if (cleaned.length > 16) cleaned = cleaned.substring(0, 16)
      } else {
        if (cleaned.length > 15) cleaned = cleaned.substring(0, 15)
      }
      
      return cleaned
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const formatted = formatMobileNumber(e.target.value)
      e.target.value = formatted
      
      if (onValueChange) {
        onValueChange(formatted)
      }
      
      if (props.onChange) {
        props.onChange(e)
      }
    }

    return (
      <div className="space-y-2">
        {label && (
          <Label htmlFor={props.id} className="text-sm font-medium">
            {label}
          </Label>
        )}
        <Input
          {...props}
          ref={ref}
          type="tel"
          onChange={handleChange}
          className={cn(
            error && "border-red-500 focus:border-red-500 focus:ring-red-500",
            className
          )}
          placeholder={props.placeholder || "+1234567890 or 1234567890"}
        />
        {error && (
          <p className="text-red-500 text-sm">{error}</p>
        )}
        {helperText && !error && (
          <p className="text-gray-500 text-xs">{helperText}</p>
        )}
      </div>
    )
  }
)

MobileInput.displayName = "MobileInput"

export { MobileInput }
