import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, act } from '@testing-library/react'
import BreathingOverlay from './BreathingOverlay'

describe('BreathingOverlay — таймер 4-7-8', () => {
  beforeEach(() => { vi.useFakeTimers() })
  afterEach(() => { vi.useRealTimers() })

  it('рендерится без ошибок', () => {
    render(<BreathingOverlay />)
    expect(screen.getByText(/Вдох/i)).toBeInTheDocument()
  })

  it('показывает обратный отсчёт фазы Вдох — 4 секунды', () => {
    render(<BreathingOverlay />)
    expect(screen.getByText('4')).toBeInTheDocument()
  })

  it('уменьшает счётчик каждую секунду', () => {
    render(<BreathingOverlay />)
    expect(screen.getByText('4')).toBeInTheDocument()
    act(() => { vi.advanceTimersByTime(1000) })
    expect(screen.getByText('3')).toBeInTheDocument()
    act(() => { vi.advanceTimersByTime(1000) })
    expect(screen.getByText('2')).toBeInTheDocument()
    act(() => { vi.advanceTimersByTime(1000) })
    expect(screen.getByText('1')).toBeInTheDocument()
  })

  it('переходит к фазе Задержка после вдоха', () => {
    render(<BreathingOverlay />)
    act(() => { vi.advanceTimersByTime(4000) })
    expect(screen.getByText(/Задержка/i)).toBeInTheDocument()
    expect(screen.getByText('7')).toBeInTheDocument()
  })

  it('переходит к фазе Выдох после задержки', () => {
    render(<BreathingOverlay />)
    act(() => { vi.advanceTimersByTime(11000) })
    expect(screen.getByText(/Выдох/i)).toBeInTheDocument()
    expect(screen.getByText('8')).toBeInTheDocument()
  })

  it('цикл возвращается к вдоху через 19 секунд', () => {
    render(<BreathingOverlay />)
    act(() => { vi.advanceTimersByTime(19000) })
    expect(screen.getByText(/Вдох/i)).toBeInTheDocument()
  })

  it('содержит подсказку с техникой 4-7-8', () => {
    render(<BreathingOverlay />)
    expect(screen.getByText(/4-7-8/i)).toBeInTheDocument()
  })
})
