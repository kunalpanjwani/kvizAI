import { Link } from 'react-router-dom'

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-bg flex flex-col">
      {/* Hero Section */}
      <div className="flex-1 flex flex-col justify-center items-center px-4 py-16">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl font-bold text-gray-800 mb-6">
            Welcome to <span className="bg-gradient-primary bg-clip-text text-transparent">Quiz</span>
          </h1>
          <p className="text-xl text-gray-600 mb-12 leading-relaxed">
            AI-Powered Quiz Platform - Create, Take, and Compete with Intelligent Quizzes
          </p>
          
          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <Link
              to="/create-quiz"
              className="px-8 py-4 bg-gradient-primary text-white font-semibold rounded-xl hover:opacity-90 transform hover:scale-105 transition-all duration-200 shadow-lg"
            >
              Create Quiz
            </Link>
            <Link
              to="/dashboard"
              className="px-8 py-4 bg-white text-primary-600 font-semibold rounded-xl border-2 border-primary-200 hover:bg-primary-50 transition-all duration-200 shadow-lg"
            >
              Browse Quizzes
            </Link>
          </div>

          {/* Feature Cards */}
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="bg-white rounded-2xl shadow-card p-8 hover:shadow-xl transition-shadow duration-300">
              <div className="w-16 h-16 bg-gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl text-white">🎯</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Create Quizzes</h3>
              <p className="text-gray-600 leading-relaxed">
                Generate personalized quizzes using advanced AI technology. Create engaging content in seconds.
              </p>
            </div>
            
            <div className="bg-white rounded-2xl shadow-card p-8 hover:shadow-xl transition-shadow duration-300">
              <div className="w-16 h-16 bg-gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl text-white">🧠</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Take Quizzes</h3>
              <p className="text-gray-600 leading-relaxed">
                Test your knowledge with interactive, adaptive quizzes. Learn while having fun.
              </p>
            </div>
            
            <div className="bg-white rounded-2xl shadow-card p-8 hover:shadow-xl transition-shadow duration-300">
              <div className="w-16 h-16 bg-gradient-primary rounded-2xl flex items-center justify-center mx-auto mb-6">
                <span className="text-3xl text-white">🏆</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-800 mb-4">Compete</h3>
              <p className="text-gray-600 leading-relaxed">
                Join leaderboards and compete with others. Track your progress and achievements.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Navigation */}
      <footer className="bg-white shadow-footer py-4">
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

export default Home 