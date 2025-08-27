import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { quizAPI, Quiz, QuizAttempt } from '../services/api'

const QuizTaker = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [quiz, setQuiz] = useState<Quiz | null>(null)
  const [quizAttempt, setQuizAttempt] = useState<QuizAttempt | null>(null)
  const [selectedAnswer, setSelectedAnswer] = useState<number>(-1)
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<number[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>('')
  const [isFinished, setIsFinished] = useState(false)
  const [startTime, setStartTime] = useState<Date | null>(null)

  useEffect(() => {
    if (!user) {
      navigate('/login')
      return
    }

    const fetchQuizAndStartAttempt = async () => {
      try {
        if (!id) {
          setError('Quiz ID is required')
          return
        }

        // Fetch the real quiz from the backend
        const fetchedQuiz = await quizAPI.getById(id)
        setQuiz(fetchedQuiz)
        setAnswers(new Array(fetchedQuiz.questions.length).fill(-1))
        setStartTime(new Date())

        // Start quiz attempt
        const attempt = await quizAPI.startAttempt(id)
        setQuizAttempt(attempt)
      } catch (error) {
        console.error('Failed to load quiz:', error)
        const errorMessage = error instanceof Error ? error.message : 'Failed to load quiz'
        if (errorMessage.includes('Quiz not found')) {
          setError(`Quiz not found. Please use a valid quiz ID from the dashboard, or create a quiz first.`)
        } else {
          setError(errorMessage)
        }
      } finally {
        setLoading(false)
      }
    }

    fetchQuizAndStartAttempt()
  }, [id, user, navigate])

  const handleAnswerSelect = (answerIndex: number) => {
    setSelectedAnswer(answerIndex)
  }

  const handleNext = () => {
    if (selectedAnswer === -1 || !quiz) return

    // Save the current answer
    const newAnswers = [...answers]
    newAnswers[currentQuestion] = selectedAnswer
    setAnswers(newAnswers)

    if (currentQuestion < quiz.questions.length - 1) {
      // Move to next question
      setCurrentQuestion(currentQuestion + 1)
      setSelectedAnswer(newAnswers[currentQuestion + 1] !== -1 ? newAnswers[currentQuestion + 1] : -1)
    } else {
      // Finish quiz
      handleFinishQuiz(newAnswers)
    }
  }

  const handleFinishQuiz = async (finalAnswers: number[]) => {
    if (!quiz || !quizAttempt || !startTime) return

    try {
      // Calculate time taken in seconds
      const endTime = new Date()
      const timeTakenSeconds = Math.round((endTime.getTime() - startTime.getTime()) / 1000)
      
      // Submit quiz results to backend
      const submittedAttempt = await quizAPI.submitQuiz(quiz.id, finalAnswers, timeTakenSeconds)
      setQuizAttempt(submittedAttempt)
      setIsFinished(true)

      console.log('Quiz completed and submitted:', {
        quizId: quiz.id,
        attemptId: submittedAttempt.id,
        answers: finalAnswers,
        score: submittedAttempt.score,
        timeTaken: timeTakenSeconds,
        correctAnswers: submittedAttempt.correct_answers,
        totalQuestions: quiz.questions.length
      })

      // Show results for 4 seconds, then redirect to dashboard
      setTimeout(() => {
        navigate('/dashboard')
      }, 4000)

    } catch (error) {
      console.error('Failed to submit quiz:', error)
      setError('Failed to submit quiz results')
    }
  }

  const progressPercentage = quiz ? ((currentQuestion + 1) / quiz.questions.length) * 100 : 0

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-bg flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading quiz...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-bg flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Quiz Error</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={() => navigate('/dashboard')}
            className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    )
  }

  if (!quiz) {
    return (
      <div className="min-h-screen bg-gradient-bg flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Quiz not found</p>
        </div>
      </div>
    )
  }

  if (isFinished && quizAttempt) {
    return (
      <div className="min-h-screen bg-gradient-bg flex items-center justify-center">
        <div className="bg-white rounded-2xl shadow-card p-8 max-w-md w-full mx-4 text-center">
          <div className="text-6xl mb-4">🎉</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Quiz Complete!</h2>
          <p className="text-gray-600 mb-4">Great job finishing the quiz!</p>
          
          <div className="bg-gray-50 rounded-xl p-4 mb-4">
            <div className="text-3xl font-bold text-primary-600 mb-1">
              {quizAttempt.score}/{quizAttempt.max_score}
            </div>
            <p className="text-sm text-gray-600">Your Score</p>
          </div>
          
          <div className="grid grid-cols-2 gap-4 text-sm text-gray-600 mb-4">
            <div>
              <div className="font-semibold text-green-600">{quizAttempt.correct_answers}</div>
              <div>Correct</div>
            </div>
            <div>
              <div className="font-semibold text-red-600">{quizAttempt.incorrect_answers}</div>
              <div>Incorrect</div>
            </div>
          </div>
          
          <div className="text-sm text-gray-600 mb-4">
            <div className="font-semibold">{quizAttempt.percentage.toFixed(1)}%</div>
            <div>Accuracy</div>
          </div>
          
          <div className="text-sm text-gray-600 mb-4">
            Time taken: {Math.floor(quizAttempt.time_taken / 60)}m {quizAttempt.time_taken % 60}s
          </div>
          
          <p className="text-sm text-gray-500">Your stats have been updated! Redirecting to dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-bg flex flex-col">
      {/* Header */}
      <div className="text-center py-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">{quiz.title}</h1>
        <p className="text-gray-600">Question {currentQuestion + 1} of {quiz.questions.length}</p>
      </div>

      {/* Quiz Container */}
      <div className="flex-1 flex justify-center items-center px-4 pb-20">
        <div className="w-full max-w-2xl">
          {/* Quiz Card */}
          <div className="bg-white rounded-2xl shadow-card p-8">
            {/* Progress Bar */}
            <div className="mb-8">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-gradient-primary h-2 rounded-full transition-all duration-300 ease-out"
                  style={{ width: `${progressPercentage}%` }}
                ></div>
              </div>
            </div>

            {/* Question */}
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-gray-800 leading-relaxed">
                {quiz.questions[currentQuestion].question}
              </h2>
            </div>

            {/* Answer Options */}
            <div className="space-y-4 mb-8">
              {quiz.questions[currentQuestion].options.map((option: string, index: number) => (
                <label
                  key={index}
                  className={`block cursor-pointer transition-all duration-200 ${
                    selectedAnswer === index
                      ? 'bg-primary-50 border-primary-500'
                      : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                  } border-2 rounded-xl p-4`}
                >
                  <input
                    type="radio"
                    name="answer"
                    value={index}
                    checked={selectedAnswer === index}
                    onChange={() => handleAnswerSelect(index)}
                    className="sr-only"
                  />
                  <div className="flex items-center">
                    <div className={`w-5 h-5 rounded-full border-2 mr-3 flex items-center justify-center ${
                      selectedAnswer === index
                        ? 'border-primary-500 bg-primary-500'
                        : 'border-gray-300'
                    }`}>
                      {selectedAnswer === index && (
                        <div className="w-2 h-2 bg-white rounded-full"></div>
                      )}
                    </div>
                    <span className="text-gray-800 font-medium">{option}</span>
                  </div>
                </label>
              ))}
            </div>

            {/* Navigation Buttons */}
            <div className="flex gap-4">
              {currentQuestion > 0 && (
                <button
                  onClick={() => {
                    const newAnswers = [...answers]
                    newAnswers[currentQuestion] = selectedAnswer
                    setAnswers(newAnswers)
                    setCurrentQuestion(currentQuestion - 1)
                    setSelectedAnswer(answers[currentQuestion - 1] !== -1 ? answers[currentQuestion - 1] : -1)
                  }}
                  className="px-6 py-4 border-2 border-primary-600 text-primary-600 font-semibold rounded-xl hover:bg-primary-50 transition-all duration-200"
                >
                  Previous
                </button>
              )}
              
              <button
                onClick={handleNext}
                disabled={selectedAnswer === -1}
                className={`flex-1 py-4 px-6 rounded-xl font-semibold text-white transition-all duration-200 ${
                  selectedAnswer !== -1
                    ? 'bg-gradient-primary hover:opacity-90 transform hover:scale-[1.02]'
                    : 'bg-gray-300 cursor-not-allowed'
                }`}
              >
                {currentQuestion === quiz.questions.length - 1 ? 'Finish Quiz' : 'Next Question'}
              </button>
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

export default QuizTaker 