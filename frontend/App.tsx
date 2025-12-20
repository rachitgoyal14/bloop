import React, { useEffect } from 'react';
import Header from './components/Header';
import Hero from './components/Hero';
import Features from './components/Features';
import FAQ from './components/FAQ';
import Footer from './components/Footer';
import InteractiveBackground from './components/InteractiveBackground';

const App: React.FC = () => {
  // Enforce dark mode on body
  useEffect(() => {
    document.documentElement.classList.add('dark');
  }, []);

  return (
    <div className="min-h-screen bg-black text-white relative">
      <InteractiveBackground />
      <Header />
      <main className="relative z-10">
        <Hero />
        <Features />
        <FAQ />
      </main>
      <Footer />
    </div>
  );
};

export default App;