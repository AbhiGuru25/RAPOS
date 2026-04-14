// Supabase Configuration for RAPOS
const SUPABASE_URL = "https://btvplzxhozcomnpiihor.supabase.co";
const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ0dnBsenhob3pjb21ucGlpaG9yIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNzcyNDMsImV4cCI6MjA5MTc1MzI0M30.diiNc-1AmqSDAuQAlu6CCWcEghUa0pgg36liQ4QDVPI";

// Backend API Configuration
// Change this to your Render/Railway URL when you deploy the backend!
const API_BASE_URL = "http://localhost:8000"; 

// Initialize the Supabase Client (avoiding variable shadowing)
const supabaseClient = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Make the client available globally for the rest of the application
window.supabase = supabaseClient;

console.log("RAPOS: Supabase initialized. API Base:", API_BASE_URL);
