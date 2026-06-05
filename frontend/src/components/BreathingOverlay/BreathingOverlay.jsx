import { useState, useEffect, useRef } from 'react'
import './BreathingOverlay.css'

const PHASES = [
  { label: 'Вдох',      duration: 4, phase: 'in'   },
  { label: 'Задержка',  duration: 7, phase: 'hold' },
  { label: 'Выдох',     duration: 8, phase: 'out'  },
]
const TOTAL = PHASES.reduce((a, p) => a + p.duration, 0)

export default function BreathingOverlay() {
  const [tick, setTick]       = useState(0)
  const [seconds, setSeconds] = useState(0)
  const intervalRef = useRef(null)

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      setSeconds(s => (s + 1) % TOTAL)
      setTick(t => t + 1)
    }, 1000)
    return () => clearInterval(intervalRef.current)
  }, [])

  let elapsed = 0
  let currentPhase = PHASES[0]
  let phaseSecond = seconds
  for (const p of PHASES) {
    if (seconds < elapsed + p.duration) {
      currentPhase = p
      phaseSecond = seconds - elapsed
      break
    }
    elapsed += p.duration
  }

  const progress = phaseSecond / currentPhase.duration

  return (
    <div className="breathing-overlay" onClick={e => e.stopPropagation()}>
      <div className="breathing-overlay__fog" />
      <div className={`breathing-circle breathing-circle--${currentPhase.phase}`}>
        <div className="breathing-circle__ring" />
        <div className="breathing-circle__inner">
          <span className="breathing-circle__label">{currentPhase.label}...</span>
          <span className="breathing-circle__count">{currentPhase.duration - phaseSecond}</span>
        </div>
      </div>
      <p className="breathing-overlay__hint">Техника 4-7-8 · нажмите ◯ чтобы выйти</p>
    </div>
  )
}
