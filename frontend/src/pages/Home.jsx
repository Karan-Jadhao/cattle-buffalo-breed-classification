import { useState } from "react";
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import About from "../components/About";
import Stats from "../components/Stats";
import HowItWorks from "../components/HowItWorks";
import PredictionCard from "../components/PredictionCard";
import SupportedImages from "../components/SupportedImages";
import Footer from "../components/Footer";
import LoginModal from "../components/LoginModal";
import ContactModal from "../components/ContactModal";

function Home() {
  const [loginOpen, setLoginOpen] = useState(false);
  const [contactOpen, setContactOpen] = useState(false);

  return (
    <>
      <Navbar
        onOpenLogin={() => setLoginOpen(true)}
        onOpenContact={() => setContactOpen(true)}
      />

      <main>
        <Hero />
        <About />
        <Stats />

        <section className="how-prediction-section">
          <HowItWorks />
          <PredictionCard />
        </section>

        <SupportedImages />
      </main>

      <Footer onOpenContact={() => setContactOpen(true)} />

      <LoginModal isOpen={loginOpen} onClose={() => setLoginOpen(false)} />
      <ContactModal isOpen={contactOpen} onClose={() => setContactOpen(false)} />
    </>
  );
}

export default Home;