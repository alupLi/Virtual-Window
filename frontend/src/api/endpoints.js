import api from './client'

export const register    = (d) => api.post('/auth/register', d)
export const login       = (d) => api.post('/auth/login', d)
export const logout      = ()  => api.post('/auth/logout')
export const getMe       = ()  => api.get('/auth/me')

export const getLocations = ()   => api.get('/locations')
export const getLocation  = (id) => api.get(`/locations/${id}`)
export const getScenes    = ()   => api.get('/scenes')

export const getSounds = ({ locationId, sceneId } = {}) => {
  const params = {}
  if (locationId) params.location_id = locationId
  if (sceneId)    params.scene_id    = sceneId
  return api.get('/sounds', { params })
}

export const getTracks  = ()   => api.get('/music')
export const getWeather = (id) => api.get(`/weather/${id}`)

export const getFavorites   = ()   => api.get('/favorites')
export const addFavorite    = (d)  => api.post('/favorites', d)
export const removeFavorite = (id) => api.delete(`/favorites/${id}`)

export const getSettings    = ()  => api.get('/settings')
export const updateSettings = (d) => api.put('/settings', d)
