import { useApp } from './context/AppContext'
import Header from './components/Header/Header'
import Window from './components/Window/Window'
import LocationDropdown from './components/LocationDropdown/LocationDropdown'
import SoundPanel from './components/SoundPanel/SoundPanel'
import BreathingOverlay from './components/BreathingOverlay/BreathingOverlay'
import UserPanel from './components/UserPanel/UserPanel'
import './styles/globals.css'
import './App.css'

export default function App() {
  const { authLoading, openPanel } = useApp()

  if (authLoading) {
    return (
      <div className="app-loading">
        <span className="app-loading__text">Virtual Window</span>
      </div>
    )
  }

  return (
    <div className="app">
      <Window />

      <Header />

      {openPanel === 'location'  && <LocationDropdown />}
      {openPanel === 'sound'     && <SoundPanel />}
      {openPanel === 'breathing' && <BreathingOverlay />}
      {openPanel === 'user'      && <UserPanel />}
    </div>
  )
}
