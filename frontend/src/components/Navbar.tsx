import { Link } from 'react-router-dom'

const Navbar = () => {
  return (
    <nav className="bg-white shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-xl font-bold text-primary-600">
            kvizAI
          </Link>
          <div className="flex space-x-4">
            <Link to="/" className="text-gray-700 hover:text-primary-600">
              Home
            </Link>
            <Link to="/dashboard" className="text-gray-700 hover:text-primary-600">
              Dashboard
            </Link>
            <Link to="/leaderboard" className="text-gray-700 hover:text-primary-600">
              Leaderboard
            </Link>
            <Link to="/login" className="text-gray-700 hover:text-primary-600">
              Login
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar 