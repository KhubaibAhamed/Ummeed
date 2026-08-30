import { useState } from 'react';
import { LandingPage } from './components/LandingPage';
import { ChatScreen } from './components/ChatScreen';

function App() {
  const [session, setSession] = useState(null);

  if (!session) {
    return <LandingPage onSelect={setSession} />;
  }

  return <ChatScreen language={session.language} location={session.location || undefined} />;
}

export default App;
