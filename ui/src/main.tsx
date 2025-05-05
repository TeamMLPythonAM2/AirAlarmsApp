import { createRoot } from 'react-dom/client'
import dotenv from 'dotenv'
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
    <App/>
)
