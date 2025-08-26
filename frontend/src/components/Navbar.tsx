import { Link } from 'react-router-dom'

const Navbar = () => {
  return (
    <nav className="bg-white shadow-soft">
      <div className="container mx-auto px-8">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
            Quiz
          </Link>
          <div className="flex space-x-8">
            <Link to="/" className="text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200">
              Home
            </Link>
            <Link to="/dashboard" className="text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200">
              Dashboard
            </Link>
            <Link to="/leaderboard" className="text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200">
              Leaderboard
            </Link>
            <Link to="/login" className="text-gray-700 hover:text-primary-600 font-medium transition-colors duration-200">
              Login
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar 