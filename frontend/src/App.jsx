import { useState, useEffect } from 'react';
import RepoInput from './components/RepoInput';
import LoadingState from './components/LoadingState';
import DocumentationViewer from './components/DocumentationViewer';
import ErrorBoundary from './components/ErrorBoundary';
import { generateDocumentation, checkHealth } from './services/api';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [documentation, setDocumentation] = useState(null);
  const [error, setError] = useState(null);
  const [repoName, setRepoName] = useState('');
  const [backendHealth, setBackendHealth] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Check backend health on mount
  useEffect(() => {
    checkHealth()
      .then(() => setBackendHealth(true))
      .catch(() => setBackendHealth(false));
  }, []);

  // Load dark mode preference from localStorage
  useEffect(() => {
    const savedDarkMode = localStorage.getItem('darkMode') === 'true';
    setIsDarkMode(savedDarkMode);
  }, []);

  // Toggle dark mode and save preference
  const toggleDarkMode = () => {
    const newDarkMode = !isDarkMode;
    setIsDarkMode(newDarkMode);
    localStorage.setItem('darkMode', newDarkMode.toString());
  };

  const handleGenerateDocumentation = async (repoUrl) => {
    setIsLoading(true);
    setError(null);
    setDocumentation(null);

    try {
      const result = await generateDocumentation(repoUrl);
      setDocumentation(result.documentation);
      setRepoName(result.repo_name);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ErrorBoundary>
      <div className={`min-h-screen py-8 transition-colors duration-200 ${
        isDarkMode ? 'bg-gray-900' : 'bg-gray-50'
      }`}>
        {/* Dark Mode Toggle */}
        <div className="fixed top-4 right-4 z-50">
          <button
            onClick={toggleDarkMode}
            className={`p-3 rounded-full shadow-lg transition-all duration-200 ${
              isDarkMode
                ? 'bg-gray-700 hover:bg-gray-600 text-yellow-300'
                : 'bg-white hover:bg-gray-100 text-gray-700'
            }`}
            aria-label="Toggle dark mode"
          >
            {isDarkMode ? (
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" />
              </svg>
            ) : (
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
              </svg>
            )}
          </button>
        </div>

        {!backendHealth && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded max-w-2xl mx-auto mb-4">
            <p className="font-bold">Backend Not Reachable</p>
            <p className="text-sm">
              Make sure the FastAPI backend is running on port 8000
            </p>
          </div>
        )}

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded max-w-2xl mx-auto mb-4">
            <p className="font-bold">Error</p>
            <p className="text-sm">{error}</p>
          </div>
        )}

        {!isLoading && !documentation && (
          <RepoInput
            onSubmit={handleGenerateDocumentation}
            isLoading={isLoading}
            isDarkMode={isDarkMode}
          />
        )}

        {isLoading && <LoadingState isDarkMode={isDarkMode} />}

        {documentation && (
          <DocumentationViewer
            documentation={documentation}
            repoName={repoName}
            isDarkMode={isDarkMode}
          />
        )}
      </div>
    </ErrorBoundary>
  );
}

export default App;
