import { useState } from 'react'

const QuizCreator = () => {
  const [quizData, setQuizData] = useState({
    title: '',
    description: '',
    category: '',
    difficulty: 'Medium',
    questionCount: 10,
    useAI: true
  })

  const [isGenerating, setIsGenerating] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (quizData.useAI) {
      setIsGenerating(true)
      // TODO: Implement AI quiz generation
      setTimeout(() => {
        setIsGenerating(false)
        console.log('AI Quiz generated:', quizData)
      }, 2000)
    } else {
      console.log('Manual quiz creation:', quizData)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    setQuizData({
      ...quizData,
      [e.target.name]: e.target.value
    })
  }

  const categories = [
    'General Knowledge',
    'Science',
    'History',
    'Geography',
    'Literature',
    'Sports',
    'Technology',
    'Arts',
    'Mathematics',
    'Other'
  ]

  return (
    <div className="min-h-screen bg-gradient-bg">
      {/* Header */}
      <div className="bg-white shadow-soft">
        <div className="max-w-7xl mx-auto px-8 py-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Create Quiz</h1>
          <p className="text-gray-600">Generate engaging quizzes with AI or create them manually</p>
        </div>
      </div>

      <div className="max-w-4xl mx-auto px-8 py-8">
        {/* AI vs Manual Toggle */}
        <div className="bg-white rounded-2xl shadow-card p-8 mb-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Quiz Generation Method</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div 
              className={`p-6 rounded-xl border-2 cursor-pointer transition-all duration-200 ${
                quizData.useAI 
                  ? 'border-primary-500 bg-primary-50' 
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => setQuizData({ ...quizData, useAI: true })}
            >
              <div className="text-center">
                <div className="w-16 h-16 bg-gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <span className="text-3xl text-white">🤖</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">AI Generation</h3>
                <p className="text-gray-600 text-sm">
                  Let AI create questions based on your topic and preferences
                </p>
              </div>
            </div>

            <div 
              className={`p-6 rounded-xl border-2 cursor-pointer transition-all duration-200 ${
                !quizData.useAI 
                  ? 'border-primary-500 bg-primary-50' 
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => setQuizData({ ...quizData, useAI: false })}
            >
              <div className="text-center">
                <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                  <span className="text-3xl">✏️</span>
                </div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Manual Creation</h3>
                <p className="text-gray-600 text-sm">
                  Create questions manually with full control over content
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Quiz Creation Form */}
        <div className="bg-white rounded-2xl shadow-card p-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Quiz Details</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Title */}
            <div>
              <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
                Quiz Title *
              </label>
              <input
                type="text"
                id="title"
                name="title"
                value={quizData.title}
                onChange={handleChange}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                placeholder="Enter quiz title"
              />
            </div>

            {/* Description */}
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                id="description"
                name="description"
                value={quizData.description}
                onChange={handleChange}
                rows={3}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                placeholder="Describe what this quiz is about"
              />
            </div>

            {/* Category and Difficulty */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                  Category
                </label>
                <select
                  id="category"
                  name="category"
                  value={quizData.category}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                >
                  <option value="">Select a category</option>
                  {categories.map((category) => (
                    <option key={category} value={category}>{category}</option>
                  ))}
                </select>
              </div>

              <div>
                <label htmlFor="difficulty" className="block text-sm font-medium text-gray-700 mb-2">
                  Difficulty
                </label>
                <select
                  id="difficulty"
                  name="difficulty"
                  value={quizData.difficulty}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
                >
                  <option value="Easy">Easy</option>
                  <option value="Medium">Medium</option>
                  <option value="Hard">Hard</option>
                </select>
              </div>
            </div>

            {/* Question Count */}
            <div>
              <label htmlFor="questionCount" className="block text-sm font-medium text-gray-700 mb-2">
                Number of Questions
              </label>
              <input
                type="number"
                id="questionCount"
                name="questionCount"
                value={quizData.questionCount}
                onChange={handleChange}
                min="1"
                max="50"
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200"
              />
            </div>

            {/* AI Generation Options */}
            {quizData.useAI && (
              <div className="bg-primary-50 border border-primary-200 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-primary-800 mb-4">🤖 AI Generation Options</h3>
                <div className="space-y-4">
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="includeExplanations"
                      className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                    />
                    <label htmlFor="includeExplanations" className="ml-2 text-sm text-gray-700">
                      Include explanations for correct answers
                    </label>
                  </div>
                  <div className="flex items-center">
                    <input
                      type="checkbox"
                      id="adaptiveDifficulty"
                      className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                    />
                    <label htmlFor="adaptiveDifficulty" className="ml-2 text-sm text-gray-700">
                      Use adaptive difficulty based on user performance
                    </label>
                  </div>
                </div>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isGenerating}
              className={`w-full py-4 px-6 rounded-xl font-semibold text-white transition-all duration-200 ${
                isGenerating
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-gradient-primary hover:opacity-90 transform hover:scale-[1.02]'
              }`}
            >
              {isGenerating ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Generating Quiz...
                </div>
              ) : (
                quizData.useAI ? 'Generate Quiz with AI' : 'Create Quiz Manually'
              )}
            </button>
          </form>
        </div>
      </div>

      {/* Footer Navigation */}
      <footer className="bg-white shadow-footer py-4 mt-12">
        <div className="flex justify-around items-center max-w-md mx-auto">
          <button className="p-3 text-primary-600 hover:text-primary-700 transition-colors duration-200">
            <span className="text-2xl">🏠</span>
          </button>
          <button className="p-3 text-primary-600 hover:text-primary-700 transition-colors duration-200">
            <span className="text-2xl">❓</span>
          </button>
          <button className="p-3 text-primary-600 hover:text-primary-700 transition-colors duration-200">
            <span className="text-2xl">👤</span>
          </button>
        </div>
      </footer>
    </div>
  )
}

export default QuizCreator 