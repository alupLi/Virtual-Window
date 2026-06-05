import { useMemo } from 'react'
import './WeatherOverlay.css'

export default function WeatherOverlay({ weather }) {
  const rainDrops = useMemo(() => Array.from({ length: 90 }, () => ({
    left: `${Math.random() * 110 - 5}%`,
    animationDelay: `${Math.random() * 2}s`,
    animationDuration: `${0.5 + Math.random() * 0.5}s`,
    opacity: 0.3 + Math.random() * 0.4,
  })), [])

  const snowFlakes = useMemo(() => Array.from({ length: 65 }, () => ({
    left: `${Math.random() * 110 - 5}%`,
    animationDelay: `${Math.random() * 5}s`,
    animationDuration: `${4 + Math.random() * 4}s`,
    width: `${3 + Math.random() * 5}px`,
    height: `${3 + Math.random() * 5}px`,
  })), [])

  if (!weather) return null

  return (
    <div className="weather-overlay">
      {weather.is_raining && (
        <div className="rain-layer">
          {rainDrops.map((s, i) => <div key={i} className="rain-drop" style={s} />)}
        </div>
      )}
      {weather.is_snowing && (
        <div className="snow-layer">
          {snowFlakes.map((s, i) => <div key={i} className="snow-flake" style={s} />)}
        </div>
      )}
      {weather.is_foggy && (
        <>
          <div className="fog-layer fog-1" />
          <div className="fog-layer fog-2" />
        </>
      )}
      <div className={`time-tint time-tint--${weather.time_of_day}`} />
    </div>
  )
}
