import HeroSection from "@/components/landing/HeroSection";
import FeaturesSection from "@/components/landing/FeaturesSection";
import TimelinePreview from "@/components/landing/TimelinePreview";
import TestimonialsSection from "@/components/landing/TestimonialsSection";
import PricingSection from "@/components/landing/PricingSection";
import Footer from "@/components/layout/Footer";

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-white">
      <HeroSection />
      <FeaturesSection />
      <TimelinePreview />
      <TestimonialsSection />
      <PricingSection />
      <Footer />
    </main>
  );
}
