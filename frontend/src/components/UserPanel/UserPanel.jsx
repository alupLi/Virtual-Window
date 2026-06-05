import { useApp } from '../../context/AppContext'
import AuthForm from '../Auth/Auth'
import * as api from '../../api/endpoints'
import './UserPanel.css'

export default function UserPanel() {
  const { user, setUser, favorites, locations, scenes,
          selectLocation, selectScene, setOpenPanel } = useApp()

  const handleLogout = async () => {
    await api.logout().catch(() => {})
    setUser(null)
    setOpenPanel(null)
  }

  const openFav = (fav) => {
    if (fav.location_id) {
      const loc = locations.find(l => l.id === fav.location_id)
      if (loc) { selectLocation(loc); setOpenPanel(null) }
    } else {
      const sc = scenes.find(s => s.id === fav.scene_id)
      if (sc) { selectScene(sc); setOpenPanel(null) }
    }
  }

  const favLocations = favorites.filter(f => f.location_id)
  const favScenes    = favorites.filter(f => f.scene_id)

  return (
    <div className="user-panel glass" onClick={e => e.stopPropagation()}>
      <button className="user-panel__close" onClick={() => setOpenPanel(null)}>✕</button>

      {!user ? (
        <>
          <p className="user-panel__heading">Аккаунт</p>
          <AuthForm onSuccess={(userData) => setUser(userData)} />
        </>
      ) : (
        <>
          <div className="user-panel__profile">
            <div className="user-panel__avatar">
              {user.username.charAt(0).toUpperCase()}
            </div>
            <div>
              <p className="user-panel__name">{user.username}</p>
              <p className="user-panel__email ellipsis">{user.email}</p>
            </div>
          </div>

          {(favLocations.length > 0 || favScenes.length > 0) && (
            <div className="user-panel__favs">
              <p className="user-panel__section">ИЗБРАННОЕ</p>

              {favLocations.map(fav => {
                const loc = locations.find(l => l.id === fav.location_id)
                if (!loc) return null
                return (
                  <div key={fav.id} className="user-panel__fav-item" onClick={() => openFav(fav)}>
                    <span className="user-panel__fav-icon">☆</span>
                    <span className="ellipsis">{loc.name}</span>
                  </div>
                )
              })}

              {favScenes.map(fav => {
                const sc = scenes.find(s => s.id === fav.scene_id)
                if (!sc) return null
                return (
                  <div key={fav.id} className="user-panel__fav-item" onClick={() => openFav(fav)}>
                    <span className="user-panel__fav-icon">☆</span>
                    <span className="ellipsis">{sc.name}</span>
                  </div>
                )
              })}
            </div>
          )}

          <div style={{ flex: 1 }} />

          <button className="user-panel__logout" onClick={handleLogout}>
            ⎋ Выйти
          </button>
        </>
      )}
    </div>
  )
}
