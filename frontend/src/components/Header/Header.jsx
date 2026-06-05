import { useState, useEffect } from 'react'
import { useApp } from '../../context/AppContext'
import './Header.css'

function Clock() {
  const [time, setTime] = useState(new Date())
  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(t)
  }, [])
  return (
    <span className="hdr__clock">
      {time.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })}
    </span>
  )
}

export default function Header() {
  const { openPanel, togglePanel, user, activeLocation, activeScene } = useApp()

  const currentName = activeLocation?.name || activeScene?.name || null

  return (
    <header className="hdr glass">
      <div className="hdr__left">
        <span className="hdr__logo">Virtual Window</span>
      </div>

      <div className="hdr__right">
        <button
          className={`hdr__pill ${openPanel === 'location' ? 'hdr__pill--active' : ''}`}
          onClick={(e) => { e.stopPropagation(); togglePanel('location') }}
          title="Выбрать локацию"
        >
          <span className="hdr__pill-icon">◎</span>
          <span className="hdr__pill-label ellipsis">
            {currentName || 'Выбрать место'}
          </span>
          <span className="hdr__pill-caret">{openPanel === 'location' ? '∧' : '∨'}</span>
        </button>

        <button
          className={`hdr__icon-btn ${openPanel === 'sound' ? 'hdr__icon-btn--active' : ''}`}
          onClick={(e) => { e.stopPropagation(); togglePanel('sound') }}
          title="Звук и музыка"
        >
          ♫
        </button>

        <button
          className={`hdr__icon-btn ${openPanel === 'breathing' ? 'hdr__icon-btn--active' : ''}`}
          onClick={(e) => { e.stopPropagation(); togglePanel('breathing') }}
          title="Дыхательная гимнастика"
        >
          ◯
        </button>

        <button
          className={`hdr__avatar-btn ${openPanel === 'user' ? 'hdr__avatar-btn--active' : ''}`}
          onClick={(e) => { e.stopPropagation(); togglePanel('user') }}
          title={user ? user.username : 'Войти'}
        >
          {user
            ? <span className="hdr__avatar-letter">{user.username.charAt(0).toUpperCase()}</span>
            : <span className="hdr__avatar-icon">⊙</span>
          }
        </button>
      </div>
    </header>
  )
}
