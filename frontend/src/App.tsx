import { useState } from 'react'
import axios from 'axios'
import CodeEditor from './components/CodeEditor'
import TestResults from './components/TestResults'

interface TestResult {
  generated_tests: string
  execution_output: string
  passed: boolean
  error: string | null
}

function App() {
  const [code, setCode] = useState('')
  const [result, setResult] = useState<TestResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const apiBase = import.meta.env.VITE_API_URL || ''
  const api = axios.create({ baseURL: apiBase })

  const handleGenerateTests = async () => {
    if (!code.trim()) {
      setError('Por favor ingresa código Python')
      return
    }

    setLoading(true)
    setError('')

    try {
      const response = await api.post('/api/generate-tests', {
        code: code
      })
      setResult(response.data)
    } catch (err) {
      let errorMsg = 'Error desconocido'
      
      if (axios.isAxiosError(err)) {
        if (err.response?.data?.error) {
          errorMsg = err.response.data.error
        } else if (err.response?.data?.detail) {
          errorMsg = err.response.data.detail
        } else if (err.message) {
          errorMsg = err.message
        }
      }
      
      setError(`❌ ${errorMsg}`)
      console.error('Full error:', err)
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-blue-800">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">🧪 AI Test Generator</h1>
          <p className="text-blue-100">Genera pruebas automáticas con inteligencia artificial</p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Left Panel - Code Input */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-800 mb-4">Código Python</h2>
            <CodeEditor code={code} onChange={setCode} />
            <button
              onClick={handleGenerateTests}
              disabled={loading}
              className="mt-4 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-bold py-3 px-4 rounded-lg transition duration-200"
            >
              {loading ? '⏳ Generando...' : '✨ Generate Tests'}
            </button>
            
            {/* Security Info */}
            <div className="mt-6 p-4 bg-amber-50 border border-amber-200 rounded-lg">
              <p className="text-sm font-semibold text-amber-900 mb-2">🛡️ Por seguridad:</p>
              <ul className="text-xs text-amber-800 space-y-1">
                <li>❌ No se permite: os, subprocess, sys, open()</li>
                <li>❌ No se permite: eval(), exec(), import</li>
                <li>✅ Máximo 5000 caracteres</li>
                <li>⏱️ Timeout: 10 seconds</li>
              </ul>
            </div>
          </div>

          {/* Right Panel - Results */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
                <p className="text-red-700 font-semibold">{error}</p>
              </div>
            )}
            {result && <TestResults result={result} />}
            {!result && !error && (
              <div className="text-gray-400 text-center py-12">
                Los resultados aparecerán aquí...
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
