const Home = () => {
  return (
    <div className="text-center">
      <h1 className="text-4xl font-bold text-gray-900 mb-4">
        Welcome to kvizAI
      </h1>
      <p className="text-xl text-gray-600 mb-8">
        AI-Powered Quiz Platform - 100% Free
      </p>
      <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
        <div className="card">
          <h3 className="text-lg font-semibold mb-2">Create Quizzes</h3>
          <p className="text-gray-600">Generate personalized quizzes using AI</p>
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold mb-2">Take Quizzes</h3>
          <p className="text-gray-600">Test your knowledge with interactive quizzes</p>
        </div>
        <div className="card">
          <h3 className="text-lg font-semibold mb-2">Compete</h3>
          <p className="text-gray-600">Join leaderboards and compete with others</p>
        </div>
      </div>
    </div>
  )
}

export default Home 