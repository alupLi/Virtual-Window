import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import * as api from '../api/endpoints'

const AppContext = createContext(null)

export function AppProvider({ children }) {
  const [user, setUser]               = useState(null)
  const [authLoading, setAuthLoading] = useState(true)

  const [locations, setLocations] = useState([])
  const [scenes, setScenes]       = useState([])
  const [tracks, setTracks]       = useState([])
  const [favorites, setFavorites] = useState([])

  const [activeLocation, setActiveLocation] = useState(null)
  const [activeScene, setActiveScene]       = useState(null)
  const [weather, setWeather]               = useState(null)
  const [weatherLoading, setWeatherLoading] = useState(false)
  const [sounds, setSounds]                 = useState([])

  const [activeTrack, setActiveTrack]     = useState(null)
  const [isPlaying, setIsPlaying]         = useState(false)
  const [volumeSounds, setVolumeSounds]   = useState(0.7)
  const [volumeMusic, setVolumeMusic]     = useState(0.4)
  const [activeSoundIds, setActiveSoundIds] = useState([])

  const [openPanel, setOpenPanel] = useState(null)

  const togglePanel = useCallback((name) => {
    setOpenPanel(prev => prev === name ? null : name)
  }, [])

  // Init
  useEffect(() => {
    api.getMe().then(r => setUser(r.data)).catch(() => setUser(null)).finally(() => setAuthLoading(false))
    api.getLocations().then(r => setLocations(r.data)).catch(() => {})
    api.getScenes().then(r => setScenes(r.data)).catch(() => {})
    api.getTracks().then(r => setTracks(r.data)).catch(() => {})
  }, [])

  useEffect(() => {
    if (!user) { setFavorites([]); return }
    api.getFavorites().then(r => setFavorites(r.data)).catch(() => {})
    api.getSettings().then(r => {
      const s = r.data
      setVolumeSounds(s.volume_sounds ?? 0.7)
      setVolumeMusic(s.volume_music ?? 0.4)
      if (s.last_location_id) {
        api.getLocation(s.last_location_id).then(lr => selectLocation(lr.data)).catch(() => {})
      }
    }).catch(() => {})
  }, [user])

  // Select location
  const selectLocation = useCallback(async (loc) => {
    setActiveLocation(loc)
    setActiveScene(null)
    setWeather(null)
    setSounds([])
    if (!loc) return
    setWeatherLoading(true)
    try {
      const [wRes, sRes] = await Promise.all([
        api.getWeather(loc.id),
        api.getSounds({ locationId: loc.id }),
      ])
      setWeather(wRes.data)
      setSounds(sRes.data)
    } catch { } finally { setWeatherLoading(false) }
    if (user) api.updateSettings({ last_location_id: loc.id, last_scene_id: null }).catch(() => {})
  }, [user])

  const selectScene = useCallback(async (scene) => {
    setActiveScene(scene)
    setActiveLocation(null)
    setWeather(null)
    setSounds([])
    if (!scene) return
    try {
      const sRes = await api.getSounds({ sceneId: scene.id })
      setSounds(sRes.data)
    } catch { }
    if (user) api.updateSettings({ last_scene_id: scene.id, last_location_id: null }).catch(() => {})
  }, [user])

  // Favorites
  const toggleFavorite = useCallback(async (type, id) => {
    if (!user) return
    const existing = favorites.find(f => type === 'location' ? f.location_id === id : f.scene_id === id)
    if (existing) {
      await api.removeFavorite(existing.id)
      setFavorites(prev => prev.filter(f => f.id !== existing.id))
    } else {
      const body = type === 'location' ? { location_id: id } : { scene_id: id }
      const res = await api.addFavorite(body)
      setFavorites(prev => [...prev, res.data])
    }
  }, [user, favorites])

  const isFavorite = useCallback((type, id) =>
    favorites.some(f => type === 'location' ? f.location_id === id : f.scene_id === id)
  , [favorites])

  const setVolumeSoundsAndSave = useCallback((v) => {
    setVolumeSounds(v)
    if (user) api.updateSettings({ volume_sounds: v }).catch(() => {})
  }, [user])

  const setVolumeMusicAndSave = useCallback((v) => {
    setVolumeMusic(v)
    if (user) api.updateSettings({ volume_music: v }).catch(() => {})
  }, [user])

  const selectTrack = useCallback((track) => {
    setActiveTrack(track)
    setIsPlaying(true)
    if (user && track) api.updateSettings({ last_track_id: track.id }).catch(() => {})
  }, [user])

  const toggleSound = useCallback((id) => {
    setActiveSoundIds(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id])
  }, [])

  return (
    <AppContext.Provider value={{
      user, setUser, authLoading,
      locations, scenes, tracks, favorites,
      activeLocation, activeScene, weather, weatherLoading, sounds,
      activeTrack, isPlaying, setIsPlaying,
      volumeSounds, setVolumeSounds: setVolumeSoundsAndSave,
      volumeMusic,  setVolumeMusic:  setVolumeMusicAndSave,
      activeSoundIds, toggleSound,
      openPanel, togglePanel, setOpenPanel,
      selectLocation, selectScene, selectTrack,
      toggleFavorite, isFavorite,
    }}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)