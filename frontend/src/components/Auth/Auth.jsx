import { useState } from 'react'
import * as api from '../../api/endpoints'
import './Auth.css'

export default function AuthForm({ onSuccess }) {
  const [mode, setMode]   = useState('login')
  const [form, setForm]   = useState({ username: '', email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const set = f => e => setForm(p => ({ ...p, [f]: e.target.value }))

  const submit = async () => {
    setError(''); setLoading(true)
    try {
      if (mode === 'register') await api.register(form)
      const res = await api.login({ email: form.email, password: form.password })
      onSuccess(res.data)
    } catch (e) {
      setError(e.response?.data?.detail || 'Ошибка. Проверьте данные.')
    } finally { setLoading(false) }
  }

  return (
    <div className="auth-form">
      <p className="auth-form__title">{mode === 'login' ? 'Войти' : 'Регистрация'}</p>

      {mode === 'register' && (
        <input className="auth-form__input" placeholder="Имя пользователя"
          value={form.username} onChange={set('username')} onKeyDown={e => e.key === 'Enter' && submit()} />
      )}
      <input className="auth-form__input" type="email" placeholder="Email"
        value={form.email} onChange={set('email')} onKeyDown={e => e.key === 'Enter' && submit()} />
      <input className="auth-form__input" type="password" placeholder="Пароль"
        value={form.password} onChange={set('password')} onKeyDown={e => e.key === 'Enter' && submit()} />

      {error && <p className="auth-form__error">{error}</p>}

      <button className="auth-form__submit" onClick={submit} disabled={loading}>
        {loading ? '...' : mode === 'login' ? 'Войти' : 'Создать аккаунт'}
      </button>
      <button className="auth-form__switch"
        onClick={() => { setMode(m => m === 'login' ? 'register' : 'login'); setError('') }}>
        {mode === 'login' ? 'Нет аккаунта? Зарегистрироваться' : 'Уже есть аккаунт? Войти'}
      </button>
    </div>
  )
}
