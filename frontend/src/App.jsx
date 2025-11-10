import { AuthProvider } from './context/AuthContext';
import { BrowserRouter as Router } from 'react-router-dom';
// Tus componentes...

function App() {
  return (
    <AuthProvider>
      <Router>
        {/* Tu contenido de la app */}
      </Router>
    </AuthProvider>
  );
}

export default App;