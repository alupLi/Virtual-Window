import { useEffect, useRef } from 'react'
import { useApp } from '../../context/AppContext'
import './SoundPanel.css'

const MOOD = { calm: 'Спокойная', ambient: 'Амбиент', lofi: 'Lo-Fi' }

export default function SoundPanel() {
  const {
    tracks, activeTrack, selectTrack, isPlaying, setIsPlaying,
    volumeMusic, setVolumeMusic,
    sounds, activeSoundIds, toggleSound, volumeSounds, setVolumeSounds,
  } = useApp()

  const audioRef = useRef(null)

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return
    if (!activeTrack) { audio.pause(); return }
    const src = `http://localhost:8000${activeTrack.file_path}`
    if (audio.src !== src) { audio.src = src; audio.load() }
    isPlaying ? audio.play().catch(() => {}) : audio.pause()
  }, [activeTrack, isPlaying])

  useEffect(() => {
    if (audioRef.current) audioRef.current.volume = volumeMusic
  }, [volumeMusic])

  const handleTrack = (track) => {
    if (activeTrack?.id === track.id) setIsPlaying(!isPlaying)
    else selectTrack(track)
  }

  const prevTrack = () => {
    if (!tracks.length) return
    const idx = tracks.findIndex(t => t.id === activeTrack?.id)
    selectTrack(tracks[(idx - 1 + tracks.length) % tracks.length])
  }
  const nextTrack = () => {
    if (!tracks.length) return
    const idx = tracks.findIndex(t => t.id === activeTrack?.id)
    selectTrack(tracks[(idx + 1) % tracks.length])
  }

  const ambientSounds = sounds.filter(s => !s.weather_condition)
  const weatherSounds = sounds.filter(s => s.weather_condition)

  return (
    <div className="sound-panel glass" onClick={e => e.stopPropagation()}>
      <div className="sound-panel__music">
        <p className="sound-panel__section-label">МУЗЫКА</p>

        <p className="sound-panel__track-title ellipsis">
          {activeTrack?.title || 'Не выбрано'}
        </p>
        {activeTrack?.mood_tag && (
          <p className="sound-panel__track-tag">{MOOD[activeTrack.mood_tag] || activeTrack.mood_tag}</p>
        )}

        <div className="sound-panel__controls">
          <button className="sound-panel__ctrl" onClick={prevTrack} title="Назад">⏮</button>
          <button
            className="sound-panel__ctrl sound-panel__ctrl--play"
            onClick={() => {
              if (!activeTrack && tracks.length) selectTrack(tracks[0])
              else setIsPlaying(!isPlaying)
            }}
          >
            {isPlaying ? '⏸' : '▶'}
          </button>
          <button className="sound-panel__ctrl" onClick={nextTrack} title="Вперёд">⏭</button>
        </div>

        <div className="sound-panel__vol-row">
          <span className="sound-panel__vol-icon">♫</span>
          <input
            type="range" min={0} max={1} step={0.01}
            value={volumeMusic}
            onChange={e => setVolumeMusic(parseFloat(e.target.value))}
            className="sound-panel__slider"
          />
        </div>

        <div className="sound-panel__track-list">
          {tracks.map(t => (
            <div
              key={t.id}
              className={`sound-panel__track-row ${activeTrack?.id === t.id ? 'sound-panel__track-row--active' : ''}`}
              onClick={() => handleTrack(t)}
            >
              <span className="sound-panel__track-play">
                {activeTrack?.id === t.id && isPlaying ? '▮▮' : '▶'}
              </span>
              <span className="sound-panel__track-name ellipsis">{t.title}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="sound-panel__divider" />

      <div className="sound-panel__ambient">
        <p className="sound-panel__section-label">ЗВУКИ ОКРУЖЕНИЯ</p>

        <div className="sound-panel__vol-row">
          <span className="sound-panel__vol-icon">◈</span>
          <input
            type="range" min={0} max={1} step={0.01}
            value={volumeSounds}
            onChange={e => setVolumeSounds(parseFloat(e.target.value))}
            className="sound-panel__slider"
          />
        </div>

        {sounds.length === 0 && (
          <p className="sound-panel__empty">Выберите локацию<br />для звуков</p>
        )}

        {ambientSounds.length > 0 && (
          <>
            <p className="sound-panel__sub-label">Активные звуки</p>
            {ambientSounds.map(s => (
              <SoundToggle key={s.id} sound={s} active={activeSoundIds.includes(s.id)} onToggle={toggleSound} />
            ))}
          </>
        )}

        {weatherSounds.length > 0 && (
          <>
            <p className="sound-panel__sub-label">Погода</p>
            {weatherSounds.map(s => (
              <SoundToggle key={s.id} sound={s} active={activeSoundIds.includes(s.id)} onToggle={toggleSound} />
            ))}
          </>
        )}
      </div>

      <audio ref={audioRef} loop />
    </div>
  )
}

function SoundToggle({ sound, active, onToggle }) {
  return (
    <div
      className={`sound-toggle ${active ? 'sound-toggle--on' : ''}`}
      onClick={() => onToggle(sound.id)}
    >
      <span className="sound-toggle__name">{sound.name}</span>
      <span className="sound-toggle__dot" />
    </div>
  )
}
