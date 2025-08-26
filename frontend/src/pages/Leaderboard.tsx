const Leaderboard = () => {
  // Mock leaderboard data - replace with actual data from your backend
  const leaderboardData = [
    {
      rank: 1,
      name: "Alex Johnson",
      score: 2850,
      quizzesTaken: 24,
      averageScore: 95,
      avatar: "👨‍💻"
    },
    {
      rank: 2,
      name: "Sarah Chen",
      score: 2720,
      quizzesTaken: 22,
      averageScore: 92,
      avatar: "👩‍🎓"
    },
    {
      rank: 3,
      name: "Mike Rodriguez",
      score: 2580,
      quizzesTaken: 20,
      averageScore: 89,
      avatar: "👨‍🔬"
    },
    {
      rank: 4,
      name: "Emily Davis",
      score: 2450,
      quizzesTaken: 19,
      averageScore: 87,
      avatar: "👩‍🏫"
    },
    {
      rank: 5,
      name: "David Kim",
      score: 2320,
      quizzesTaken: 18,
      averageScore: 85,
      avatar: "👨‍💼"
    },
    {
      rank: 6,
      name: "Lisa Wang",
      score: 2180,
      quizzesTaken: 17,
      averageScore: 83,
      avatar: "👩‍🎨"
    },
    {
      rank: 7,
      name: "Tom Wilson",
      score: 2050,
      quizzesTaken: 16,
      averageScore: 81,
      avatar: "👨‍🚀"
    },
    {
      rank: 8,
      name: "Anna Brown",
      score: 1920,
      quizzesTaken: 15,
      averageScore: 79,
      avatar: "👩‍⚕️"
    }
  ]

  const getRankBadge = (rank: number) => {
    if (rank === 1) return "🥇"
    if (rank === 2) return "🥈"
    if (rank === 3) return "🥉"
    return `#${rank}`
  }

  const getRankColor = (rank: number) => {
    if (rank === 1) return "bg-yellow-100 text-yellow-800 border-yellow-200"
    if (rank === 2) return "bg-gray-100 text-gray-800 border-gray-200"
    if (rank === 3) return "bg-orange-100 text-orange-800 border-orange-200"
    return "bg-white text-gray-600 border-gray-200"
  }

  return (
    <div className="min-h-screen bg-gradient-bg">
      {/* Header */}
      <div className="bg-white shadow-soft">
        <div className="max-w-7xl mx-auto px-8 py-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Leaderboard</h1>
          <p className="text-gray-600">See how you rank against other quiz enthusiasts</p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-8 py-8">
        {/* Top 3 Podium */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {leaderboardData.slice(0, 3).map((user, index) => (
            <div key={user.rank} className={`text-center ${index === 1 ? 'order-first md:order-none' : ''}`}>
              <div className={`relative ${index === 1 ? 'scale-110' : 'scale-100'} transition-transform duration-300`}>
                <div className={`w-24 h-24 mx-auto mb-4 rounded-full flex items-center justify-center text-4xl ${
                  index === 0 ? 'bg-yellow-100' : 
                  index === 1 ? 'bg-gray-100' : 'bg-orange-100'
                }`}>
                  {user.avatar}
                </div>
                <div className="absolute -top-2 -right-2 w-8 h-8 rounded-full bg-gradient-primary text-white text-sm font-bold flex items-center justify-center">
                  {getRankBadge(user.rank)}
                </div>
              </div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">{user.name}</h3>
              <p className="text-2xl font-bold text-primary-600 mb-1">{user.score}</p>
              <p className="text-sm text-gray-600">points</p>
            </div>
          ))}
        </div>

        {/* Full Leaderboard */}
        <div className="bg-white rounded-2xl shadow-card p-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Full Rankings</h2>
          
          <div className="space-y-4">
            {leaderboardData.map((user) => (
              <div key={user.rank} className={`flex items-center p-4 rounded-xl border-2 ${getRankColor(user.rank)} transition-all duration-200 hover:shadow-md`}>
                {/* Rank */}
                <div className="w-12 h-12 rounded-full bg-gradient-primary text-white font-bold text-lg flex items-center justify-center mr-4">
                  {user.rank}
                </div>

                {/* Avatar and Name */}
                <div className="flex items-center flex-1">
                  <span className="text-2xl mr-3">{user.avatar}</span>
                  <div>
                    <h3 className="font-semibold text-gray-800">{user.name}</h3>
                    <p className="text-sm text-gray-600">{user.quizzesTaken} quizzes taken</p>
                  </div>
                </div>

                {/* Stats */}
                <div className="text-right">
                  <p className="text-xl font-bold text-gray-800">{user.score}</p>
                  <p className="text-sm text-gray-600">{user.averageScore}% avg</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Your Ranking */}
        <div className="bg-white rounded-2xl shadow-card p-8 mt-8">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Your Ranking</h2>
          <div className="text-center py-8">
            <p className="text-gray-600 mb-4">Sign in to see your ranking and compete with others!</p>
            <button className="px-6 py-3 bg-gradient-primary text-white font-semibold rounded-xl hover:opacity-90 transform hover:scale-105 transition-all duration-200">
              Sign In to Compete
            </button>
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

export default Leaderboard 