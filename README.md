# 📻 Island Radio

<p align="center">
  A visually stunning, lightweight, and high-performance web radio player tailored for Sri Lankan online radio stations. Built with a deeply responsive mobile-first approach.
</p>

## ✨ Features

- **Sleek Dashboard Player:** A beautiful desktop dashboard format that gracefully shrinks into an ultra-compact sticky mini-player on mobile devices to prevent viewport blocking.
- **Retro Swiping Tuner:** Browse and discover active stations via a snappy, horizontal dragging carousel reminiscent of an analog radio tuner.
- **Dynamic CSS Visualizer:** Fully integrated CSS-driven graphic EQ sound wave that pulses dynamically alongside active playback.
- **Light & Dark Mode:** Native OS-level syncing with smooth animated transitons plus manual toggles saved seamlessly to LocalStorage.
- **Seamless Streaming:** Connects to the true global radio streams utilizing the open internet radio registry to curate the best HD feeds securely.
- **No Dependencies:** Built with pure Vanilla JavaScript, CSS variables, and zero bloated frameworks! Extremely fast initialization and zero setup time.

## 🚀 Getting Started

Since **Island Radio** is built entirely on the native web stack, you don't need NodeJS or NPM limits to spin it up.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/raveenjk/sl-live-radio-app.git
   ```
2. **Launch:** 
   Simply double-click the `index.html` file, or for the best viewing experience, open the folder using [VS Code Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer).
3. **Listen:** Plug in your headphones and enjoy instant playback!

## 📁 Project Structure

```
├── index.html        # Main App Entrypoint
├── data/
│   └── stations.json # Local API mock data wrapping stream mappings and logos
├── css/
│   ├── base.css      # Core variable tokens, color palettes and resets
│   ├── browse.css    # Styles relative to the search filter layout
│   └── player.css    # Logic for sticky headers, swiping carousel, and CSS visualizer
└── js/
    ├── main.js       # Main runtime tying DOM events together 
    ├── player.js     # HTML5 Audio API orchestration state machine 
    ├── store.js      # Wrappers for robust LocalStorage fetching 
    └── browse.js     # Fuzzy-search functions for locating modules 
```

## 🛠 Tech Stack

- **HTML5:** Semantic architecture
- **CSS3:** Heavy usage of Native CSS Custom Variables for theming, Flexbox for dashboards, bounding rects for animations. 
- **Vanilla JS (ES6+):** Module-pattern separation, `Audio` browser APIs, state synchronization.

## 🤝 Contributing

Contributions, issues and feature requests are welcome! 
Feel free to check [issues page](https://github.com/raveenjk/sl-live-radio-app/issues). 

## 📝 License

This project is generously distributed via open-source under the MIT License.
