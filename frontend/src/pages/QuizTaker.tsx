import { useState } from 'react'

const QuizTaker = () => {
  const [selectedAnswer, setSelectedAnswer] = useState<string>('')
  const [currentQuestion, setCurrentQuestion] = useState(0)
  
  // Mock quiz data - replace with actual data from your backend
  const mockQuiz = {
    title: "General Knowledge Quiz",
    questions: [
      {
        id: 1,
        question: "What is the capital of France?",
        options: ["Paris", "London", "Madrid", "Berlin"],
        correctAnswer: 0
      },
      {
        id: 2,
        question: "Which planet is known as the Red Planet?",
        options: ["Venus", "Mars", "Jupiter", "Saturn"],
        correctAnswer: 1
      },
      {
        id: 3,
        question: "What is the largest mammal in the world?",
        options: ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
        correctAnswer: 1
      }
    ]
  }

  const handleAnswerSelect = (answer: string) => {
    setSelectedAnswer(answer)
  }

  const handleNext = () => {
    if (selectedAnswer && currentQuestion < mockQuiz.questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
      setSelectedAnswer('')
    }
  }

  const progressPercentage = ((currentQuestion + 1) / mockQuiz.questions.length) * 100

  return (
    <div className="min-h-screen bg-gradient-bg flex flex-col">
      {/* Header */}
      <div className="text-center py-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">{mockQuiz.title}</h1>
        <p className="text-gray-600">Question {currentQuestion + 1} of {mockQuiz.questions.length}</p>
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
                {mockQuiz.questions[currentQuestion].question}
              </h2>
            </div>

            {/* Answer Options */}
            <div className="space-y-4 mb-8">
              {mockQuiz.questions[currentQuestion].options.map((option, index) => (
                <label
                  key={index}
                  className={`block cursor-pointer transition-all duration-200 ${
                    selectedAnswer === option
                      ? 'bg-primary-50 border-primary-500'
                      : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
                  } border-2 rounded-xl p-4`}
                >
                  <input
                    type="radio"
                    name="answer"
                    value={option}
                    checked={selectedAnswer === option}
                    onChange={() => handleAnswerSelect(option)}
                    className="sr-only"
                  />
                  <div className="flex items-center">
                    <div className={`w-5 h-5 rounded-full border-2 mr-3 flex items-center justify-center ${
                      selectedAnswer === option
                        ? 'border-primary-500 bg-primary-500'
                        : 'border-gray-300'
                    }`}>
                      {selectedAnswer === option && (
                        <div className="w-2 h-2 bg-white rounded-full"></div>
                      )}
                    </div>
                    <span className="text-gray-800 font-medium">{option}</span>
                  </div>
                </label>
              ))}
            </div>

            {/* Next Button */}
            <button
              onClick={handleNext}
              disabled={!selectedAnswer}
              className={`w-full py-4 px-6 rounded-xl font-semibold text-white transition-all duration-200 ${
                selectedAnswer
                  ? 'bg-gradient-primary hover:opacity-90 transform hover:scale-[1.02]'
                  : 'bg-gray-300 cursor-not-allowed'
              }`}
            >
              {currentQuestion === mockQuiz.questions.length - 1 ? 'Finish Quiz' : 'Next Question'}
            </button>
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