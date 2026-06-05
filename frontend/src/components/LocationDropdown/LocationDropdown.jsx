import { useState } from 'react'
import { useApp } from '../../context/AppContext'
import './LocationDropdown.css'

export default function LocationDropdown() {
  const { locations, scenes, activeLocation, activeScene, selectLocation, selectScene,
          toggleFavorite, isFavorite, user, setOpenPanel } = useApp()
  const [tab, setTab] = useState('real')

  const pick = (fn, item) => {
    fn(item)
    setOpenPanel(null)
  }

  return (
    <div className="loc-drop glass" onClick={e => e.stopPropagation()}>
      <div className="loc-drop__tabs">
        <button
          className={`loc-drop__tab ${tab === 'real' ? 'loc-drop__tab--active' : ''}`}
          onClick={() => setTab('real')}
        >
          Реальные места
        </button>
        <button
          className={`loc-drop__tab ${tab === 'fictional' ? 'loc-drop__tab--active' : ''}`}
          onClick={() => setTab('fictional')}
        >
          Вымышленные
        </button>
      </div>

      <div className="loc-drop__cards">
        {tab === 'real' && locations.map(loc => {
          const active = activeLocation?.id === loc.id
          const fav = isFavorite('location', loc.id)
          return (
            <div
              key={loc.id}
              className={`loc-card ${active ? 'loc-card--active' : ''}`}
              onClick={() => pick(selectLocation, active ? null : loc)}
            >
              <div
                className="loc-card__thumb"
                style={{ backgroundImage: `url(http://localhost:8000${loc.bg_image})` }}
              />
              <span className="loc-card__name ellipsis">{loc.name}</span>
              <span className="loc-card__sub ellipsis">{loc.country}</span>
              {user && (
                <button
                  className={`loc-card__fav ${fav ? 'loc-card__fav--on' : ''}`}
                  onClick={e => { e.stopPropagation(); toggleFavorite('location', loc.id) }}
                >
                  {fav ? '♥' : '♡'}
                </button>
              )}
            </div>
          )
        })}

        {tab === 'fictional' && scenes.map(scene => {
          const active = activeScene?.id === scene.id
          const fav = isFavorite('scene', scene.id)
          return (
            <div
              key={scene.id}
              className={`loc-card ${active ? 'loc-card--active' : ''}`}
              onClick={() => pick(selectScene, active ? null : scene)}
            >
              <div
                className="loc-card__thumb"
                style={{ backgroundImage: `url(http://localhost:8000${scene.preview_image})` }}
              />
              <span className="loc-card__name ellipsis">{scene.name}</span>
              {scene.description && (
                <span className="loc-card__sub ellipsis">{scene.description}</span>
              )}
              {user && (
                <button
                  className={`loc-card__fav ${fav ? 'loc-card__fav--on' : ''}`}
                  onClick={e => { e.stopPropagation(); toggleFavorite('scene', scene.id) }}
                >
                  {fav ? '♥' : '♡'}
                </button>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
