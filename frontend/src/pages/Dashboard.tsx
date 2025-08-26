import { Link } from 'react-router-dom'

const Dashboard = () => {
  // Mock data - replace with actual data from your backend
  const mockQuizzes = [
    {
      id: 1,
      title: "General Knowledge Quiz",
      description: "Test your knowledge on various topics",
      questionCount: 10,
      difficulty: "Medium",
      category: "General"
    },
    {
      id: 2,
      title: "Science Quiz",
      description: "Explore the wonders of science",
      questionCount: 15,
      difficulty: "Hard",
      category: "Science"
    },
    {
      id: 3,
      title: "History Quiz",
      description: "Journey through time and events",
      questionCount: 12,
      difficulty: "Easy",
      category: "History"
    }
  ]

  const stats = [
    { label: "Total Quizzes", value: "24", icon: "📚" },
    { label: "Completed", value: "18", icon: "✅" },
    { label: "Average Score", value: "85%", icon: "🎯" },
    { label: "Rank", value: "#12", icon: "🏆" }
  ]

  return (
    <div className="min-h-screen bg-gradient-bg">
      {/* Header */}
      <div className="bg-white shadow-soft">
        <div className="max-w-7xl mx-auto px-8 py-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Dashboard</h1>
          <p className="text-gray-600">Welcome back! Here's your quiz overview.</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {stats.map((stat, index) => (
            <div key={index} className="bg-white rounded-2xl shadow-card p-6 hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.label}</p>
                  <p className="text-2xl font-bold text-gray-800">{stat.value}</p>
                </div>
                <div className="text-3xl">{stat.icon}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-2xl shadow-card p-8 mb-12">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Quick Actions</h2>
          <div className="flex flex-wrap gap-4">
            <Link
              to="/create-quiz"
              className="px-6 py-3 bg-gradient-primary text-white font-semibold rounded-xl hover:opacity-90 transform hover:scale-105 transition-all duration-200"
            >
              Create New Quiz
            </Link>
            <Link
              to="/quiz/1"
              className="px-6 py-3 bg-white text-primary-600 font-semibold rounded-xl border-2 border-primary-200 hover:bg-primary-50 transition-all duration-200"
            >
              Take Quiz
            </Link>
            <Link
              to="/leaderboard"
              className="px-6 py-3 bg-white text-primary-600 font-semibold rounded-xl border-2 border-primary-200 hover:bg-primary-50 transition-all duration-200"
            >
              View Leaderboard
            </Link>
          </div>
        </div>

        {/* Recent Quizzes */}
        <div className="bg-white rounded-2xl shadow-card p-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-semibold text-gray-800">Recent Quizzes</h2>
            <Link to="/create-quiz" className="text-primary-600 hover:text-primary-700 font-medium">
              View All
            </Link>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockQuizzes.map((quiz) => (
              <div key={quiz.id} className="border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-shadow duration-300">
                <div className="flex items-start justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-800">{quiz.title}</h3>
                  <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                    quiz.difficulty === 'Easy' ? 'bg-green-100 text-green-800' :
                    quiz.difficulty === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {quiz.difficulty}
                  </span>
                </div>
                
                <p className="text-gray-600 text-sm mb-4">{quiz.description}</p>
                
                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <span>{quiz.questionCount} questions</span>
                  <span>{quiz.category}</span>
                </div>
                
                <div className="flex gap-2">
                  <Link
                    to={`/quiz/${quiz.id}`}
                    className="flex-1 px-4 py-2 bg-primary-600 text-white text-center rounded-lg hover:bg-primary-700 transition-colors duration-200"
                  >
                    Take Quiz
                  </Link>
                  <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors duration-200">
                    Edit
                  </button>
                </div>
              </div>
            ))}
          </div>
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

export default Dashboard 