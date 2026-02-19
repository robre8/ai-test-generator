interface TestResult {
  generated_tests: string
  execution_output: string
  passed: boolean
  error: string | null
}

interface TestResultsProps {
  result: TestResult
}

export default function TestResults({ result }: TestResultsProps) {
  return (
    <div className="space-y-6">
      {/* Status */}
      <div className={`p-4 rounded-lg ${result.passed ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
        <p className={`font-bold text-lg ${result.passed ? 'text-green-700' : 'text-red-700'}`}>
          {result.passed ? '✅ Todos los tests pasaron' : '❌ Los tests fallaron'}
        </p>
      </div>

      {/* Error (if any) */}
      {result.error && (
        <div>
          <h3 className="font-bold text-red-700 mb-2">⚠️ Error</h3>
          <pre className="bg-red-50 p-3 rounded border border-red-200 text-red-700 text-sm overflow-auto max-h-40">
            {result.error}
          </pre>
        </div>
      )}

      {/* Generated Tests */}
      {result.generated_tests && (
        <div>
          <h3 className="font-bold text-gray-800 mb-2">Tests Generados</h3>
          <pre className="bg-gray-50 p-3 rounded border border-gray-300 text-gray-900 text-xs overflow-auto max-h-40">
            {result.generated_tests}
          </pre>
        </div>
      )}

      {/* Pytest Output */}
      {result.execution_output && (
        <div>
          <h3 className="font-bold text-gray-800 mb-2">Output de pytest</h3>
          <pre className="bg-gray-900 p-3 rounded border border-gray-700 text-green-400 text-xs overflow-auto max-h-40 font-mono">
            {result.execution_output}
          </pre>
        </div>
      )}
    </div>
  )
}
