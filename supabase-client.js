// Supabase Configuration for RAPOS
window.SUPABASE_URL = "https://btvplzxhozcomnpiihor.supabase.co";
window.SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ0dnBsenhob3pjb21ucGlpaG9yIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzYxNzcyNDMsImV4cCI6MjA5MTc1MzI0M30.diiNc-1AmqSDAuQAlu6CCWcEghUa0pgg36liQ4QDVPI";

// Backend API Configuration
window.API_BASE_URL = window.API_BASE_URL || "https://rapos-backend.onrender.com"; 

// Initialize the Supabase Client safely
if (typeof supabase !== 'undefined') {
    if (!window.supabaseClient) {
        window.supabaseClient = supabase.createClient(window.SUPABASE_URL, window.SUPABASE_ANON_KEY);
    }
    window.supabase = window.supabaseClient;
}

console.log("RAPOS: Supabase initialized. API Base:", window.API_BASE_URL);
