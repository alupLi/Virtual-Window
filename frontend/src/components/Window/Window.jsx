import { useApp } from '../../context/AppContext'
import WeatherOverlay from '../WeatherOverlay/WeatherOverlay'
import './Window.css'

const PLACEHOLDER = {
  morning: 'linear-gradient(160deg,#1a1000 0%,#3d2500 40%,#7a4a15 70%,#c08030 100%)',
  day:     'linear-gradient(160deg,#080f1e 0%,#0c2240 40%,#163d6a 70%,#22608a 100%)',
  evening: 'linear-gradient(160deg,#0c0408 0%,#280b18 40%,#551828 70%,#802018 100%)',
  night:   'linear-gradient(160deg,#010306 0%,#040a14 40%,#081020 70%,#0c1830 100%)',
  default: 'linear-gradient(160deg,#080a10 0%,#0e1220 50%,#141a30 100%)',
}

export default function Window() {
  const { activeLocation, activeScene, weather, weatherLoading, openPanel, setOpenPanel } = useApp()

  const bgImage = activeLocation?.bg_image || activeScene?.bg_image || null
  const tod = weather?.time_of_day || 'default'

  const style = bgImage
    ? { backgroundImage: `url(http://localhost:8000${bgImage})` }
    : { background: PLACEHOLDER[tod] }

  const handleClick = () => setOpenPanel(null)

  return (
    <div className="window" style={style} onClick={handleClick}>
      <div className="window__vignette" />
      <WeatherOverlay weather={weather} />

      {weatherLoading && <div className="window__shimmer" />}

      {!activeLocation && !activeScene && (
        <div className="window__empty">
          <p className="window__empty-title">Виртуальное окно</p>
          <p className="window__empty-hint">Выберите локацию или сцену</p>
        </div>
      )}

      {(activeLocation || activeScene) && (
        <div className="window__caption">
          <span className="window__caption-name"></span>
          {activeLocation && weather && (
            <span className="window__caption-meta"></span>
          )}
        </div>
      )}
    </div>
  )
}
