import type { Difficulty } from '@/types/quiz'

export function enumKeys<O extends object, K extends keyof O = keyof O>(obj: O): K[] {
  return Object.keys(obj).filter((k) => Number.isNaN(+k)) as K[]
}

export function difficultyToString(difficulty: Difficulty) {
  switch (difficulty) {
    case 1:
      return 'Facile'
    case 2:
      return 'Moyen'
    case 3:
      return 'Difficile'
  }
}

export function difficultyToEmoji(difficulty: Difficulty) {
  switch (difficulty) {
    case 1:
      return '🤓'
    case 2:
      return '😎'
    case 3:
      return '🤯'
  }
}

export function difficultyHint(difficulty: Difficulty) {
  switch (difficulty) {
    case 1:
      return 'Facile, pas de chrono'
    case 2:
      return 'Moyen, temps total 10 secondes par question'
    case 3:
      return 'Difficile, temps par question 5 secondes'
    default:
      return ''
  }
}

export function startDifficultyTimer(
  difficulty: Difficulty,
  numberOfQuestion: number,
  onTimeUpdate: (time: number) => void,
  answer: () => boolean,
  endQuiz: () => void
) {
  let clear = () => {}

  switch (difficulty) {
    case 1:
      break
    case 2: {
      let timeRemaining = numberOfQuestion * 10 + 1
      onTimeUpdate(timeRemaining)
      const interval = setInterval(() => {
        timeRemaining--
        onTimeUpdate(timeRemaining)
        if (timeRemaining <= 0) {
          endQuiz()
        }
      }, 1000)
      clear = () => {
        console.log('clearing')
        clearInterval(interval)
      }
      break
    }
    case 3: {
      let timeRemaining = 6
      onTimeUpdate(timeRemaining)
      const interval = setInterval(() => {
        timeRemaining--
        onTimeUpdate(timeRemaining)
        if (timeRemaining <= 0) {
          const quizEnded = answer()
          if (!quizEnded) {
            timeRemaining = 6
            onTimeUpdate(timeRemaining)
          }
        }
      }, 1000)
      clear = () => {
        console.log('clearing')
        clearInterval(interval)
      }
      break
    }
    default:
      break
  }

  return { clear }
}
