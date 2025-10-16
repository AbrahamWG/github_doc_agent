export default function LoadingState({ isDarkMode }) {
  return (
    <div className="max-w-2xl mx-auto mt-16 text-center">
      <div className={`animate-spin rounded-full h-16 w-16 border-b-2 mx-auto mb-4 ${
        isDarkMode ? 'border-blue-400' : 'border-blue-600'
      }`}></div>
      <h3 className={`text-xl font-semibold mb-2 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
        Generating Documentation
      </h3>
      <p className={isDarkMode ? 'text-gray-300' : 'text-gray-600'}>
        This may take 30-60 seconds...
      </p>

      <div className="mt-8 space-y-2 text-left max-w-md mx-auto">
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 rounded-full bg-green-500"></div>
          <p className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>
            Fetching repository structure
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 rounded-full bg-yellow-500 animate-pulse"></div>
          <p className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>
            Analyzing code complexity
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <div className={`w-4 h-4 rounded-full ${isDarkMode ? 'bg-gray-600' : 'bg-gray-300'}`}></div>
          <p className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>
            Gathering context
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <div className={`w-4 h-4 rounded-full ${isDarkMode ? 'bg-gray-600' : 'bg-gray-300'}`}></div>
          <p className={`text-sm ${isDarkMode ? 'text-gray-300' : 'text-gray-700'}`}>
            Generating documentation
          </p>
        </div>
      </div>
    </div>
  );
}
