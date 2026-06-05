import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

vi.mock('../../api/endpoints', () => ({
  login:    vi.fn(),
  register: vi.fn(),
  logout:   vi.fn(),
  getMe:    vi.fn(),
}))
vi.mock('../../api/client', () => ({ default: {} }))

import * as apiEndpoints from '../../api/endpoints'
import AuthForm from './Auth'

const clickSubmit = () => fireEvent.click(screen.getByRole('button', { name: /Войти|Создать аккаунт/i }))

describe('AuthForm — валидация и взаимодействие', () => {
  beforeEach(() => { vi.clearAllMocks() })

  it('отображает поля Email и Пароль по умолчанию', () => {
    render(<AuthForm onSuccess={vi.fn()} />)
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument()
    expect(screen.getByPlaceholderText('Пароль')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Войти' })).toBeInTheDocument()
  })

  it('переключается в режим регистрации', async () => {
    render(<AuthForm onSuccess={vi.fn()} />)
    await userEvent.click(screen.getByText(/Нет аккаунта/))
    expect(screen.getByPlaceholderText('Имя пользователя')).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'Создать аккаунт' })).toBeInTheDocument()
  })

  it('показывает ошибку при неверных данных входа', async () => {
    apiEndpoints.login.mockRejectedValueOnce({
      response: { data: { detail: 'Invalid credentials' } }
    })
    render(<AuthForm onSuccess={vi.fn()} />)
    await userEvent.type(screen.getByPlaceholderText('Email'), 'wrong@test.com')
    await userEvent.type(screen.getByPlaceholderText('Пароль'), 'wrongpass')
    clickSubmit()
    await waitFor(() => {
      expect(screen.getByText('Invalid credentials')).toBeInTheDocument()
    })
  })

  it('вызывает onSuccess после успешного входа', async () => {
    const mockUser = { id: 1, username: 'testuser', email: 'test@test.com' }
    apiEndpoints.login.mockResolvedValueOnce({ data: mockUser })
    const onSuccess = vi.fn()
    render(<AuthForm onSuccess={onSuccess} />)
    await userEvent.type(screen.getByPlaceholderText('Email'), 'test@test.com')
    await userEvent.type(screen.getByPlaceholderText('Пароль'), 'password123')
    clickSubmit()
    await waitFor(() => { expect(onSuccess).toHaveBeenCalledWith(mockUser) })
  })

  it('при регистрации сначала вызывает register затем login', async () => {
    const mockUser = { id: 2, username: 'newuser', email: 'new@test.com' }
    apiEndpoints.register.mockResolvedValueOnce({})
    apiEndpoints.login.mockResolvedValueOnce({ data: mockUser })
    const onSuccess = vi.fn()
    render(<AuthForm onSuccess={onSuccess} />)
    await userEvent.click(screen.getByText(/Нет аккаунта/))
    await userEvent.type(screen.getByPlaceholderText('Имя пользователя'), 'newuser')
    await userEvent.type(screen.getByPlaceholderText('Email'), 'new@test.com')
    await userEvent.type(screen.getByPlaceholderText('Пароль'), 'securepass')
    fireEvent.click(screen.getByRole('button', { name: 'Создать аккаунт' }))
    await waitFor(() => {
      expect(apiEndpoints.register).toHaveBeenCalled()
      expect(apiEndpoints.login).toHaveBeenCalled()
      expect(onSuccess).toHaveBeenCalledWith(mockUser)
    })
  })

  it('кнопка недоступна во время загрузки', async () => {
    let resolve
    apiEndpoints.login.mockReturnValueOnce(new Promise(r => { resolve = r }))
    render(<AuthForm onSuccess={vi.fn()} />)
    await userEvent.type(screen.getByPlaceholderText('Email'), 't@t.com')
    await userEvent.type(screen.getByPlaceholderText('Пароль'), 'p')
    clickSubmit()
    await waitFor(() => {
      expect(screen.getByRole('button', { name: '...' })).toBeDisabled()
    })
    resolve({ data: { id: 1 } })
  })

  it('Enter в поле пароля отправляет форму', async () => {
    apiEndpoints.login.mockResolvedValueOnce({ data: { id: 1, username: 'u' } })
    const onSuccess = vi.fn()
    render(<AuthForm onSuccess={onSuccess} />)
    await userEvent.type(screen.getByPlaceholderText('Email'), 'test@test.com')
    await userEvent.type(screen.getByPlaceholderText('Пароль'), 'pass{Enter}')
    await waitFor(() => expect(onSuccess).toHaveBeenCalled())
  })
})
