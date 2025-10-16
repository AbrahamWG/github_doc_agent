import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus, prism } from 'react-syntax-highlighter/dist/esm/styles/prism';

export default function DocumentationViewer({ documentation, repoName, isDarkMode }) {
  const [activeTab, setActiveTab] = useState('beginner');

  const tabs = [
    { id: 'beginner', label: 'Beginner', icon: '🌱' },
    { id: 'intermediate', label: 'Intermediate', icon: '⚡' },
    { id: 'advanced', label: 'Advanced', icon: '🚀' },
  ];

  const downloadMarkdown = (level) => {
    const content = documentation[level];
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${repoName}-${level}-docs.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className={`max-w-4xl mx-auto mt-8 p-6 ${isDarkMode ? 'text-white' : ''}`}>
      <div className="mb-6">
        <h2 className={`text-2xl font-bold mb-2 ${isDarkMode ? 'text-white' : 'text-gray-900'}`}>
          Documentation for {repoName}
        </h2>
        <p className={isDarkMode ? 'text-gray-300' : 'text-gray-600'}>
          Select your experience level to view tailored documentation
        </p>
      </div>

      {/* Tabs */}
      <div className={`flex space-x-2 mb-6 ${isDarkMode ? 'border-b border-gray-700' : 'border-b border-gray-200'}`}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2 font-medium transition ${
              activeTab === tab.id
                ? isDarkMode
                  ? 'border-b-2 border-blue-400 text-blue-400'
                  : 'border-b-2 border-blue-600 text-blue-600'
                : isDarkMode
                ? 'text-gray-400 hover:text-blue-400'
                : 'text-gray-600 hover:text-blue-600'
            }`}
          >
            <span className="mr-2">{tab.icon}</span>
            {tab.label}
          </button>
        ))}
      </div>

      {/* Documentation Content */}
      <div
        className={`rounded-lg shadow-lg p-8 prose prose-lg max-w-none
          ${isDarkMode
            ? 'bg-gray-800 prose-invert prose-headings:text-white prose-p:text-gray-200 prose-strong:text-white prose-code:text-blue-300'
            : 'bg-white prose-headings:text-gray-900 prose-p:text-gray-700'
          }
          prose-headings:font-bold
          prose-h1:text-3xl prose-h1:mb-4 prose-h1:mt-8
          prose-h2:text-2xl prose-h2:mb-3 prose-h2:mt-6
          prose-h3:text-xl prose-h3:mb-2 prose-h3:mt-4
          prose-p:mb-4 prose-p:leading-relaxed
          prose-ul:my-4 prose-ul:list-disc prose-ul:pl-6
          prose-ol:my-4 prose-ol:list-decimal prose-ol:pl-6
          prose-li:mb-2
          prose-code:text-sm prose-code:px-1 prose-code:py-0.5 prose-code:rounded
          ${isDarkMode ? 'prose-code:bg-gray-700' : 'prose-code:bg-gray-100'}
        `}
      >
        <ReactMarkdown
          components={{
            code({ node, inline, className, children, ...props }) {
              const match = /language-(\w+)/.exec(className || '');
              return !inline && match ? (
                <SyntaxHighlighter
                  style={isDarkMode ? vscDarkPlus : prism}
                  language={match[1]}
                  PreTag="div"
                  className="rounded-md my-4"
                  {...props}
                >
                  {String(children).replace(/\n$/, '')}
                </SyntaxHighlighter>
              ) : (
                <code className={className} {...props}>
                  {children}
                </code>
              );
            },
            p({ children }) {
              return <p className="mb-4 leading-relaxed">{children}</p>;
            },
            h1({ children }) {
              return <h1 className="text-3xl font-bold mb-4 mt-8">{children}</h1>;
            },
            h2({ children }) {
              return <h2 className="text-2xl font-bold mb-3 mt-6">{children}</h2>;
            },
            h3({ children }) {
              return <h3 className="text-xl font-bold mb-2 mt-4">{children}</h3>;
            },
            ul({ children }) {
              return <ul className="list-disc pl-6 my-4 space-y-2">{children}</ul>;
            },
            ol({ children }) {
              return <ol className="list-decimal pl-6 my-4 space-y-2">{children}</ol>;
            },
            li({ children }) {
              return <li className="mb-2">{children}</li>;
            },
          }}
        >
          {documentation[activeTab]}
        </ReactMarkdown>
      </div>

      {/* Download Buttons */}
      <div className="mt-6 flex gap-4">
        <button
          onClick={() => downloadMarkdown(activeTab)}
          className={`px-6 py-2 rounded-lg transition ${
            isDarkMode
              ? 'bg-green-600 hover:bg-green-700 text-white'
              : 'bg-green-600 hover:bg-green-700 text-white'
          }`}
        >
          Download {tabs.find((t) => t.id === activeTab)?.label} Documentation
        </button>
        <button
          onClick={() => window.location.reload()}
          className={`px-6 py-2 rounded-lg transition ${
            isDarkMode
              ? 'bg-gray-700 hover:bg-gray-600 text-white'
              : 'bg-gray-600 hover:bg-gray-700 text-white'
          }`}
        >
          Generate New Documentation
        </button>
      </div>
    </div>
  );
}
