import { useState } from 'react';

export default function RepoInput({ onSubmit, isLoading, isDarkMode }) {
  const [repoUrl, setRepoUrl] = useState('');
  const [error, setError] = useState('');

  const validateGitHubUrl = (url) => {
    const pattern = /^https:\/\/github\.com\/[\w-]+\/[\w-]+\/?$/;
    return pattern.test(url);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (!validateGitHubUrl(repoUrl)) {
      setError(
        'Please enter a valid GitHub repository URL (e.g., https://github.com/username/repo)'
      );
      return;
    }

    onSubmit(repoUrl);
  };

  return (
    <div className="max-w-2xl mx-auto mt-8 p-6">
      <h1 className={`text-3xl font-bold mb-4 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
        Smart Documentation Generator
      </h1>
      <p className={`mb-6 ${isDarkMode ? 'text-gray-300' : 'text-gray-600'}`}>
        Generate beginner, intermediate, and advanced documentation for any public GitHub repository
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <input
            type="text"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="https://github.com/username/repository"
            className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition ${
              isDarkMode
                ? 'bg-gray-800 border-gray-600 text-white placeholder-gray-400'
                : 'bg-white border-gray-300 text-gray-900'
            }`}
            disabled={isLoading}
          />
          {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
        >
          {isLoading ? 'Generating Documentation...' : 'Generate Documentation'}
        </button>
      </form>

      <div className={`mt-6 p-4 rounded-lg ${
        isDarkMode ? 'bg-blue-900/30 border border-blue-700' : 'bg-blue-50'
      }`}>
        <h3 className={`font-semibold mb-2 ${isDarkMode ? 'text-blue-300' : 'text-gray-900'}`}>
          Try these examples:
        </h3>
        <ul className={`space-y-1 text-sm ${isDarkMode ? 'text-blue-400' : 'text-blue-700'}`}>
          <li
            className="cursor-pointer hover:underline"
            onClick={() => setRepoUrl('https://github.com/expressjs/express')}
          >
            https://github.com/expressjs/express
          </li>
          <li
            className="cursor-pointer hover:underline"
            onClick={() => setRepoUrl('https://github.com/axios/axios')}
          >
            https://github.com/axios/axios
          </li>
          <li
            className="cursor-pointer hover:underline"
            onClick={() => setRepoUrl('https://github.com/microsoft/vscode')}
          >
            https://github.com/microsoft/vscode
          </li>
        </ul>
      </div>
    </div>
  );
}
