# 📱 Splitora - Expense Splitting Made Simple

A beautiful, modern expense splitting app built with Expo and React Native. Accessible as a web app or native mobile app.

## ✨ Features

- 🎨 **Modern UI/UX** - Premium design with dark mode, glassmorphism, and smooth animations
- 📊 **Smart Dashboard** - Track expenses, debts, and balances at a glance
- 📈 **Trend Indicators** - See spending changes vs previous month
- 👥 **Group Expenses** - Split bills with friends and family
- 🎯 **Swipe Gestures** - Intuitive swipe-to-delete on expense items
- ⚡ **Real-time Sync** - Powered by Supabase for instant data sync
- 📱 **Responsive** - Works perfectly on all screen sizes (mobile, tablet, desktop)

## 🚀 Tech Stack

- **Framework:** Expo (React Native)
- **Navigation:** Expo Router
- **Backend:** Supabase (PostgreSQL + Auth)
- **UI:** Custom components with React Native Reanimated
- **Charts:** React Native Gifted Charts
- **Styling:** StyleSheet with theme system

## 🌐 Live Demo

**Web App:** [Coming Soon - Deploy to Vercel]

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/splitora-mobile.git

# Navigate to project
cd splitora-mobile

# Install dependencies
npm install

# Start development server
npm start
```

## 🔧 Environment Setup

Create a `.env` file in the root directory:

```env
EXPO_PUBLIC_SUPABASE_URL=your_supabase_url
EXPO_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## 📱 Running the App

### Web (Browser)
```bash
npm run web
```

### iOS Simulator (Mac only)
```bash
npm run ios
```

### Android Emulator
```bash
npm run android
```

### Expo Go (Real Device)
```bash
npm start
# Scan QR code with Expo Go app
```

## 🏗️ Building for Production

### Web Build
```bash
npm run build:web
# Output: dist/ folder
```

### Native Builds
```bash
# Install EAS CLI
npm install -g eas-cli

# Build for Android
eas build --platform android

# Build for iOS
eas build --platform ios
```

## 🎨 Key Features

### Dashboard
- Greeting card with date/time
- Color-coded stat cards (Total Spent, You Owe, Get Back)
- Trend indicators showing % change
- Recent activity feed
- Spending insights with charts

### Gestures & Interactions
- Swipe-to-delete on expenses
- Haptic feedback on actions
- Smooth page transitions
- Pull-to-refresh on lists

### UI Components
- Skeleton loaders for better UX
- Success animations
- Empty states with helpful guidance
- Custom themed components

## 📁 Project Structure

```
splitora-mobile/
├── app/                    # Expo Router pages
│   ├── (tabs)/            # Tab navigation screens
│   ├── expense/           # Expense detail screens
│   └── groups/            # Group management screens
├── components/            # Reusable components
│   └── ui/               # UI components
├── lib/                  # Utilities and configs
│   ├── context/         # React Context providers
│   ├── hooks/           # Custom React hooks
│   └── supabase.ts      # Supabase client
├── constants/           # Theme, colors, spacing
└── assets/             # Images, fonts, icons
```

## 🎯 Deployment

### Vercel (Web)
1. Push to GitHub
2. Connect repository to Vercel
3. Build command: `npm run build:web`
4. Output directory: `dist`
5. Deploy!

See [DEPLOY.md](./DEPLOY.md) for detailed instructions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for learning or building your own expense splitting app!

## 🙏 Acknowledgments

- Built with [Expo](https://expo.dev)
- Backend powered by [Supabase](https://supabase.com)
- Charts by [React Native Gifted Charts](https://github.com/Abhinandan-Kushwaha/react-native-gifted-charts)

---

Made with ❤️ for simpler expense splitting

