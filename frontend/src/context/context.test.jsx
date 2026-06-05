import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

vi.mock('../api/endpoints', () => ({
  getMe:       vi.fn().mockRejectedValue(new Error('not auth')),
  getLocations:vi.fn().mockResolvedValue({ data: [
    { id: 1, name: 'Норвегия', country: 'Норвегия', latitude: 61, longitude: 7,
      timezone: 'Europe/Oslo', bg_image: '/norway.jpg' },
  ]}),
  getScenes:   vi.fn().mockResolvedValue({ data: [] }),
  getTracks:   vi.fn().mockResolvedValue({ data: [] }),
  getWeather:  vi.fn().mockResolvedValue({ data: {
    time_of_day: 'day', weather_code: 0, is_raining: false,
    is_snowing: false, is_foggy: false, temperature: 18
  }}),
  getSounds:   vi.fn().mockResolvedValue({ data: [] }),
  getFavorites:vi.fn().mockResolvedValue({ data: [] }),
  getSettings: vi.fn().mockResolvedValue({ data: { volume_sounds: 0.7, volume_music: 0.4 } }),
  updateSettings: vi.fn().mockResolvedValue({}),
  addFavorite:    vi.fn(),
  removeFavorite: vi.fn(),
}))
vi.mock('../api/client', () => ({ default: {} }))

import { AppProvider, useApp } from './AppContext'
import * as endpoints from '../api/endpoints'

function TestConsumer() {
  const { locations, activeLocation, selectLocation, openPanel, togglePanel } = useApp()
  return (
    <div>
      <span data-testid="loc-count">{locations.length}</span>
      <span data-testid="active-loc">{activeLocation?.name || 'none'}</span>
      <span data-testid="open-panel">{openPanel || 'none'}</span>
      <button onClick={() => selectLocation(locations[0])}>select-first</button>
      <button onClick={() => togglePanel('location')}>toggle-loc</button>
      <button onClick={() => togglePanel('sound')}>toggle-sound</button>
    </div>
  )
}

function renderWithContext() {
  return render(<AppProvider><TestConsumer /></AppProvider>)
}

describe('AppContext — глобальный стейт', () => {
  beforeEach(() => { vi.clearAllMocks()
    endpoints.getMe.mockRejectedValue(new Error('not auth'))
    endpoints.getLocations.mockResolvedValue({ data: [
      { id: 1, name: 'Норвегия', country: 'Норвегия', latitude: 61, longitude: 7,
        timezone: 'Europe/Oslo', bg_image: '/norway.jpg' },
    ]})
    endpoints.getScenes.mockResolvedValue({ data: [] })
    endpoints.getTracks.mockResolvedValue({ data: [] })
    endpoints.getWeather.mockResolvedValue({ data: {
      time_of_day: 'day', weather_code: 0, is_raining: false,
      is_snowing: false, is_foggy: false, temperature: 18
    }})
    endpoints.getSounds.mockResolvedValue({ data: [] })
  })

  it('загружает локации при инициализации', async () => {
    renderWithContext()
    await waitFor(() => { expect(screen.getByTestId('loc-count').textContent).toBe('1') })
  })

  it('активная локация изначально отсутствует', async () => {
    renderWithContext()
    await waitFor(() => { expect(screen.getByTestId('active-loc').textContent).toBe('none') })
  })

  it('selectLocation устанавливает активную локацию', async () => {
    renderWithContext()
    await waitFor(() => expect(screen.getByTestId('loc-count').textContent).toBe('1'))
    await userEvent.click(screen.getByText('select-first'))
    await waitFor(() => { expect(screen.getByTestId('active-loc').textContent).toBe('Норвегия') })
  })

  it('selectLocation запрашивает погоду', async () => {
    renderWithContext()
    await waitFor(() => expect(screen.getByTestId('loc-count').textContent).toBe('1'))
    await userEvent.click(screen.getByText('select-first'))
    await waitFor(() => { expect(endpoints.getWeather).toHaveBeenCalledWith(1) })
  })

  it('togglePanel открывает панель', async () => {
    renderWithContext()
    expect(screen.getByTestId('open-panel').textContent).toBe('none')
    await userEvent.click(screen.getByText('toggle-loc'))
    expect(screen.getByTestId('open-panel').textContent).toBe('location')
  })

  it('togglePanel закрывает уже открытую панель', async () => {
    renderWithContext()
    await userEvent.click(screen.getByText('toggle-loc'))
    await userEvent.click(screen.getByText('toggle-loc'))
    expect(screen.getByTestId('open-panel').textContent).toBe('none')
  })

  it('переключение панели закрывает предыдущую', async () => {
    renderWithContext()
    await userEvent.click(screen.getByText('toggle-loc'))
    await userEvent.click(screen.getByText('toggle-sound'))
    expect(screen.getByTestId('open-panel').textContent).toBe('sound')
  })
})
