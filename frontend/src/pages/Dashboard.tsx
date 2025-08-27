import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { userAPI, UserStats, UserQuizAttempt, quizAPI, Quiz } from '../services/api'

const Dashboard = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [stats, setStats] = useState<UserStats | null>(null)
  const [recentQuizzes, setRecentQuizzes] = useState<Quiz[]>([])
  const [quizAttempts, setQuizAttempts] = useState<UserQuizAttempt[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!user) {
      navigate('/login')
      return
    }

    const fetchData = async () => {
      try {
        const [userStats, quizzes, attempts] = await Promise.all([
          userAPI.getStats(),
          quizAPI.getAll({ limit: 6 }),
          userAPI.getQuizAttempts()
        ])
        setStats(userStats)
        setRecentQuizzes(quizzes)
        setQuizAttempts(attempts)
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [user, navigate])

  // Refresh data when component comes back into focus (e.g., after completing a quiz)
  useEffect(() => {
    const handleFocus = async () => {
      if (user && !loading) {
        try {
          const [userStats, attempts] = await Promise.all([
            userAPI.getStats(),
            userAPI.getQuizAttempts()
          ])
          setStats(userStats)
          setQuizAttempts(attempts)
        } catch (error) {
          console.error('Failed to refresh user stats:', error)
        }
      }
    }

    window.addEventListener('focus', handleFocus)
    return () => window.removeEventListener('focus', handleFocus)
  }, [user, loading])

  if (!user) {
    return null // Will redirect to login
  }

  // Helper function to get user's last attempt for a quiz
  const getQuizAttempt = (quizId: string) => {
    return quizAttempts.find(attempt => attempt.quiz_id === quizId)
  }

  const dashboardStats = [
    { 
      label: "Total Score", 
      value: loading ? "..." : stats?.total_score?.toString() || "0", 
      icon: "🎯" 
    },
    { 
      label: "Quizzes Taken", 
      value: loading ? "..." : stats?.quizzes_taken?.toString() || "0", 
      icon: "✅" 
    },
    { 
      label: "Average Score", 
      value: loading ? "..." : stats?.average_score ? `${Math.round(stats.average_score)}%` : "0%", 
      icon: "📊" 
    },
    { 
      label: "Global Rank", 
      value: loading ? "..." : stats?.rank ? `#${stats.rank}` : "N/A", 
      icon: "🏆" 
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-bg">
      {/* Header */}
      <div className="bg-white shadow-soft">
        <div className="max-w-7xl mx-auto px-8 py-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">Welcome back, {user.username}!</h1>
              <p className="text-gray-600">Here's your quiz overview and recent activity.</p>
            </div>
            <button
              onClick={logout}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {dashboardStats.map((stat, index) => (
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
            {loading ? (
              // Loading skeleton
              Array.from({ length: 3 }).map((_, index) => (
                <div key={index} className="border border-gray-200 rounded-xl p-6 animate-pulse">
                  <div className="h-4 bg-gray-200 rounded mb-4"></div>
                  <div className="h-3 bg-gray-200 rounded mb-2"></div>
                  <div className="h-3 bg-gray-200 rounded mb-4"></div>
                  <div className="flex gap-2">
                    <div className="flex-1 h-8 bg-gray-200 rounded"></div>
                    <div className="w-16 h-8 bg-gray-200 rounded"></div>
                  </div>
                </div>
              ))
            ) : recentQuizzes.length > 0 ? (
              recentQuizzes.map((quiz) => {
                const attempt = getQuizAttempt(quiz.id)
                return (
                  <div key={quiz.id} className="border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-shadow duration-300">
                    <div className="flex items-start justify-between mb-4">
                      <h3 className="text-lg font-semibold text-gray-800">{quiz.title}</h3>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                        quiz.difficulty === 'easy' ? 'bg-green-100 text-green-800' :
                        quiz.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {quiz.difficulty}
                      </span>
                    </div>
                    
                    <p className="text-gray-600 text-sm mb-4">{quiz.description || 'No description available'}</p>
                    
                    <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                      <span>{quiz.question_count} questions</span>
                      <span>{quiz.subject}</span>
                    </div>
                    
                    {/* Show last score if user has taken this quiz */}
                    {attempt && (
                      <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                        <div className="flex items-center justify-between">
                          <div className="text-sm text-blue-800">
                            <span className="font-medium">Last Score:</span> {attempt.last_score}/{attempt.max_score}
                          </div>
                          <div className="text-sm font-semibold text-blue-900">
                            {attempt.last_percentage}%
                          </div>
                        </div>
                      </div>
                    )}
                    
                    <div className="flex gap-2">
                      <Link
                        to={`/quiz/${quiz.id}`}
                        className="flex-1 px-4 py-2 bg-primary-600 text-white text-center rounded-lg hover:bg-primary-700 transition-colors duration-200"
                      >
                        {attempt ? 'Retake Quiz' : 'Take Quiz'}
                      </Link>
                      {quiz.creator_username === user.username && (
                        <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors duration-200">
                          Edit
                        </button>
                      )}
                    </div>
                  </div>
                )
              })
            ) : (
              <div className="col-span-full text-center py-12">
                <div className="text-gray-400 mb-4">
                  <span className="text-6xl">📝</span>
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">No quizzes yet</h3>
                <p className="text-gray-600 mb-4">Start by creating your first questionnaire!</p>
                <Link
                  to="/create-quiz"
                  className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
                >
                  Create Questionnaire
                </Link>
              </div>
            )}
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