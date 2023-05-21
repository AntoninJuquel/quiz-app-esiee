import type { Difficulty } from '@/types/quiz'

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
