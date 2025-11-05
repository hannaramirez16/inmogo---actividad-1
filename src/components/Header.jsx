import logo from '../assets/img/LOGO2.png'
import { Navbar } from './Navbar'

export const Header = () => {
  return (
  <header className="fixed top-0 left-0 right-0 z-50 bg-[#2023c80e]">
      <div className="max-w-7xl mx-auto px-4 md:px-8 py-4 flex items-center justify-between">
        <div className="flex items-center">
          <img src={logo} alt="Immongo logo" className="h-15 w-auto" />
        </div>

        <Navbar />
      </div>
    </header>
  )
}