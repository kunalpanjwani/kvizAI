import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const Navbar = () => {
  const { user, logout } = useAuth()

  return (
    <nav className="bg-white shadow-soft">
      <div className="container mx-auto px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            kvizAI
          </Link>
          <div className="flex items-center space-x-8">
            <Link to="/" className="text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200">
              Home
            </Link>
            
            {user ? (
              // Authenticated user menu
              <>
                <Link to="/dashboard" className="text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200">
                  Dashboard
                </Link>
                <Link to="/create-quiz" className="text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200">
                  Create Quiz
                </Link>
                <Link to="/leaderboard" className="text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200">
                  Leaderboard
                </Link>
                
                <div className="flex items-center space-x-4">
                  <span className="text-gray-600 text-sm">Hi, {user.username}!</span>
                  <button
                    onClick={logout}
                    className="px-4 py-2 text-sm bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                  >
                    Logout
                  </button>
                </div>
              </>
            ) : (
              // Guest user menu
              <>
                <Link to="/leaderboard" className="text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200">
                  Leaderboard
                </Link>
                <Link to="/login" className="text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200">
                  Login
                </Link>
                <Link to="/register" className="px-4 py-2 bg-gradient-primary text-white rounded-lg hover:opacity-90 transition-opacity">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar 