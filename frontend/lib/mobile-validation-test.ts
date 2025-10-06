/**
 * Test file for mobile number validation
 * This can be removed in production
 */

import { validationRules } from './validation'

// Test cases for mobile number validation
const testCases = [
  // Valid cases
  { input: "1234567890", expected: null, description: "10 digit number" },
  { input: "+1234567890", expected: null, description: "International format" },
  { input: "1234567890123", expected: null, description: "13 digit number" },
  { input: "+123456789012345", expected: null, description: "15 digit international" },
  
  // Invalid cases
  { input: "123456789", expected: "Mobile number must be at least 10 digits", description: "Too short" },
  { input: "0123456789", expected: "Mobile number cannot start with 0", description: "Starts with 0" },
  { input: "1234567890123456", expected: "Mobile number cannot exceed 15 digits", description: "Too long" },
  { input: "abc123456789", expected: "Please enter a valid mobile number", description: "Contains letters" },
  { input: "123-456-7890", expected: "Please enter a valid mobile number", description: "Contains dashes" },
  { input: "(123) 456-7890", expected: "Please enter a valid mobile number", description: "Contains parentheses" },
  { input: "+0123456789", expected: "Mobile number cannot start with 0", description: "International starting with 0" },
  { input: "++1234567890", expected: "Please enter a valid mobile number", description: "Double plus" },
]

export function testMobileValidation() {
  console.log("Testing Mobile Number Validation")
  console.log("=================================")
  
  const validator = new (require('./validation').FormValidator)()
  validator.addRule('mobile', validationRules.mobile)
  
  testCases.forEach((testCase, index) => {
    const result = validator.validate({ mobile: testCase.input })
    const error = result.errors.mobile || null
    const passed = error === testCase.expected
    
    console.log(`Test ${index + 1}: ${testCase.description}`)
    console.log(`  Input: "${testCase.input}"`)
    console.log(`  Expected: ${testCase.expected || 'null'}`)
    console.log(`  Got: ${error || 'null'}`)
    console.log(`  Result: ${passed ? '✅ PASS' : '❌ FAIL'}`)
    console.log('')
  })
}

// Uncomment to run tests
// testMobileValidation()
